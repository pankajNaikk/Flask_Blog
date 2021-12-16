########## THIS FILE ONLY FOR RUN THE APPLICATION ##########



# Import the app from the package 'flask_app'
from flask_app import create_app

# create app instance
app = create_app()

# Run the app
if __name__ == '__main__':
    app.run(debug=True)