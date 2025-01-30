import torch
from torch import nn
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
matplotlib.use('agg')

from PIL import Image
import torchvision.transforms as transforms

from server.face_recognition.iresnet import iresnet34, ExtendediResNet34
import time
from server.face_recognition.align_trans import norm_crop
import io
from facenet_pytorch import MTCNN
import base64


def create_model(path,device):
  """
    Creates an iresnet34 model from a given path

    @param path: path to model backbone
    @param device: device on which to run the model
    @return: model
  """
  loaded_model = iresnet34()
  
  state_dict = torch.load(path, map_location=device)
  loaded_model.load_state_dict(state_dict,strict=True)
  loaded_model = loaded_model.to(device)
  return loaded_model

def preprocess_image(img, device="cpu"):
  """
    Performs pre-processing operations (face alignment and crop) on a single image
    
    @param image_path: path to image
    @param device: device on which to run the models
    @return: pre-processed image tensor
  """
  mtcnn = MTCNN(select_largest=True, post_process=False, device=device)
  try:
    boxes, probs, landmarks = mtcnn.detect(img, landmarks=True)
  except Exception as e:
    return None
  if landmarks is None:
    return None, None

  facial5points = landmarks[0]

  warped_face, _ = norm_crop(img, landmark=facial5points, createEvalDB=True)
  img = Image.fromarray(warped_face[:, :, ::-1])

  transform = transforms.Compose([
        transforms.Resize((112, 112)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
    ])

  input_tensor = transform(img)
  input_tensor = input_tensor.to(torch.float)

  
  plt.clf()
  plt.imshow(warped_face)
  plt.axis('off')
  plt.tight_layout()
  buf = io.BytesIO()
  plt.savefig(buf, bbox_inches='tight', pad_inches=0, dpi=300, transparent=True)
  buf.seek(0)
  image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
  buf.close()

  return input_tensor, image_base64

def compare_embeddings(embedding1, embedding2, cos=torch.nn.CosineSimilarity(dim=1, eps=1e-10)):
  """
    Gets the cosine similarity between images and thresholds it to determine if they are the same person
  
    @param emb1: first image embedding
    @param emb2: second image embedding
    @param cos: cosine similarity function
    @return: boolean indicating whether the images are of the same person
  """
  similarity = cos(embedding1, embedding2).item()
  threshold = 0.37185913324356085

  return similarity > threshold

def compute_embedding(image, model=create_model('server/face_recognition/253682backbone.pth', 'cpu'), device="cpu"):
  """
    Gets embedding for an image tensor using a given model
    @param image_tensor: image tensor
    @param model: model used for embedding extraction
    @param device: device on which to run the model
    @return: embedding tensor
  """
  image_tensor, img = preprocess_image(image)
  if image_tensor is None:
    return None, None, None

  image_tensor = image_tensor.to(device)
  image_tensor.requires_grad_(True)
  image_tensor = image_tensor.unsqueeze(0)

  model.eval()
  embedding = model(image_tensor.clone())
  return embedding, image_tensor, img

def predict(image1, image2=None, embedding1=None, embedding2=None, model_path='server/face_recognition/253682backbone.pth', device='cpu'):
  """
    Predicts if two images are of the same person and generates the xSSAB gradient maps for the first image
  
    @param image1: first image
    @param image2: second image
    @param emb1: first image embedding
    @param emb2: second image embedding
    @param model_path: path to model backbone
    @param device: device on which to run the model
    @return: boolean indicating whether the images are of the same person, gradient maps for the images
  """

  assert image2 is not None or embedding2 is not None, "Either image2 or embedding2 must be provided"
  assert image1 is not None or embedding1 is not None, "Either image1 or embedding1 must be provided"
  
  device = torch.device("cpu" if torch.backends.mps.is_available() else "cpu")
  model = create_model(model_path ,device)
  model.eval()

  if embedding1 is None:
    embedding1, input_tensor1, croped_image = compute_embedding(image1, model, device)
  else:
    if not isinstance(embedding1, torch.Tensor):
      embedding1 = torch.tensor(embedding1).to(device)
      embedding1 = embedding1.unsqueeze(0)
    input_tensor1, croped_image = preprocess_image(image1)
    input_tensor1 = input_tensor1.to(device)
    input_tensor1.requires_grad_(True)
    input_tensor1 = input_tensor1.unsqueeze(0)
  
  if embedding2 is None:
    embedding2, _, _ = compute_embedding(image2, model, device)
  else:
    embedding2 = torch.tensor(embedding2).to(device)
    embedding2 = embedding2.unsqueeze(0)
  
  if embedding1 is None or embedding2 is None:
    return None, None, None, None

  prediction = compare_embeddings(embedding1, embedding2)  
  th = 0.37185913324356085
  gradient_1_2_pos, gradient_1_2_neg = compute_grads(input_tensor1, embedding1, embedding2, th, model, model_path, device)

  combi = gradient_1_2_pos - gradient_1_2_neg
  grad_pos = np.where(combi > 0, combi, 0)
  grad_neg = np.where(combi < 0, -combi, 0)
  
  grad_pos = create_image(grad_pos, "#42b983")
  grad_neg = create_image(grad_neg, "#e74c3c")
  
  return prediction, croped_image, grad_pos, grad_neg

def create_image(grad, color):
  """
    Creates a gradient map image from a given gradient map

    @param grad: gradient map
    @param color: color of the gradient map
    @return: base64 encoded image
  """

  transparency_color = (0, 0, 0, 0)
  end_color = tuple(int(color[i:i+2], 16) / 255.0 for i in (1, 3, 5))
  start_color = (end_color[0], end_color[1], end_color[2], 0.8)
  
  # Create a custom colormap
  cmap_colors = [transparency_color, start_color, end_color]
  cmap_name = 'custom'
  cm = mcolors.LinearSegmentedColormap.from_list(cmap_name, cmap_colors)

  # visualize gradient map
  bound = max(np.abs(grad.flatten()))
  plt.clf()
  plt.imshow(grad, vmin=0, vmax=bound, cmap=cm)
  plt.axis('off')
  plt.tight_layout()
  buf = io.BytesIO()
  plt.savefig(buf, bbox_inches='tight', pad_inches=0, dpi=300, transparent=True)
  buf.seek(0)
  image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
  buf.close()
  return image_base64
  

def compute_grads(img1, embedding1, embedding2, th, model, model_path='server/face_recognition/253682backbone.pth', device='cpu'):
  """
    Computes the xSSAB gradient maps for a given image and embeddings

    @param img1: first image tensor
    @param emb1: first image embedding
    @param emb2: second image embedding
    @param th: threshold for positive/negative features
    @param model: model used for gradient computation
    @param model_path: path to model backbone
    @param device: device on which to run the model
    @return: gradient maps for the first image
  """
  
  state_dict = torch.load(model_path, map_location=device)
  model_cos = ExtendediResNet34(state_dict)
  model_cos = model_cos.to(device)
  model_cos.eval()

  gradient_pos = get_gradient(img1, embedding1, embedding2, model_cos, model, 1, 'Balanced34', th)
  gradient_neg = get_gradient(img1, embedding1, embedding2, model_cos, model, 2, 'Balanced34', th)

  gradient_1_2_pos = np.mean(gradient_pos,axis=2)
  gradient_1_2_neg = np.mean(gradient_neg,axis=2)

  return [gradient_1_2_pos, gradient_1_2_neg]



def get_gradient(img_1, emb1, emb2, model, model_emb, version, model_name, thr):
  """
    Computes the xSSAB gradient map (positive or negative) for a given image and embeddings
    
    @param img_1: first image tensor
    @param emb1: first image embedding
    @param emb2: second image embedding
    @param model: model used for gradient computation
    @param model_emb: model used for embedding extraction
    @param version: version of the model
    @param model_name: name of the model
    @param thr: threshold for positive/negative features
    @return: gradient map for the first image
  """
  cos, root_1 = get_cosine(img_1, emb1, emb2, model, model_emb, version, model_name, thr)
  cos.retain_grad()
  root_1.retain_grad()
  feature = cos.squeeze()

  feature.backward(retain_graph=True)

  feature_gradients = root_1.grad

  fg = feature_gradients.detach().cpu().numpy().squeeze()
  fg = np.transpose(fg, (1, 2, 0))  # (height, width, channel)

  return fg

def get_cosine(img_1, emb_1, emb_2, model, model_emb, version, model_name, thr, device='cpu'):
  """
    Compute cosine similarity of img_1 and img_2 with possibility to hide positive/negative features.

    @param img_1: first image tensor
    @param emb_1: first image embedding
    @param emb_2: second image embedding
    @param model: model used for gradient computation
    @param model_emb: model used for embedding extraction
    @param version: version of the model
    @param model_name: name of the model
    @param thr: threshold for positive/negative features
    @param device: device on which to run the model
    @return: cosine similarity of the images
  """

  # normalize embedding
  emb_1 = nn.functional.normalize(emb_1, p=2.0, dim=1)
  emb_1 = emb_1.detach().cpu().numpy().squeeze()
  emb_2 = nn.functional.normalize(emb_2, p=2.0, dim=1)
  emb_2 = emb_2.detach().cpu().numpy().squeeze()

  # remove irrelevant features
  if version == 0:  # standard cosine similarity computation
    emb_2 = emb_2.detach().squeeze()
    model.cosine_layer.weight = nn.Parameter(emb_2)
  elif version == 1:  # only keep positive features
    bound = thr / len(emb_1)
    weights = torch.tensor([x[1] if x[0] >= bound else 0.0 for x in np.column_stack((np.multiply(emb_1, emb_2), emb_2))])
    weights = weights.to(device)
    model.cosine_layer.weight = nn.Parameter(weights)
  else:  # only keep negative features
    bound = thr / len(emb_1)
    weights = torch.tensor([x[1] if x[0] < bound else 0.0 for x in np.column_stack((np.multiply(emb_1, emb_2), emb_2))])
    weights = weights.to(device)
    model.cosine_layer.weight = nn.Parameter(weights)

  #img = utils_os.transform_img(img_1)
  cos = model(img_1.clone())
  return cos, img_1

