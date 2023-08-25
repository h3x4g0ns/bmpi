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
    model = model_config[model_name]["model"]
    params = model["param"]
    dtype = model["dtype"]
    self.transforms = transforms.Compose(model["transforms"])
    self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    self.model = model["model"](**params)
    self.model = self.model.to(device=self.device, dtype=dtype)
    self.model = torch.compile(self.model)
    self.model.eval()
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
    