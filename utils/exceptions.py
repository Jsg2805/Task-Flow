class UserAlreadyExistsError(Exception):
    """    Creating an exception for the conditon when the user id of an existing user is added again."""
    pass

class TaskAlreadyExistsError(Exception):
    """
    Creating an already exsisting task.
    """
    pass

class EntityNotFoundError(Exception):
    """An exception to be raised when the entity is not found."""
    pass
