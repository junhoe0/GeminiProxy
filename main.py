import os 
from flask import Flask, request, jsonify
from google import genai
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

load_dotenv()

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits='50 per hour',
    storage_uri='memory://'
)

client = genai.Client(api_key=os.environ.get("GENAI_API_KEY"))

@app.route("/generate", methods=["POST"])
@limiter.limit('10 per minute')
def generate():
    try:
        data = request.get_json()
        prompt = data.get("prompt")
        if not prompt or prompt.strip() == "":
            return jsonify({"error": "Prompt is required"}), 400

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return jsonify({"response": response.text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
