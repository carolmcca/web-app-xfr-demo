import os
from annoy import AnnoyIndex
from server.models import Image
import numpy as np

INDEX_FILE_PATH = os.getenv('ANNOY_INDEX_PATH', 'annoy_index.ann')

class AnnoyIndexManager:
  _instance = None

  def __new__(cls, *args, **kwargs):
    if cls._instance is None:
      cls._instance = super().__new__(cls, *args, **kwargs)
      cls._instance.index = None
    return cls._instance

  def __init__(self):
    if not hasattr(self, 'initialized'):
      self.initialized = True
      self.load_index()

  def build_index(self, force=False):
    if self.index is None or force:
      EMBEDDING_DIM = 512
      self.index = AnnoyIndex(EMBEDDING_DIM, 'angular')  # cosine similarity
      all_images = Image.objects.all()
      for i, image in enumerate(all_images):
        embedding = np.array(image.embedding)
        self.index.add_item(i, embedding)
      self.index.build(1000)
      self.save_index()

  def save_index(self):
    index_dir = os.path.dirname(INDEX_FILE_PATH)
    os.makedirs(index_dir, exist_ok=True)
    self.index.save(INDEX_FILE_PATH)

  def load_index(self):
    if os.path.exists(INDEX_FILE_PATH):
      EMBEDDING_DIM = 512
      self.index = AnnoyIndex(EMBEDDING_DIM, 'angular')  # cosine similarity
      self.index.load(INDEX_FILE_PATH)
    else:
      self.build_index()

  def get_index(self):
    return self.index
