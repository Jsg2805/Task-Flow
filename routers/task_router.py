from flask import Blueprint, request
from manager.task_manager import TaskManager
from utils.exceptions import EntityNotFoundError

task_bp = Blueprint('task_routes', __name__)
"""
 Blueprint for task related API.

"""
tm = TaskManager() 
"""
Creates a single instance to manages task operations
"""                 

@task_bp.route('/', methods=['POST'])
def create_task():
    data = request.get_json()
    try:
        task = tm.create_task(
            data["task_id"], 
            data["title"], 
            data["description"],
            data["due_date"], 
            data.get("priority", "MEDIUM"),
            data.get("user_id")
        )
        if "user_id" in data and data["user_id"]:
            try:
                tm.assign_task_to_user(data["task_id"], data["user_id"])
            except Exception as e:
                # Still return success for task creation even if assignment fails
                return {"message": f"Task created but assignment failed: {str(e)}"}, 201
        return {"message": "Task created successfully", "task": task.to_dict()}, 201
    except Exception as e:
        return {"error": str(e)}, 400
    """
    Creates new task.
    Returns
    201: When task is created successsfully
    400: bad request when a creation failure occurs.

    """


@task_bp.route('/', methods=['GET'])
def list_tasks():
    status = request.args.get('status')
    user_id = request.args.get('user_id')
    
    try:
        if status:
            tasks = tm.list_tasks_by_status(status)
        elif user_id:
            tasks = tm.list_tasks_by_user(user_id)
        else:
            tasks = tm.list_all_tasks()
        
        return {"tasks": [t.to_dict() for t in tasks]}, 200
    except Exception as e:
        return {"error": str(e)}, 400
    """
    Retrieves all the tasks.
    Returns:
    200: list of all task.
    400: Error occured, invalid input.

    """


@task_bp.route('/<task_id>', methods=['GET'])
def get_task(task_id):
    try:
        task = tm.get_task(task_id)
        if not task:
            return {"error": "Task not found"}, 404
        return {"task": task.to_dict()}, 200
    except Exception as e:
        return {"error": str(e)}, 400
    """
    Gets a task according to the given id.
    Returns:
    200: when a task is found
    404: Taks is not found
    400:Exception Errors
    
    """

@task_bp.route('/<task_id>/status', methods=['PUT'])
def update_status(task_id):
    data = request.get_json()
    try:
        tm.update_task_status(task_id, data["status"])
        return {"message": "Status updated successfully"}, 200
    except Exception as e:
        return {"error": str(e)}, 400
    """
    Updates the task.
    Returns:
    200: Status updated
    400:Invalid data
    
    """

@task_bp.route('/<task_id>/priority', methods=['PUT'])
def update_priority(task_id):
    data = request.get_json()
    try:
        tm.update_task_priority(task_id, data["priority"])
        return {"message": "Priority updated successfully"}, 200
    except Exception as e:
        return {"error": str(e)}, 400
    """
    Updates the task priority.
    Returns:
    200: Task priority has been updated
    400: Error has occured    
    """

@task_bp.route('/<task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    try:
        tm.update_task(task_id, **data)
        return {"message": "Task updated successfully"}, 200
    except Exception as e:
        return {"error": str(e)}, 400
    """
    Updates tasks
    Returns:
    200: Task is updated
    400: Invalid input

    """


@task_bp.route('/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        tm.delete_task(task_id)
        return {"message": "Task deleted successfully"}, 200
    except EntityNotFoundError as e:
        return {"error": str(e)}, 404
    except Exception as e:
        return {"error": str(e)}, 400
    """
    Task deletion
    Returns:
    200: Task has been deleted
    404: Task not found
    400: Deletion failed 
    
    """
