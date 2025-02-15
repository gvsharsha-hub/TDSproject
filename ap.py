from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Mock function to simulate task execution by an LLM
def execute_task(task_description):
    # Simulate task execution logic
    # Normally, you would call an LLM or other services to process the task
    if task_description.lower() == "generate error report":
        return "Error report generated successfully", 200
    elif task_description.lower() == "parse log file":
        return "Log file parsed and summary generated", 200
    else:
        raise ValueError("Unknown task description")

# POST /run?task=<task description>
@app.route('/run', methods=['POST'])
def run_task():
    # Extract task description from query parameters
    task_description = request.args.get('task', None)
    
    if not task_description:
        return jsonify({"error": "Task description is required"}), 400

    try:
        # Execute the task by calling the mock function
        message, status_code = execute_task(task_description)
        if status_code == 200:
            return jsonify({"message": message}), 200
        else:
            return jsonify({"error": "Unknown error occurred during task execution"}), 500
    except ValueError as e:
        # Handle specific known errors
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        # Catch other unexpected errors
        return jsonify({"error": "Internal server error"}), 500

# GET /read?path=<file path>
@app.route('/read', methods=['GET'])
def read_file():
    file_path = request.args.get('path', None)
    
    if not file_path:
        return jsonify({"error": "File path is required"}), 400
    
    # Check if the file exists
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            file_content = file.read()
        return file_content, 200
    else:
        return jsonify({"error": "File not found"}), 404

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
