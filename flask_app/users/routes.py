########## THIS FILE CONTAINS USER'S BLUEPRINT ##########


from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from flask_app import db, bcrypt
from flask_app.models import User, Post
from flask_app.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flask_app.users.utils import save_picture, send_reset_email


# now create the instance of this blueprint and
# pass name of the blueprint 'users' and name '__name__'

users = Blueprint('users', __name__)


# Now creating routes


# Route for Register
@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # Hash the password
        user = User(username = form.username.data, email = form.email.data, password = hashed_password) # Take user's data
        db.session.add(user) # Add the user to the database
        db.session.commit() # Commit changes to the database
        flash(f'Hi {form.username.data}! Your account is successfully created, Now login Please!!','success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


# Route for Login
@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful! Please check Email and Password', 'danger')
    return render_template('login.html', title='Login', form=form)


# Route for Logout
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


# Route for Account
@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file = image_file, form=form)


# Route for the user_posts
@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date.desc()).paginate(page=page, per_page=5)
    return render_template('user_posts.html', title='Home', posts=posts, user=user)


# Route for reset request
@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user) # send reset email to the user
        flash('Token has been send to your given email', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


# Route for reset password
# takin an active token as an argument
@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('This an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # Hash the password
        user.password = hashed_password
        db.session.commit() # Commit changes to the database
        flash(f'Your password has been successfully updated!','success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

