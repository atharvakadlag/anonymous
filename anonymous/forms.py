from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, HiddenField
from wtforms.validators import Length, DataRequired, Email, EqualTo, ValidationError
from anonymous import models
from anonymous.utils import *


class RegistrationForm(FlaskForm):
    name = StringField(
        'Name:', [DataRequired(), Length(max=120)], default='Anonymous')
    username = StringField('Username:', [DataRequired(), Length(max=120)])
    email = StringField(
        'Email ID:', [DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Password:', [DataRequired(), Length(
        min=6, message='Password to weak, try something stronger.')])
    confirm_password = PasswordField('Confirm Password:', [
                                     DataRequired(), EqualTo('password', message="Paswords don't match.")])
    submit = SubmitField('Submit')

    def validate_username(self, username):
        user = models.Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username not available.')

    def validate_email(self, email):
        email = models.Users.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email already registered, try signing in.')


class LoginForm(FlaskForm):
    email = StringField('Email:', [Length(max=100)])
    password = PasswordField('Password:')
    submit = SubmitField('Submit')

    def validate_email(self, email):
        user = models.Users.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('Email not registered. try signing up.')


class NewMessageForm(FlaskForm):
    receiver = StringField('To:', [DataRequired(), Length(max=100)])
    content = TextAreaField('Message:', [DataRequired()])
    submit = SubmitField('Submit')


class UpdateForm(FlaskForm):
    name = StringField('Name:', [DataRequired(), Length(max=120)])
    username = StringField('Username:', [DataRequired(), Length(max=120)])
    email = StringField(
        'Email ID:', [DataRequired(), Email(), Length(max=100)])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = models.Users.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username not available.')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = models.Users.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError(
                    'Email already registered, try signing in.')


class FilterMessagesForm(FlaskForm):
    msg_filter = SelectField('Filter Messages:', choices=[(
        'all', 'All'), ('sent', 'Sent'), ('received', 'Received')])


class DeleteMessageForm(FlaskForm):
    msg_id = HiddenField("msg_id")
    btnsubmit = SubmitField("Delete")


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password:', [DataRequired()])
    new_password = PasswordField('New Password:', [DataRequired(), Length(
        min=6, message='Password to weak, try something stronger.')])
    confirm_new_password = PasswordField('Confirm Password:', [
        DataRequired(), EqualTo('new_password', message="Paswords don't match.")])
    submit = SubmitField('Change Password')
