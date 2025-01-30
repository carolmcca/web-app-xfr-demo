import os
import faiss
import numpy as np
from server.models import Image

INDEX_FILE_PATH = os.getenv('FAISS_INDEX_PATH', 'faiss_index.faiss')

class FaissIndexManager:
  _instance = None

  def __new__(cls, *args, **kwargs):
    if cls._instance is None:
      cls._instance = super().__new__(cls, *args, **kwargs)
      cls._instance.index = None
      cls._instance.active_mask = None
    return cls._instance

  def __init__(self):
    if not hasattr(self, 'initialized'):
      self.initialized = True
      self.load_index()

  def build_index(self, force=False):
    """
      Build the index if it does not exist or if force is True
      
      @param force: If True, build the index from scratch even if it already exists
      @return None
    """
    if self.index is None or force:
      EMBEDDING_DIM = 512
      self.index = faiss.IndexFlatIP(EMBEDDING_DIM)
      all_images = Image.objects.all()
      embeddings = []
      self.active_mask = np.ones(len(all_images), dtype=bool)

      for image in all_images:
        embedding = np.array(image.embedding)
        embedding = embedding / np.linalg.norm(embedding)
        embeddings.append(embedding)

      if not len(embeddings) == 0:
        embeddings = np.array(embeddings, dtype='float32')
        self.index.add(embeddings)
      self.save_index()

  def save_index(self):
    """
      Save the index to disk
      
      @return None
    """
    index_dir = os.path.dirname(INDEX_FILE_PATH)
    os.makedirs(index_dir, exist_ok=True)
    faiss.write_index(self.index, INDEX_FILE_PATH)

    np.save(INDEX_FILE_PATH + '_active_mask.npy', self.active_mask)

  def load_index(self):
    """
      Load the index from disk

      @return None
    """
    if os.path.exists(INDEX_FILE_PATH) and os.path.exists(INDEX_FILE_PATH + '_active_mask.npy'):
      self.index = faiss.read_index(INDEX_FILE_PATH)
      self.active_mask = np.load(INDEX_FILE_PATH + '_active_mask.npy')
    else:
      self.build_index()

  def get_index(self):
    """
      Get the index object

      @return faiss.Index object
    """
    return self.index

  def add_embeddings(self, new_embeddings):
    """
      Add new embeddings to the index
      
      @param new_embeddings: List of embeddings to add
      @return None
    """
    new_embeddings = np.array(new_embeddings, dtype='float32')
    new_embeddings = new_embeddings / np.linalg.norm(new_embeddings, axis=1, keepdims=True)

    self.index.add(new_embeddings)
    self.active_mask = np.append(self.active_mask, [True] * len(new_embeddings))

    self.save_index()

  def remove_embeddings(self, indices):
    """
      Remove embeddings from the index
      
      @param indices: List of indices to remove
      @return None
    """
    self.active_mask[indices] = False
    self.save_index()

  def search(self, query_vector, k=10):
    """
      Search the index of the most similar embedding to the query vector
      
      @param query_vector: Query vector to search for
      @param k: Number of most similar embeddings to return
      @return List of indices of the most similar embeddings
    """
    query_vector = np.expand_dims(query_vector, axis=0).astype('float32')
    query_vector = query_vector / np.linalg.norm(query_vector)
    distances, indices = self.index.search(query_vector, k)
    active_indices = [idx for idx in indices[0] if idx>=0 and self.active_mask[idx]]
    if active_indices == []:
      return self.search(query_vector, k=k*2)
    return active_indices[0]
