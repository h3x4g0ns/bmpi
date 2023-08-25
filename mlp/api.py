from flask import Flask, request, jsonify
import torch
import torch.nn as nn
from torchvision import transforms

app = Flask(__name__)

# Load your model (for demonstration, I'm assuming a simple model structure)
class SimpleModel(nn.Module):
    def __init__(self):
        super(SimpleModel, self).__init__()
        self.fc = nn.Linear(3, 1)  # Change this to your model architecture

    def forward(self, x):
        return self.fc(x)

model = SimpleModel()
model.load_state_dict(torch.load("your_model_path.pth"))
model.compile()
model.eval()

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.json['data']
        tensor_data = torch.tensor(data, dtype=torch.float32)
        with torch.no_grad():
          prediction = model(tensor_data)
        
        response = {
            'prediction': prediction.numpy().tolist()
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
