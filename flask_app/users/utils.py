import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flask_app import mail


# Define a function for save pictures and returns the file name and extension
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.split(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    # resize image, before saving
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    # sve image
    i.save(picture_path)

    return picture_fn

# Define a function for sending email
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', recipients=[user.email], sender='noreply@gmail.com>')
    msg.body = f'''To reset your password, visite the following link:
    {url_for('users.reset_token', token=token, _external=True)}

    If you did not make this request then simply ignore this email and no changes will be made.
    '''
    mail.send(msg)