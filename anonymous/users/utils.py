from anonymous import db, models, mail
from flask import request, url_for, current_app
from flask_mail import Message
from urllib.parse import urlparse, urljoin
from passlib.hash import sha256_crypt
encrypt = sha256_crypt.encrypt
verify = sha256_crypt.verify


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Reset Password for ANON-AK', sender='anon.ak.herokuapp@gmail.com', recipients=[user.email])
    msg.body = f'''
    Use the below given link for reseting your password:
    {url_for('users.reset_password', token=token, _external=True)}
    Ignore this message if the request was not made by you.
    '''
    mail.send(msg)


