import os
from flask import Flask, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file


app = Flask(__name__)

# Retrieve the API key securely from environment variable
api_key = os.getenv("GENAI_API_KEY")  # Set your environment variable GENAI_API_KEY
if not api_key:
    raise ValueError("API key is missing. Please set the GENAI_API_KEY environment variable.")

# Configure Gemini API
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route('/optimize', methods=['POST'])
def optimize_code():
    try:
        # Parse the incoming JSON request
        data = request.json
        code = data.get("code", "")

        if not code:
            return jsonify({"error": "No code provided to optimize"}), 400

        # Gemini prompt for optimization
        prompt = f"""Analyze and optimize this Python code while preserving its functionality:
        
        ```python
        {code}
        ```
        
        Explain the optimizations and provide an improved version.
        """

        # Get the response from the Gemini API
        response = model.generate_content(prompt)

        # Return the optimized code and suggestions
        return jsonify({"suggestion": response.text})

    except Exception as e:
        # In case of any error, return an error message
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000)
