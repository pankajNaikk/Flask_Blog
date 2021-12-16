########## THIS FILE CONTAINS HOME PAGE AND ABOUT PAGE BLUEPRINT ##########

from flask import render_template, request, Blueprint
from flask_app.models import Post

# now create the instance of this blueprint and
# pass name of the blueprint 'posts' and name '__name__'

main = Blueprint('main', __name__)


# Now creating routes

# Route for Home
@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date.desc()).paginate(page=page, per_page=5) # grab all the posts from the database
    return render_template('home.html', title='Home', posts=posts)

# Route for About
@main.route("/about")
def about():
    return render_template('about.html', title='About')
