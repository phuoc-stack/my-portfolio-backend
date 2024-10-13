from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

from chat import get_response

app=Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.get("/")
def index_get():
    return render_template("base.html")

@app.post("/predict")
def predict():
    print("Request Headers:", request.headers)  # Log incoming headers
    try:
        text = request.get_json().get("message")
        print(f"Received message: {text}")  # Log received message
        
        if not text:
            return jsonify({"error": "No message provided"}), 400

        response = get_response(text)  # Your logic to get the response
        print(f"Response: {response}")  # Log the response
        
        message = {"answer": response}
        return jsonify(message)
    except Exception as e:
        print(f"Error: {e}")  # Log the exception message
        return jsonify({"error": "Internal Server Error"}), 500

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "OK"})

if __name__=="__main__":
    app.run(debug=True)



