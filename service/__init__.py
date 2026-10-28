"""
Package: service
Package for the application models and service routes
This module initializes the Flask app and database
"""
from flask import Flask
from service.common import log_handlers
from service.models import db

# Create Flask application
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "secret-for-devops"

# Initialize SQLAlchemy
db.init_app(app)

with app.app_context():
    db.create_all()

# Set up logging
log_handlers.init_logging(app, "gunicorn.error")

app.logger.info(70 * "*")
app.logger.info("  A C C O U N T S   S E R V I C E   R U N N I N G  ".center(70, "*"))
app.logger.info(70 * "*")

# Import routes and error handlers after app is initialized
from service import routes  # noqa: E402, F401
from service.common import error_handlers  # noqa: E402, F401

