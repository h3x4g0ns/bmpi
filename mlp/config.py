import torch
from .models.simple import SimpleModel
from .models.resnet import ResNet34
from torchvision import transforms

model_config = {
  "simple_model": {
    "model": SimpleModel,
    "params": {},
    "dtype": torch.bfloat16,
    "transforms": [
      transforms.PILToTensor(),
      transforms.ConvertImageDtype(torch.bfloat16)
    ]
  }, 
  "resnet_34": {
    "model": ResNet34,
    "params": {},
    "dtype": torch.bfloat16,
    "transforms": [
      transforms.PILToTensor(),
      transforms.ConvertImageDtype(torch.bfloat16)
    ],
  }
}

class Model:
  def __init__(self, model_name):
    config = model_config[model_name]
    self.name = model_name
    self.setup_model = config["model"]
    self.params = config["param"]
    self.dtype = config["dtype"]
    self.transforms = transforms.Compose(config["transforms"])
    self.transforms = None
    self._size = None

  def forward(self, x):
    input_data = self.transforms(x)
    with torch.no_grad():
      prediction = self.model(input_data)
    return prediction

  def __call__(self, x):
    y = self.forward(x)
    return y.numpy().tolist()

  def load(self, cache):
    model = self.setup_model(**self.params)
    self.model = torch.compile(self.model)
    status, self.device = cache.set(self.name, self.model, self.dtype)
    self.model.eval()

  
  @property
  def size(self):
    if not self._size:
      param_size = 0
      for param in self.model.parameters():
          param_size += param.nelement() * param.element_size()
      buffer_size = 0
      for buffer in self.model.buffers():
          buffer_size += buffer.nelement() * buffer.element_size()

      self._size = (param_size + buffer_size) / 1024**2
    return self._size
    