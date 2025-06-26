from datetime import datetime

class Task:
    """
    Represents a task with status, priority, assignment, and due date.    
    """
    VALID_STATUSES = ["TO DO", "IN PROGRESS", "DONE"]
    VALID_PRIORITIES = ["LOW", "MEDIUM", "HIGH"]

    def __init__(self, task_id, title, description, due_date, priority="MEDIUM", status="TO DO", assigned_to=None, user_id=None):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.user_id = user_id
        """
        Args:
        task_id, Unique identifier for the task.
        title ,Title of the task.
        description,Detailed description of the task.
        due_date, Due date of the task in 'YYYY-MM-DD' format.
        priority , Priority level of the task ('High', 'Medium', or 'Low').
        Default set to 'Medium'.
        
        """

        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Due date must be in YYYY-MM-DD format.")
        """
        Raises:
        Raises a ValueError, If the due date is not in the 'YYYY-MM-DD' format
        
        """        
        self.due_date = due_date
        self.priority = priority if priority in self.VALID_PRIORITIES else "MEDIUM"
        self.status = status if status in self.VALID_STATUSES else "TO DO"
        self.assigned_to = assigned_to

    def update_status(self, new_status):
        """
        Update the status of the task.

    Args:
        new_status  The new status to set for the task. Must be one of the valid statuses
                          defined in VALID_STATUSES ('To Do', 'In Progress', 'Done'  ) 
        """


        if new_status in self.VALID_STATUSES:
            self.status = new_status
        else:
            raise ValueError("Invalid status")
        """
        Raises:
       Raises ValueError ,If the provided status is not in the list of valid statuses
        
        """

    def update_priority(self, new_priority):
        """
        Update the priority level of the task.

    Args:
        new_priority, The new priority to set for the task. Must be one of the valid
        priorities defined in VALID_PRIORITIES (e.g., 'High', 'Medium', 'Low')
        """


        if new_priority in self.VALID_PRIORITIES:
            self.priority = new_priority
        else:
            raise ValueError("Invalid priority")
        """
        Raises ValueError If the provided priority is not in the list of valid priorities.
        """

    def assign_to(self, user):
        self.assigned_to = user

    def display_info(self):
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "assigned_to": self.assigned_to.name if self.assigned_to else None,
            "user_id": self.user_id,
            "status": self.status,
            "priority": self.priority,
            "due_date": self.due_date

        }
    """
Defines a display_info function which returns a str value.
Displays all the info of the Task.
"""

    def to_dict(self):
        """Convert task object to dictionary for API responses"""
        return self.display_info()
