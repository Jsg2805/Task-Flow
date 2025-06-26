class User:
    def __init__(self, user_id: str, name: str, email: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.task_list = []
        """
         Initialize a new User object.

    Args:
        user_id, Unique identifier for the user.
        name, Full name of the user.
        email, Email address of the use
        """

    def add_task(self, task):
        self.task_list.append(task)

        """
        Add a task to the user's task list.

    Args:
        task,The task object to be added to the user
        """

    def remove_task(self, task_id):
        self.task_list = [task for task in self.task_list if task.task_id != task_id]
        """
        Remove a task from the user's task list.
        Args:
        task id,The id of the task that has to be removed.
        """

    def view_tasks_by_status(self, status):
        return [task for task in self.task_list if task.status == status]
    
    """
    View the task with it's status.
    Return:
    Retuns the task with their status.
    """
