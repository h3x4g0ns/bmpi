import time
from collections import OrderedDict
import torch

class GPUCache:
  def __init__(self, num_gpus=1, ttl=300):
    """
    Initialize the cache
    Param:
      num_gpus: Number of GPUs to be managed by the cache.
      ttl: Time to live (expiry time) in seconds for each cache item.
    """
    self.caches = [OrderedDict() for _ in range(num_gpus)]
    self.ttl = ttl
    self.num_gpus = num_gpus
    self.current_gpu = 0  # For round-robin allocation
  
  def _get_gpu_free_memory(self, device):
    """
    Retrieve the available GPU memory for a given device
    """
    torch.cuda.empty_cache()  # Clear unused memory
    return torch.cuda.memory_reserved(device) - torch.cuda.memory_allocated(device)

  def _evict_models(self, required_space, device):
    """
    Evict models based on LRU and required space for a specific device
    """
    cache = self.caches[device.index]
    evicted_space = 0
    while evicted_space < required_space and cache:
      key, (timestamp, model, size) = cache.popitem(last=False)
      evicted_space += size
      del model
    return evicted_space >= required_space

  def set(self, key, model, dtype):
    """
    Add a model to the cache
    Evicts models if there's not enough GPU memory
    """
    device = torch.device(f"cuda:{self.current_gpu}")
    model_size = torch.numel(model) * model.element_size()  # size in bytes

    if model_size > self._get_gpu_free_memory(device):
      if not self._evict_models(model_size, device):
        return False, -1
    
    # Cache the model
    model = model.to(device=device, dtype=dtype)  # Move model to the appropriate GPU
    cache = self.caches[self.current_gpu]
    if key in cache:
      del cache[key]
    cache[key] = (time.time(), model, model_size)
    
    # Round-robin for next allocation
    self.current_gpu = (self.current_gpu + 1) % self.num_gpus
    return True, device

  def get(self, key):
    """
    Retrieve a model from the cache by key
    If the key does not exist or the item is expired, it returns None
    """
    for device_index, cache in enumerate(self.caches):
      if key in cache:
        timestamp, model, _ = cache[key]
        if time.time() - timestamp <= self.ttl:
          device = torch.device(f"cuda:{device_index}")
          model = model.to(device)  # Move model to the appropriate GPU if needed
          del cache[key]
          cache[key] = (timestamp, model, _)
          return model
        else:
          del cache[key]
    return None

  def clear_expired(self):
    """
    Clear all expired models from the cache
    """
    for cache in self.caches:
      to_remove = []
      for key, (timestamp, _, _) in cache.items():
        if time.time() - timestamp > self.ttl:
          to_remove.append(key)
        else:
          break
      for key in to_remove:
        del cache[key]
