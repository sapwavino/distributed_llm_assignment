from bson import ObjectId
from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import logging
from huggingface_hub import login
from pymongo import MongoClient, errors
from datetime import datetime

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

try:
    login(
        token="HF_TOKEN_HERE"
    )  # HUGGINGFACE TOKEN. USE WITH ACCOUNT THAT HAS PERMISSIONS TO ACCESS GATED MODELS
    logging.info("✅Logged in to huggingface successfully")
except Exception as e:  # USING CATCH-ALL EXCEPTION FOR ASSIGNMENT PURPOSES
    logging.error("❌Error logging into huggingface: %s", str(e))


try:
    # MongoDB connection
    client = MongoClient(
        "mongodb://0.0.0.0:27017/"
    )  # or MongoClient("mongodb://mongo:27017/") TO CONNECT TO MONGO VIA DOCKER SERVICE
    db = client["conversation_history"]
    conversations_collection = db["conversations"]
    logging.info("✅Connected to mongodb successfully")
except errors.ConnectionFailure or errors.ConfigurationError as e:
    logging.error("❌Error connecting to mongodb: %s", str(e))


models = {
    "llama2": "meta-llama/Meta-Llama-3-8B",  # USING LLAMA 3 BECAUSE LLAMA 2 NEEDS A HUGGINGFACE PRO SUBSCRIPTION
    "mistral": "mistralai/Mistral-7B-v0.1",
}

selected_model = None


@app.route("/select_model", methods=["POST"])
def select_model():
    global selected_model
    model_name = request.json.get("model")
    if model_name in models:
        selected_model = models[model_name]
        return jsonify({"message": f"Model {model_name} selected."}), 200
    logging.error("Model not found: %s", model_name)
    return jsonify({"error": "Model not found."}), 404


@app.route("/query", methods=["POST"])
def query():

    if not selected_model:
        logging.warning("No model selected.")
        return jsonify({"error": "No model selected."}), 400

    user_query = request.json.get("query")
    if not user_query:
        logging.warning("Empty query received.")
        return jsonify({"error": "Query cannot be empty."}), 400

    try:
        # Load model and tokenizer
        tokenizer = AutoTokenizer.from_pretrained(selected_model)
        model = AutoModelForCausalLM.from_pretrained(selected_model)

        # Generate response
        inputs = tokenizer(user_query, return_tensors="pt")
        outputs = model.generate(**inputs, max_new_tokens=50)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Update conversation history in MongoDB
        conversation = {
            "query": user_query,
            "response": response,
            "timestamp": datetime.now(),
        }
        conversations_collection.insert_one(conversation)

        return jsonify({"response": response}), 200

    except Exception as e:
        logging.error("❌Error during query processing: %s", str(e))
        return (
            jsonify({"error": "An error occurred while processing your request."}),
            500,
        )


@app.route("/history", methods=["GET"])
def history():
    conversations = list(conversations_collection.find().sort("timestamp", -1))
    for conversation in conversations:
        conversation["_id"] = str(conversation["_id"])
    return jsonify(conversations), 200


@app.route("/conversation/<conversation_id>", methods=["GET"])
def get_conversation(conversation_id):
    conversation = conversations_collection.find_one({"_id": ObjectId(conversation_id)})
    if conversation:
        return jsonify(conversation), 200
    else:
        return jsonify({"error": "Conversation not found."}), 404


if __name__ == "__main__":
    app.run(debug=True)
