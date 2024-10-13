from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

from chat import get_response

app=Flask(__name__)
CORS(app)

@app.get("/")
def index_get():
    return render_template("base.html")

@app.post("/predict")
def predict():
    try:
        text = request.get_json().get("message")
        response = get_response(text)
        print(f"Response: {response}")  
        message = {"answer": response}
        return jsonify(message)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "OK"})

if __name__=="__main__":
    app.run(debug=True)



