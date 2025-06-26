from models.task import Task
from models.user import User
from utils.exceptions import UserAlreadyExistsError, TaskAlreadyExistsError, EntityNotFoundError
from utils.db import get_connection
from datetime import datetime

class TaskManager:
    def __init__(self):
        """
        Initializes an instance of class task manager.
        Attributes:
        Takes task as dictionary.
        Takes users as dictionary.
        """
       
        pass

    def create_user(self, user_id, name, email):
        conn = get_connection()
        cursor = conn.cursor()
        """
        Defines a function to create user.
        Args: 
        Takes user id.
        Takes Name.
        Takes Email.        
        """
        
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            raise UserAlreadyExistsError("User already exists.")
        """
         The entered user_id is checked in self.users.
        If you try to add a user of same USER ID, 
        An exception, UserAlreadyExistsError is raised
        If no exception is found, a new object is created into the dictionary 'users'.
        """
        
        
        cursor.execute(
            "INSERT INTO users (user_id, uname, uemail) VALUES (%s, %s, %s)",
            (user_id, name, email)
        )
        conn.commit()
        cursor.close()
        conn.close()
        
        return User(user_id, name, email)

    def create_task(self, task_id, title, description, due_date, priority="MEDIUM", user_id=None):
        conn = get_connection()
        cursor = conn.cursor()
        """
        Defines a function to create task.
        Args:
        Takes task_id.
        Takes title.
        Takes description.
        Takes due date.
        Priority is set to "Medium" by default.
        """
        
       
        cursor.execute("SELECT * FROM tasks WHERE task_id = %s", (task_id,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            raise TaskAlreadyExistsError("Task already exists.")
        """
         The entered task.id is checked in tasks.
        If a task of same Task ID is found, TaskAlreadyExistsError exception is raised.
        If not a new object is created in the 'task' dictionary.
        """
        
        
        priority = priority.upper() if priority in [p.upper() for p in Task.VALID_PRIORITIES] else "MEDIUM"
        
        
        cursor.execute(
            """INSERT INTO tasks (task_id, title, description, due_date, priority, status, user_id) 
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (task_id, title, description, due_date, priority, "TO DO", user_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        
       
        return Task(task_id, title, description, due_date, priority)

    def assign_task_to_user(self, task_id, user_id):
        conn = get_connection()
        cursor = conn.cursor()
        """
        Defines a function to assign task to the user
        Args:
        Takes task_id.
        Takes user_id.
        
        """
        
        
        cursor.execute("SELECT * FROM tasks WHERE task_id = %s", (task_id,))
        task_data = cursor.fetchone()
        if not task_data:
            cursor.close()
            conn.close()
            raise EntityNotFoundError("Task not found.")
        """
        If the entered task_id or user_id is not found, an exception EntityNotFoundError is raise.
        Else, Task is assigned to the user or can be vice versa.
        """
        
       
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user_data = cursor.fetchone()
        if not user_data:
            cursor.close()
            conn.close()
            raise EntityNotFoundError("User not found.")
        
        # Update the task with the user_id
        cursor.execute(
            "UPDATE tasks SET user_id = %s WHERE task_id = %s",
            (user_id, task_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

    def list_all_tasks(self):
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT t.task_id, t.title, t.description, t.due_date, t.priority, t.status, 
                   t.user_id, u.uname
            FROM tasks t
            LEFT JOIN users u ON t.user_id = u.user_id
        """)
        
        tasks = []
        for row in cursor.fetchall():
            task_id, title, description, due_date, priority, status, user_id, user_name = row
            task = Task(task_id, title, description, str(due_date), priority, status, user_id=user_id)
            tasks.append(task)
        
        cursor.close()
        conn.close()
        return tasks
    """
    Defines a task to return all the task from the tasks dictionary.
    Return:
    Returns all the task in the tasks dictionary
    """

    def list_tasks_by_user(self, user_id):
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            raise EntityNotFoundError("User not found.")
        
        # Get tasks for the user
        cursor.execute("""
            SELECT task_id, title, description, due_date, priority, status, user_id
            FROM tasks WHERE user_id = %s
        """, (user_id,))
        
        tasks = []
        for row in cursor.fetchall():
            task_id, title, description, due_date, priority, status, user_id = row
            task = Task(task_id, title, description, str(due_date), priority, status, user_id=user_id)
            tasks.append(task)
        
        cursor.close()
        conn.close()
        return tasks
    """
     Defines a function to list tasks by users
    Args:
    Takes user_id
    Return:
    Returns the task according to the user id.
    """

    def list_tasks_by_status(self, status):
        conn = get_connection()
        cursor = conn.cursor()
        """
          Defines a function to list tasks by status
    Args:
    Takes status
    Return:
    Runs a loop which iterates through the tasks dictionary and returns their status.
        """
        
       
        status = status.upper()
        if status not in [s.upper() for s in Task.VALID_STATUSES]:
            cursor.close()
            conn.close()
            return []
        
        # Get tasks with the specified status
        cursor.execute("""
            SELECT t.task_id, t.title, t.description, t.due_date, t.priority, t.status, 
                   t.user_id, u.uname
            FROM tasks t
            LEFT JOIN users u ON t.user_id = u.user_id
            WHERE t.status = %s
        """, (status,))
        
        tasks = []
        for row in cursor.fetchall():
            task_id, title, description, due_date, priority, status, user_id, user_name = row
            task = Task(task_id, title, description, str(due_date), priority, status, user_id=user_id)
            tasks.append(task)
        
        cursor.close()
        conn.close()
        return tasks

    def update_task(self, task_id, **kwargs):
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if task exists
        cursor.execute("SELECT * FROM tasks WHERE task_id = %s", (task_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            raise EntityNotFoundError("Task not found.")
            
        # Build SET clause for SQL update
        allowed_fields = {'title', 'description', 'due_date', 'priority', 'status', 'user_id'}
        set_clauses = []
        params = []
        
        for key, value in kwargs.items():
            if key in allowed_fields:
                # Special handling for priorities and statuses
                if key == 'priority' and isinstance(value, str):
                    value = value.upper()
                    if value not in [p.upper() for p in Task.VALID_PRIORITIES]:
                        continue
                elif key == 'status' and isinstance(value, str):
                    value = value.upper()
                    if value not in [s.upper() for s in Task.VALID_STATUSES]:
                        continue
                
                set_clauses.append(f"{key} = %s")
                params.append(value)
        
        if set_clauses:
            # Execute the update
            sql = f"UPDATE tasks SET {', '.join(set_clauses)} WHERE task_id = %s"
            params.append(task_id)
            cursor.execute(sql, params)
            conn.commit()
            
        cursor.close()
        conn.close()

    def delete_task(self, task_id):
        conn = get_connection()
        cursor = conn.cursor()
        """
        A function to delete tasks is created.
        Args:
        Takes in task_id. 
        """
        # Check if task exists
        cursor.execute("SELECT * FROM tasks WHERE task_id = %s", (task_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            raise EntityNotFoundError("Task not found.")
        """
        If task_id is not in the tasks dictionary,
        An exception EntityNotFoundError is raised
        """
        
        # Delete the task
        cursor.execute("DELETE FROM tasks WHERE task_id = %s", (task_id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        

    def get_task(self, task_id):
        """
        Defines a function get_task
    Args:
    Taks id
    Return:
    Returns the corresponding task from the tasks dictionary
        """
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT t.task_id, t.title, t.description, t.due_date, t.priority, t.status, 
                   t.user_id, u.uname
            FROM tasks t
            LEFT JOIN users u ON t.user_id = u.user_id
            WHERE t.task_id = %s
        """, (task_id,))
        
        row = cursor.fetchone()
        if not row:
            cursor.close()
            conn.close()
            return None
            
        task_id, title, description, due_date, priority, status, user_id, user_name = row
        task = Task(task_id, title, description, str(due_date), priority, status, user_id=user_id)
        
        cursor.close()
        conn.close()
        return task
        
    def get_user(self, user_id):
        """Get a single user by ID"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT user_id, uname, uemail FROM users WHERE user_id = %s", (user_id,))
        row = cursor.fetchone()
        
        if not row:
            cursor.close()
            conn.close()
            return None
            
        user_id, name, email = row
        user = User(user_id, name, email)
        
       
        cursor.execute("SELECT task_id, title, description, due_date, priority, status FROM tasks WHERE user_id = %s", (user_id,))
        for task_row in cursor.fetchall():
            task_id, title, description, due_date, priority, status = task_row
            task = Task(task_id, title, description, str(due_date), priority, status, user_id=user_id)
            user.add_task(task)
            
        cursor.close()
        conn.close()
        return user

    def get_all_users(self):
        """Get all users from the database"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT user_id, uname, uemail FROM users")
        users = []
        
        for row in cursor.fetchall():
            user_id, name, email = row
            user = User(user_id, name, email)
            users.append(user)
            
        cursor.close()
        conn.close()
        return users

    
    def update_task_status(self, task_id, new_status):
        """Update a task's status"""
        new_status = new_status.upper()
        if new_status not in Task.VALID_STATUSES:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(Task.VALID_STATUSES)}")
        
        return self.update_task(task_id, status=new_status)
        
    def update_task_priority(self, task_id, new_priority):
        """Update a task's priority"""
        new_priority = new_priority.upper()
        if new_priority not in Task.VALID_PRIORITIES:
            raise ValueError(f"Invalid priority. Must be one of: {', '.join(Task.VALID_PRIORITIES)}")
            
        return self.update_task(task_id, priority=new_priority)
