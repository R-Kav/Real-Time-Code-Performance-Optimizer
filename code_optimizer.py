from flask import Flask, request, jsonify
import google.generativeai as genai
import time
import os

# Set up Gemini API key
genai.configure(api_key="AIzaSyCTT3yvUykioJKo9tMqZDB6VcdDQWCXfiE")

app = Flask(__name__)

@app.route('/optimize', methods=['POST'])
def suggest_optimization():
    code_snippet = request.json.get('code')
    
    # Request optimized code
    optimization_prompt = f"""
    Analyze the following Python code and suggest performance improvements.
    Provide explanations and optimized code if possible.

    Code:

    {code_snippet}

    Suggested optimizations:
    """

    model = genai.GenerativeModel("gemini-1.5-flash")

    for attempt in range(3):
        try:
            # Step 1: Generate optimized code
            response = model.generate_content(optimization_prompt)
            optimized_code = response.text

            # Step 2: Get explanation
            explanation_prompt = f"Explain the improvements in the following optimized code:\n{optimized_code}"
            explanation_response = model.generate_content(explanation_prompt)

            # Step 3: Get time complexity
            time_complexity_prompt = f"Provide the time complexity (Big-O) of the following optimized code:\n{optimized_code}"
            time_complexity_response = model.generate_content(time_complexity_prompt)

            # Step 4: Get space complexity
            space_complexity_prompt = f"Provide the space complexity (Big-O) of the following optimized code:\n{optimized_code}"
            space_complexity_response = model.generate_content(space_complexity_prompt)

            # Step 5: Performance score (Before & After)
            performance_prompt = f"""
            Compare the performance of the original and optimized code in terms of execution time and efficiency.
            Assign a performance score (0-100) for both versions, considering improvements in speed and resource usage.

            Original Code:

            {code_snippet}

            Optimized Code:

            {optimized_code}

            Provide the performance score before and after optimization.
            """
            performance_response = model.generate_content(performance_prompt)

            return jsonify({
                'optimized_code': optimized_code,
                'explanation': explanation_response.text,
                'time_complexity': time_complexity_response.text,
                'space_complexity': space_complexity_response.text,
                'performance_score': performance_response.text,
                'cpu_usage': 'Not available.',
                'memory_usage': 'Not available.'
            })

        except Exception as e:
            if "grpc_wait_for_shutdown_with_timeout" in str(e) or "Resource has been exhausted" in str(e):
                time.sleep(30)
            else:
                return jsonify({'error': str(e)})

    return jsonify({'error': 'Failed to generate a response due to timeout or quota limits.'})

if __name__ == "__main__":
    app.run(port=5000)
