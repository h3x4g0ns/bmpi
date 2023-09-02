import _pickle as cPickle
import zlib

class JADO:
  def __setattr__(self, key, value):
    if isinstance(value, dict):
      self.__dict__[key] = JADO.from_dict(value)
    else:
      self.__dict__[key] = value
      
  def __getattr__(self, key):
    return self.__dict__.get(key, None)

  def __repr__(self):
    return str(self.__dict__)

  @classmethod
  def from_dict(cls, data_dict):
    obj = cls()
    for key, value in data_dict.items():
      setattr(obj, key, value)
    return obj
  
  def save(self, filename):
    """
    Serialize and compress the object and save to a file.

    Args:
        filename (str): Path to the file where object will be saved.
    """
    compressed_data = zlib.compress(cPickle.dumps(self))
    with open(filename, 'wb') as file:
      file.write(compressed_data)

  @classmethod
  def load(cls, filename):
    """
    Load a compressed object from a file and deserialize it.

    Args:
        filename (str): Path to the file to load the object from.

    Returns:
        JADO: Deserialized JADO object.
    """
    with open(filename, 'rb') as file:
      compressed_data = file.read()
      return cPickle.loads(zlib.decompress(compressed_data)) 
