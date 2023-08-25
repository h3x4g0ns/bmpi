from flask import Flask, request, jsonify
from .config import Model
from .cache import ModelCache
import logging
import time

app = Flask(__name__)
cache = ModelCache()

@app.route("/api/v1/simple_model", methods=["POST"])
def predict():
  try:
    model_name = "simple_model"
    model = cache.get(model_name)
    if not model:
        logging.warning(f"{model_name} not found in cache")
        model = Model(model_name="simple_model")
        cache.set(model_name, model)
    logging.info(f"serving {model_name}")
    
    data = request.json['data']
    start = time.time()
    prediction = model(data)
    duration = time.time() - start
    logging.info(f"{model_name} pass took {duration}")
    response = {
        'prediction': prediction
    }
    return jsonify(response), 200

  except Exception as e:
    return jsonify({'error': str(e)}), 400

if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=8080)
