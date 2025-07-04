from flask import Flask, request, jsonify
import joblib

# Load your saved model
model = joblib.load("model.pkl")

app = Flask(__name__)

@app.route("/")
def home():
    return "ML Model API is running!"


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(force=True)
    print("Received data:", data)

    try:
        iq = float(data.get("iq", 0))
        cgpa = float(data.get("cgpa", 0))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid input: iq and cgpa must be numeric."}), 400

    try:
        prediction = model.predict([[iq, cgpa]])
        result = int(prediction[0])

        # Map result to message
        if result == 1:
            message = "Might get placed"
        else:
            message = "Need to work hard and focus on skills"

        return jsonify({"prediction": message})
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500


@app.route("/form")
def form():
    return """
    <html>
      <body>
        <h2>Predict using your model</h2>
        <form id="predictForm">
          <label>IQ:</label><br>
          <input type="number" id="iq" name="iq"><br><br>
          <label>CGPA:</label><br>
          <input type="number" step="0.01" id="cgpa" name="cgpa"><br><br>
          <button type="button" onclick="sendPrediction()">Predict</button>
        </form>
        <h3 id="result"></h3>
        <script>
          function sendPrediction() {
            const iq = parseFloat(document.getElementById('iq').value);
            const cgpa = parseFloat(document.getElementById('cgpa').value);

            fetch('/predict', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({ iq: iq, cgpa: cgpa })
            })
            .then(response => response.json())
            .then(data => {
              document.getElementById('result').innerText = "Prediction: " + data.prediction;
            })
            .catch(error => {
              console.error('Error:', error);
            });
          }
        </script>
      </body>
    </html>
    """
import os
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
