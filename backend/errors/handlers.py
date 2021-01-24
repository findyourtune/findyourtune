from flask import Blueprint, render_template, jsonify, request
from flask import jsonify


errors = Blueprint('errors', __name__)

# TODO: 404,, 403, 500 errorhandlers not being used right now,
# All errors will use the InvalidAPIUsage custom exception for now...
@errors.app_errorhandler(404)
def page_not_found(e):
    return handle_invalid_usage(e)

# @errors.app_errorhandler(403)
# def error_403(error):
#     return render_template('errors/403.html'), 403


# @errors.app_errorhandler(500)
# def error_500(error):
#     return render_template('errors/500.html'), 500

# Custom Exception so we can return messages with non 2xx status codes
class InvalidAPIUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


# Custom error handler for custom exception
@errors.app_errorhandler(InvalidAPIUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response