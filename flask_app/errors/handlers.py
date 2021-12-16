########## THIS FILE BLUPRINT OF OUR ERROR HANDLERS ##########


from flask import Blueprint, render_template


# now create the instance of this blueprint and
# pass name of the blueprint 'errors' and name '__name__'

errors = Blueprint('errors', __name__)


# Now creating routes


# Error 404 - page not found
@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404

# Error 403 - forbidden
@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

# Error 500 - server issue
@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500