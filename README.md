# Flask GenAI API Service

This is a lightweight Flask application that integrates with the Google GenAI SDK to generate content using the `gemini-2.5-flash` model.

## Why use this?
* This approach protects your private API key by storing it safely as an environment variable instead of hardcoding it.
* Storing your API key as an environment variable helps hide sensitive credentials and keeps your project secure.

## Prerequisites

* Python 3.8+
* A Google Gemini API Key

## Installation

1. **Clone the repository or save the script as `main.py`.**
2. **Install the required dependencies:**
```bash
pip install -r requirements.txt

```


3. **Set up your environment variables:**
Create a `.env` file in the same directory and add your API key:
```env
GENAI_API_KEY=your_actual_api_key_here

```



## Running the Application

Start the Flask server by running:

```bash
python main.py

```

The server will run on `[http://0.0.0.0:3000](http://0.0.0.0:3000)` by default (or the port specified in your environment variables).

## API Usage

### Generate Content

* **Endpoint:** `/generate`
* **Method:** `POST`
* **Content-Type:** `application/json`

**Request Body:**

```json
{
  "prompt": "Write a quick joke about computers."
}

```

**Success Response (`200 OK`):**

```json
{
  "response": "Why do programmers prefer dark mode? Because light attracts bugs!"
}

```

**Error Response (`400 Bad Request` or `500 Internal Server Error`):**

```json
{
  "error": "Prompt is required"
}

```
