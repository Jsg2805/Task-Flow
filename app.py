from flask import Flask
from routers.task_router import task_bp
from routers.user_router import user_bp

app = Flask(__name__)


app.register_blueprint(task_bp, url_prefix='/tasks')

"""
Registers task-related routes under the '/tasks' URL prefix.
"""
app.register_blueprint(user_bp, url_prefix='/users')

"""
Registers user-related routes under the '/users' URL prefix.
"""
@app.route("/")
def home():
    """
    API is running.
    """
    return {"message": "Flask Task Management API is running!"}
"""
Returns the given message.
"""

if __name__ == "__main__":
   
    from utils.db import db_creation
    db_creation()
    
    app.run(debug=True)
    """
    Initializes the database tables
    Start Flask Development Server
    """
