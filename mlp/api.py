from flask import Flask, request, jsonify
from config import Model
from cache import ModelCache

app = Flask(__name__)

cache = ModelCache()

@app.route("/api/v1/simple_model", methods=["POST"])
def predict():
    try:
        model_name = "simple_model"
        model = cache.get(model_name)
        if not model:
            model = Model(model_name="simple_model")
        data = request.json['data']
        prediction = model(data)
        response = {
            'prediction': prediction
        }
        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
