import torch.nn as nn

class SimpleModel(nn.Module):
  def __init__(self):
    super(SimpleModel, self).__init__()
    self.fc = nn.Linear(3, 1)

  def forward(self, x):
    return self.fc(x)
    