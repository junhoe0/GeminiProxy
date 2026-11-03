import os 
from flask import Flask, request, jsonify
from google import genai
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import google.api_core import errors

load_dotenv()

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits='50 per hour',
    storage_uri='memory://'
)

client = genai.Client(api_key=os.environ.get("GENAI_API_KEY"))
fallbackChain = [
    "gemini-3.8-flash",
    "gemini-3.6-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-2.5-pro",
    "gemini-2.5-flash",
    "gemini-2.5-flash-lite"
]

@app.route("/generate", methods=["POST"])
@limiter.limit('10 per minute')
def generate():
    try:
        data = request.get_json()
        prompt = data.get("prompt")
        if not prompt or prompt.strip() == "":
            return jsonify({"error": "Prompt is required"}), 400

        responseTxt = None

        for model in fallbackChain:
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                )
                responseTxt = response.text
                break
            except (errors.ServiceUnavailable, errors.ResourceExhausted):
                print(f"Model {model} is currently overloaded. Dropping down to next layer.")
                continue
        
        if responseTxt is None:
            return jsonify({"error":"All Gemini models are currently experiencing high demand right now. Please try again later."}), 503

        return jsonify({"response": response.text}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
