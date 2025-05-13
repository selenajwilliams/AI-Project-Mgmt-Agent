from flask import Flask, request, jsonify
from sheet_utils import read_sheet, update_task, prioritize_sheet
from llm_utils import prioritize
TEST = True

app = Flask(__name__)

@app.route("/")
def index():
    return "API is running! Go to /api/tasks to read, prioritize, and return tasks"

@app.route("/api/get-tasks", methods=["GET"])
def get_tasks():
    header, tasks = read_sheet()
    prioritized = prioritize(tasks)
    return jsonify([dict(zip(header, row)) for row in prioritized])

@app.route("/api/update-task", methods=["POST"])
def update_task_route():
    data = request.json  # Expect JSON task with at least 'ID' field
    task_id = str(data["ID"])
    row = [str(data.get(col, "")) for col in ["ID", "Task", "Description", "Status", "Priority", "Due Date", "Owner"]]
    success = update_task(task_id, row)
    if not success:
        return jsonify({"error": "Task not found"}), 404
    # Re-prioritize after update
    _, tasks = read_sheet()
    prioritized = prioritize(tasks)
    prioritize_sheet(prioritized)
    return jsonify({"message": "Updated and reprioritized"})

if __name__ == "__main__":

    if TEST:
        app.run(debug=True, port=5000)
    else:
        app.run(debug=True, port=5000)


