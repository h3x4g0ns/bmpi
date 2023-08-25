import time
from collections import OrderedDict
import torch

class GPUCache:
  def __init__(self, ttl=300):
    """
    Initialize the cache
    Param:
      ttl: Time to live (expiry time) in seconds for each cache item.
    """
    self.cache = OrderedDict()
    self.ttl = ttl

  def _get_gpu_free_memory(self):
    """
    Retrieve the available GPU memory
    """
    torch.cuda.empty_cache()  # Clear unused memory
    return torch.cuda.memory_reserved() - torch.cuda.memory_allocated()

  def _evict_models(self, required_space):
    """
    Evict models based on LRU and required space
    """
    evicted_space = 0
    while evicted_space < required_space and self.cache:
      key, (timestamp, model, size) = self.cache.popitem(last=False)
      evicted_space += size
      del model  # Ensure the model is deleted and memory is freed
    return evicted_space >= required_space

  def set(self, key, model):
    """
    Add a model to the cache
    Evicts models if there's not enough GPU memory
    """
    model_size = self._get_gpu_free_memory()
    if model_size > self._get_gpu_free_memory():
      if not self._evict_models(model_size):
        # Even after eviction, we couldn't free up enough memory
        return False

    # Cache the model
    if key in self.cache:
      del self.cache[key]
    self.cache[key] = (time.time(), model, model_size)
    return True

  def get(self, key):
    """
    Retrieve a model from the cache by key
    If the key does not exist or the item is expired, it returns None
    """
    if key in self.cache:
      timestamp, model, _ = self.cache[key]
      if time.time() - timestamp <= self.ttl:
        # Move the accessed model to the end
        del self.cache[key]
        self.cache[key] = (timestamp, model, _)
        return model
      else:
        # Model has expired
        del self.cache[key]
    
    return None

  def clear_expired(self):
    """
    Clear all expired models from the cache
    """
    to_remove = []
    for key, (timestamp, _, _) in self.cache.items():
      if time.time() - timestamp > self.ttl:
        to_remove.append(key)
      else:
        break

    for key in to_remove:
      del self.cache[key]
