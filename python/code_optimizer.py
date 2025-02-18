from flask import Flask, request, jsonify
import google.generativeai as genai
import time
import psutil
import os

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key="YOUR_GEMINI_API_KEY")

def measure_performance(func, *args):
    """Measures execution time, CPU, and memory usage of a function."""
    process = psutil.Process(os.getpid())  # Get current process
    cpu_before = process.cpu_percent(interval=None)
    mem_before = process.memory_info().rss / (1024 * 1024)  # Convert to MB
    
    start_time = time.time()
    result = func(*args)  # Run the function
    end_time = time.time()
    
    cpu_after = process.cpu_percent(interval=None)
    mem_after = process.memory_info().rss / (1024 * 1024)

    return {
        "execution_time": end_time - start_time,
        "cpu_usage": cpu_after - cpu_before,
        "memory_usage": mem_after - mem_before,
        "result": result
    }

@app.route('/optimize', methods=['POST'])
def optimize_code():
    data = request.json
    code = data.get("code", "")

    if not code.strip():
        return jsonify({"error": "No code provided."})

    prompt = f"""
    Analyze the following code and suggest an optimized version.
    Also, provide:
    - Explanation for the optimization
    - Time complexity of original vs optimized code
    - CPU and memory usage improvements.

    Code:
    ```
    {code}
    ```
    """

    model = genai.GenerativeModel("gemini-1.5-flash")

    try:
        response = model.generate_content(prompt).text
        
        # Extract relevant sections from the response (if needed, parse it better)
        optimized_code = response.split("Optimized Code:")[1].split("Explanation:")[0].strip()
        explanation = response.split("Explanation:")[1].split("Time Complexity:")[0].strip()
        time_complexity = response.split("Time Complexity:")[1].split("CPU Usage:")[0].strip()
        cpu_usage = response.split("CPU Usage:")[1].split("Memory Usage:")[0].strip()
        memory_usage = response.split("Memory Usage:")[1].strip()

        return jsonify({
            "optimized_code": optimized_code,
            "explanation": explanation,
            "time_complexity": time_complexity,
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage
        })
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
