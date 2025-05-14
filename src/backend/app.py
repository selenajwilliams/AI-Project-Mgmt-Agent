from flask import Flask, request, jsonify, Response
from sheet_utils import read_sheet, update_task, prioritize_sheet
from llm_utils import prioritize
from flask_cors import CORS
# import gunicorn
import uuid  # For generating unique IDs in add-task 
TEST = False
LOCAL_DEPLOY = False

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    data = "API is running! Go to /api/tasks to read, prioritize, and return tasks\n"
    return Response(data, status=200, mimetype="text/plain")


@app.route("/api/get-tasks", methods=["GET"])
def get_tasks():
    header, tasks = read_sheet()
    prioritized = prioritize(tasks)
    return jsonify([dict(zip(header, row)) for row in prioritized])

@app.route("/api/add-task", methods=["POST"])
def add_task_route():
    data = request.json
    task_id = str(uuid.uuid4().int)[:10]  # 10-digit unique ID
    # Create a new row in the correct column order
    row = [
        task_id,
        data.get("Task", ""),
        data.get("Description", ""),
        data.get("Status", "Incomplete"),
        data.get("Priority", "Low"),
        data.get("Due Date", ""),
        data.get("Owner", "")
    ]

    success = update_task(task_id, row, create_new=True)  # Allow creating a new row
    if not success:
        return jsonify({"error": "Failed to add task"}), 500

    # Re-prioritize tasks
    _, tasks = read_sheet()
    prioritized = prioritize(tasks)
    prioritize_sheet(prioritized)

    return jsonify({"message": "Task added and prioritized", "task_id": task_id})


@app.route("/api/complete-task", methods=["POST"])
def complete_task_route():
    data = request.json
    task_name = data.get("Task", "").strip()

    if not task_name:
        return jsonify({"error": "Missing Task name"}), 400

    header, all_rows = read_sheet()
    for row in all_rows:
        if row[1].strip() == task_name:
            updated_row = row.copy()
            updated_row[3] = "Complete"  # Status column
            success = update_task(row[0], updated_row)
            if success:
                print(f"completed [{task_name}]")

                
                # Re-prioritize after marking complete
                # not necessary for now -- saving API credits
                # _, tasks = read_sheet()
                # prioritized = prioritize(tasks)
                # prioritize_sheet(prioritized)

                return jsonify({"message": f"Marked '{task_name}' as complete"})
            else:
                return jsonify({"error": "Failed to update task"}), 500

    return jsonify({"error": "Task not found"}), 404


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


# error handling
@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    if TEST:
        app.run(debug=LOCAL_DEPLOY, port=5000)
    else:
        app.run(debug=LOCAL_DEPLOY, port=5000)