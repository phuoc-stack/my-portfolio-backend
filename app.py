from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import logging
from chat import get_response
import nltk

app=Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
logging.basicConfig(level=logging.DEBUG)

# Download the 'punkt' tokenizer if not already downloaded
try:
    nltk.data.find('tokenizers/punkt_tab')
    logging.info("Found 'punkt_tab' tokenizer.")
except LookupError:
    logging.error("Downloading 'punkt_tab' tokenizer.")
    nltk.download('punkt_tab')  # Download the resource
# Ensure 'punkt' tokenizer is also available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    logging.error("Downloading 'punkt' tokenizer.")
    nltk.download('punkt')

# Set the NLTK data path for deployment
nltk.data.path.append('/opt/render/nltk_data')

@app.get("/")
def index_get():
    return render_template("base.html")

@app.post("/predict")
def predict():
    try:
        text = request.get_json().get("message")
        if text is None:
            logging.error("No message provided in the request")
            return jsonify({"error": "No message provided"}), 400

        response = get_response(text)
        logging.info(f"Received message: {text}, Response: {response}")
        message = {"answer": response}
        return jsonify(message)
    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
        return jsonify({"error": "Internal Server Error"}), 500

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "OK"})

if __name__=="__main__":
    app.run(debug=True)



