#!/usr/bin/python3
"""
app module for the Flask application
"""

from flask import Flask, jsonify
from flask_cors import CORS
from os import getenv

from api.v1.views import app_views
from models import storage

# Initialize Flask app
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

# Register the blueprint for views
app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(exception):
    """
    Teardown method to close storage session
    """
    storage.close()

@app.errorhandler(404)
def handle_404(exception):
    """
    Custom handler for 404 errors
    :return: JSON response with 404 status code
    """
    data = {"error": "Not found"}
    resp = jsonify(data)
    resp.status_code = 404
    return resp

if __name__ == "__main__":
    # Retrieve host and port from environment variables, or use default values
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)

