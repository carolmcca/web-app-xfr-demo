from django.http import HttpResponse
from django.db import connection
import hashlib
import mimetypes
import numpy as np
import os
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request

from server.face_recognition.predict import predict, compute_embedding, compare_embeddings
from server.models import Image
from utils.faiss_index_manager import FaissIndexManager

from django.contrib.auth.models import User
from django.db.models import Max
import cv2
import torch


@api_view(['GET'])
def health_check(request):
  """
    Endpoint to check if the server is running.

    @param request: The HTTP request object.
    @return: A response indicating that the server is alive.
  """
  return Response({"message": "I'm alive"})

@api_view(['POST'])
def verify_images(request, format=None):
  """
    Endpoint to verify if two images are of the same person.

    @param request: The HTTP request object containing either image files or image paths.
    @param format: The format of the request data (optional).
    @return: A response containing the prediction and explanation related data.
  """

  #TODO: implement SHAP-based explanations and remove hardcoded values
  responsibilities = {"african": 0.3, "asian": 0.53, "caucasian": 0.5, "middle_aged": 0.1, "young": 0.8, "big_nose": 1, "big_lips": 0.6, "black_hair": 0.8, "blonde_hair": 0.2, "curly_hair": 0.5}
  
  # Create images from the provided files or paths
  if request.POST.get('from_files') == 'true':
    image1 = request.FILES.get('image1')
    image1 = array_to_image(image1)
    image2 = request.FILES.get('image2')
    image2 = array_to_image(image2)
  else:
    image1_path = request.POST.get('image1').split('path=')[1]
    image1 = cv2.imread(image1_path)[:,:,::-1]
    image2_path = request.POST.get('image2').split('path=')[1]
    image2 = cv2.imread(image2_path)[:,:,::-1]

  if image1 is None or image2 is None:
    return Response({"error": "Both images must be provided."}, status=400)
  
  # Predict whether the images are of the same person
  prediction, croped_image, grad_pos, grad_neg = predict(image1, image2=image2)
  if prediction is None:
    return Response({"error": "We couldn't find a face on the selected image."}, status=200)

  return Response({
        "prediction": prediction,
        "responsibilities": responsibilities,
        "croped_image": croped_image,
        "grad_pos": grad_pos,
        "grad_neg": grad_neg
    })

@api_view(['POST'])
def identify_image(request, format=None):
  """
    Endpoint to search for the identity of an individual on the database.

    @param request: The HTTP request object containing either an image file or an image path.
    @param format: The format of the request data (optional).
    @return: A response containing the prediction and explanation related data.
  """

  #TODO: implement SHAP-based explanations and remove hardcoded values
  responsibilities = {"african": 0.3, "asian": 0.53, "caucasian": 0.5, "middle_aged": 0.1, "young": 0.8, "big_nose": 1, "big_lips": 0.6, "black_hair": 0.8, "blonde_hair": 0.2, "curly_hair": 0.5}

  if Image.objects.count() == 0:
    return Response({"error": "There are no images on the database."})
  
  # Create an image from the provided file or path
  if request.POST.get('from_files') == 'true':
    image1 = request.FILES.get('image1') 
    image1 = array_to_image(image1)
    image1_path = None
  else:
    image1_path = request.POST.get('image1').split('path=')[1]
    image1 = cv2.imread(image1_path)[:,:,::-1]

  if image1_path is None and image1 is None:
    return Response({"error": "A valid image must be provided."}, status=400)
  
  embedding1, _, _ = compute_embedding(image1)
  
  if embedding1 is None:
    return Response({"error": "We couldn't find a face on the selected image."}, status=200)
  
  image2 = find_pair_image(embedding1)

  base_url = os.getenv("VUE_APP_BACKEND_SERVER")
  pair_url = base_url + f'/images/?path={image2.path}'

  # Predict whether the provided image and the most similar one on the database are of the same person
  prediction, croped_image, grad_pos, grad_neg = predict(image1, embedding1=embedding1, embedding2=image2.embedding)
  if prediction is None:
    return Response({"error": "The selected image(s) don't have faces."}, status=200)

  return Response({
    "prediction": prediction,
    "responsibilities": responsibilities,
    "croped_image": croped_image,
    "pair_image": pair_url,
    "grad_pos": grad_pos,
    "grad_neg": grad_neg
  })

def array_to_image(array):
  """
    Converts an array to an image object.

    @param array: The array to convert.
    @return: The converted image.
  """
  nparray = np.frombuffer(array.read(), np.uint8)
  image = cv2.imdecode(nparray, cv2.IMREAD_COLOR) 
  image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  return image


def find_pair_image(embedding1):
  """
    Finds the most similar image in the database to the provided embedding, using cosine similarity.

    @param embedding1: The embedding to compare.
    @return: The most similar image from the database.
  """
  index_manager = FaissIndexManager()
  embedding1 = embedding1.squeeze().detach().numpy()
  search_result = index_manager.search(embedding1, k=10)
  if search_result == []:
    return None
  image_index = int(search_result) + 1
  most_similar = Image.objects.get(id=image_index)
  return most_similar

def find_pair_image_without_index(embedding1):
  """
    Finds the most similar image in the database to the provided embedding without using any index.

    @param embedding1: The embedding to compare.
    @return: The most similar image from the database.
  """
  images = Image.objects.all()
  embeddings = [torch.tensor(image.embedding).unsqueeze(0) for image in images]
  embeddings = torch.cat(embeddings, dim=0)
  similarities = torch.cosine_similarity(embeddings, embedding1, dim=1)
  most_similar_index = torch.argmax(similarities)
  most_similar = images[most_similar_index.item()]
  return most_similar

@api_view(['GET'])
def example_images(request: Request):
  """
    Endpoint to get example images.

    @param request: The HTTP request object.
    @return: A response containing URLs of example images.
  """
  example_image_dir = 'static/example_images'
  image_files = os.listdir(example_image_dir)
  image_paths = [os.path.join(example_image_dir, filename) for filename in image_files]

  base_url = os.getenv("VUE_APP_BACKEND_SERVER")

  urls = [base_url + f'/images/?path={image_path}' for image_path in image_paths]

  return Response(urls)

@api_view(['GET'])
def get_image(request):
  """
    Endpoint to retrieve an image by its path.

    @param request: The HTTP request object containing the image path.
    @return: An HTTP response with the image data.
  """
  image_path = request.GET.get('path')
  with open(image_path, 'rb') as f:
    data = f.read()
  content_type, _ = mimetypes.guess_type(image_path)
  
  return HttpResponse(data, content_type=content_type)
  
def compute_hashes(images):
  """
    Computes hashes for a list of images.

    @param images: The list of images to hash.
    @return: A list of hashes for the images.
  """
  hashes = []
  for image in images:
    image.seek(0)
    hashes.append(hash_image(image.read()))
  return hashes

def is_same_identity(embeddings, user_embedding):
  """
    Checks if the embeddings belong to the same identity as the user_embedding.

    @param embeddings: List of embeddings to check.
    @param user_embedding: The user's embedding to compare against.
    @return: True if all embeddings match the user's embedding, False otherwise.
  """
  for embedding in embeddings: 
    if not compare_embeddings(user_embedding, embedding):
      return False
  return True

def hash_image(image_data):
  """
    Generates a SHA-256 hash of the given image data.

    @param image_data: The image data to hash.
    @return: The SHA-256 hash of the image.
  """
  hasher = hashlib.sha256()
  hasher.update(image_data)
  hashed_image = hasher.hexdigest()
  return hashed_image

def hash_image_from_file(image_path):
  """
    Hashes an image from a file.

    @param image_data: The file path of the image to hash.
    @return: The SHA-256 hash of the image.
  """
  with open(image_path, 'rb') as f:
    image_data = f.read()
    return hash_image(image_data)

@api_view(['GET'])
def delete_all_images(request):
  """
    Endpoint to delete all images from the database.  

    @param request: The HTTP request object.
    @return: A response indicating that all images were removed successfully.
  """
  with connection.cursor() as cursor:
    cursor.execute("TRUNCATE TABLE server_image RESTART IDENTITY CASCADE;")
  # Rebuild the index to reset it
  index_manager = FaissIndexManager()
  index_manager.build_index(force=True)
  
  return Response({"message": "All images removed successfully."})

@api_view(['GET'])
def add_dummy_images(request):
  """
    Endpoint to add dummy images to the database.

    @param request: The HTTP request object.
    @return: A response indicating that the dummy images were added successfully.
  """
  num_embeddings = 994
  embeddings = [generate_dummy_embedding() for _ in range(num_embeddings)]
  hashes = [hash_image(np.random.bytes(256)) for _ in range(num_embeddings)]
  
  # Create a dummy user if it doesn't exist
  if not User.objects.filter(username='dummy').exists():
    user = User.objects.create_user(username='dummy', password='dummy')
  else:
    user = User.objects.get(username='dummy')

  # Add dummy embeddings to the database
  for i, (embedding, hash) in enumerate(zip(embeddings, hashes)):
    path = f'static/images/dummy_image_{i}.jpg'
    Image.objects.create(path=path, embedding=embedding, user=user, hash=hash)
  
  # Add the dummy embeddings to the index
  index_manager = FaissIndexManager()
  index_manager.add_embeddings(embeddings)

  return Response({"message": "Dummy embeddings added successfully."})

def generate_dummy_embedding(size=512):
  """
    Generates a dummy embedding of the given size.

    @param size: The size of the embedding to generate.
    @return: A dummy embedding of the given size.
  """
  return np.random.rand(size).tolist()

@api_view(['POST'])
def users_register(request):
  """
    Endpoint to register a new user.
    
    @param request: The HTTP request object containing the user's username and password.
    @return: A response indicating if the user was added successfully.
  """
  name = request.data.get('username')
  password = request.data.get('password')
  if User.objects.filter(username=name).exists():
    return Response({"detail": "This username is already taken. Please choose a different one and try again"}, status=400)
  user = User.objects.create_user(username=name, password=password)
  
  return Response({'message': 'Successfully added user'})

@api_view(['POST'])
def verify_user(request):
  """
    Endpoint to verify if an image belongs to a given user.

    @param request: The HTTP request object containing the user's username and either an image file or an image path.
    @return: A response containing the prediction and explanation related data.
  """
  user = request.data.get('username')
  
  if not User.objects.filter(username=user).exists():
    return Response({'error': 'User not found'}, status=200)
  
  user = User.objects.get(username=user)
  user_images = Image.objects.filter(user=user)
  if user_images.count() == 0:
    return Response({"error": "There are no images for this identity."})
  
  # Create an image from the provided file or path
  if request.POST.get('from_files') == 'true':
    image1 = request.FILES.get('image1') 
    image1 = array_to_image(image1)
    image1_path = None
  else:
    image1_path = request.POST.get('image1').split('path=')[1]
    image1 = cv2.imread(image1_path)[:,:,::-1]

  if image1_path is None and image1 is None:
    return Response({"error": "A valid image must be provided."}, status=400)
  
  embedding1, _, _ = compute_embedding(image1)
  if embedding1 is None:
    return Response({"error": "We couldn't find a face on the selected image."}, status=200)

  # Compute the mean of the user embeddings
  embeddings = np.vstack(user_images.values_list('embedding', flat=True))
  user_embedding = np.mean(embeddings, axis=0).astype(np.float32)

  # Predict whether the provided image matches with the mean of the user's embeddings
  prediction, croped_image, grad_pos, grad_neg = predict(image1, embedding1=embedding1, embedding2=user_embedding)

  if prediction is None:
    return Response({"error": "We couldn't find a face on the selected image(s)."}, status=200)

  #TODO: implement SHAP-based explanations and remove hardcoded values
  responsibilities = {"african": 0.3, "asian": 0.53, "caucasian": 0.5, "middle_aged": 0.1, "young": 0.8, "big_nose": 1, "big_lips": 0.6, "black_hair": 0.8, "blonde_hair": 0.2, "curly_hair": 0.5}

  base_url = os.getenv("VUE_APP_BACKEND_SERVER")
  pair_url = base_url + f'/images/?path={user_images.first().path}'

  return Response({
  "prediction": prediction,
  "responsibilities": responsibilities,
  "croped_image": croped_image,
  "pair_image": pair_url,
  "grad_pos": grad_pos,
  "grad_neg": grad_neg
})

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def users_get_or_add_images(request):
  """
  Endpoint to get or add images for a user.
  
  @param request: The HTTP request object.
  @return: A response containing the user's images or a message indicating that the images were added successfully.
  """

  user = request.user
  #If the method is GET, return the user's images
  if request.method == 'GET':
    return users_images(user)
  #If the method is POST, add the images to the database
  elif request.method == 'POST':
    images = [request.FILES.get('image' + str(i + 1)) for i in range(len(request.FILES))]
    force = request.data.get('force') == 'true'
    return add_images(user, images, force)


def add_images(user, images, force):
  """
    Adds images to the database for a given user.
    
    @param user: The user to add the images to.
    @param images: The images to add.
    @param force: A flag indicating if the images should be added even if their embeddings aren't recognized as being from the provided user.
    @return: A response indicating if the images were added successfully.
  """
  image_dir = 'static/images'
  if not os.path.exists(image_dir):
    os.makedirs(image_dir)
    
  # Create filenames for the images to be saved (img1.png, img2.png, etc.)
  last_image = Image.objects.aggregate(max_id=Max('id'))['max_id']
  first_id = 0 if last_image is None else last_image
  image_paths = [os.path.join(image_dir, f"img{first_id + i + 1}.png") for i in range(len(images))]

  embeddings = []
  for image_array in images:
    image = array_to_image(image_array)
    embedding, _, _ = compute_embedding(image)
    if embedding is None:
      return Response({"error": "We couldn't find a face on one of the uploaded images. Please try again with face images."})
    embeddings.append(embedding)

  hashes = compute_hashes(images)

  user_image = Image.objects.filter(user=user).first()
  if user_image is None:
    user_embedding = embeddings[0]
  else:
    user_embedding = torch.tensor(user_image.embedding)

 # In case the user has images on the database, check if the uploaded images belong to the user. If not, return a warning message.
  if not force and not is_same_identity(embeddings, user_embedding):
    return Response({"error": {"type": "confirm", "message": "All uploaded images must belong to the user."}})
  
  if Image.objects.filter(user=user).exists() and Image.objects.filter(user=user, hash__in=hashes).exists():
    return Response({"error": "One or more of your images are already on the database."})

  for image, path in zip(images, image_paths):
    with open(path, 'wb') as f:
      for chunk in image.chunks():
        f.write(chunk)
  
  embeddings = [embedding.tolist()[0] for embedding in embeddings]
  
  # Add images to the database
  for path, embedding, hash in zip(image_paths, embeddings, hashes):
    Image.objects.create(path=path, embedding=embedding, user=user, hash=hash) 

  # Add the embeddings to the index
  index_manager = FaissIndexManager()
  index_manager.add_embeddings(embeddings)

  return Response({"message": "Images added successfully."})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def users_auth(request):
  """
    Endpoint to authenticate a user.

    @param request: The HTTP request object.
    @return: A response indicating that the user is authenticated
  """
  return Response({"message": "You are authenticated."})


def users_images(user):
  """
    Gets the images associated with a given user.

    @param user: The user to get the images for.
    @return: A response containing the user's images.
  """
  images = Image.objects.filter(user=user)
  image_paths = [image.path for image in images]
  base_url = os.getenv("VUE_APP_BACKEND_SERVER")
  image_urls = [base_url + f'/images/?path={image_path}' for image_path in image_paths]
  return Response({"image_urls": image_urls})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def users_delete_image(request):
  """
    Endpoint to delete an image associated with a user.
    
    @param request: The HTTP request object containing the image path.
    @return: A response indicating that the image was deleted successfully.
    """
  user = request.user
  image_url = request.data.get('path')
  path = image_url.split('?path=')[1]
  image = Image.objects.filter(path=path).first()
  image_id = image.id
  if image.user == user:
    image.delete()
    os.remove(path)
    index_manager = FaissIndexManager()
    index_manager.remove_embeddings(image_id-1)
    return Response({"message": "Image deleted successfully"})
  else:
    return Response({"error", "Invalid request: the image must be associated with the logged in user"})
  
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def users_delete(request):
  """
    Endpoint to delete a user.
    
    @param request: The HTTP request object.
    @return: A response indicating that the user was deleted successfully.
  """
  user = request.user
  user.delete()
  return Response({"message": "User deleted successfully"})
  
  

