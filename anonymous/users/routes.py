from flask import Blueprint
from flask import redirect, url_for, render_template
from flask import request, flash, abort
from flask_login import login_user, login_required, current_user, logout_user
from anonymous import db, models
from anonymous.users import forms
from anonymous.messages.forms import DeleteMessageForm, FilterMessagesForm
from anonymous.users.utils import verify, encrypt, is_safe_url, send_reset_email

users = Blueprint('users', __name__)


@users.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = models.Users.query.filter_by(email=form.email.data).first()
        if verify(form.password.data, user.password):
            login_user(user)
            flash(f'Login Successfull as {user.name}', 'success')
            next = request.args.get('next')
            if not is_safe_url(next):
                return abort(400)
            return redirect(next or url_for('main.home'))
        else:
            flash('Login Unsuccessfull, check email and password', 'danger')
    return render_template('login.html', form=form)


@users.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        user = models.Users(name=form.name.data, username=form.username.data,
                            email=form.email.data, password=encrypt(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash('Registration Successfull', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account/update_account", methods=['POST', 'GET'])
@login_required
def update_account():
    form = forms.UpdateForm()

    if request.method == "GET":
        form.name.data = current_user.name
        form.username.data = current_user.username
        form.email.data = current_user.email

    if request.method == "POST":
        if form.validate_on_submit():
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.name = form.name.data
            db.session.commit()
            flash("Account updated successfully", "success")
            form.name.data = current_user.name
            form.username.data = current_user.username
            form.email.data = current_user.email

    return render_template('update_account.html', form=form)


@users.route("/account/my_messages", methods=['POST', 'GET'])
@login_required
def user_messages():
    form = FilterMessagesForm()
    delete_message_form = DeleteMessageForm()

    messages = models.Messages.query.filter(
        (models.Messages.receiver == current_user.username) | (models.Messages.user_id == current_user))

    if form.msg_filter.data == "sent":
        messages = models.Messages.query.filter_by(user_id=current_user.id)
    if form.msg_filter.data == "received":
        messages = models.Messages.query.filter_by(
            receiver=current_user.username)

    if request.method == "POST":
        msg_id = delete_message_form.msg_id.data
        message = models.Messages.query.get(msg_id)
        if message:
            db.session.delete(message)
            db.session.commit()
            flash(f"Message deleted sucessfully", "success")

    return render_template('user_posts.html', form=form, delete_message_form=delete_message_form, messages=messages)



@users.route('/account/change_password', methods=['POST', 'GET'])
@login_required
def change_password():
    form = forms.ChangePasswordForm()
    if form.validate_on_submit():
        if verify(form.current_password.data, current_user.password):
            current_user.password = encrypt(form.new_password.data)
            db.session.commit()
            flash("Password change sucessfully", "success")
        else:
            flash("Wrong password.", "danger")

    return render_template('change_password.html', form=form)


@users.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = models.Users.verify_reset_token(token)
    if not user:
        flash('Invalid or Expired Token, please regenerate the token', 'danger')
        return redirect(url_for('users.reset_request'))
    form = forms.ResetPasswordForm()
    if form.validate_on_submit():
        user.password = encrypt(form.new_password.data)
        db.session.commit()
        flash("Password reset sucessfull, Proceed to login", "success")
        return redirect(url_for('users.login'))
    return render_template('reset_password.html', form=form)


@users.route('/reset_request', methods=['POST', 'GET'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    form = forms.ResetRequestForm()
    if form.validate_on_submit():
        user = models.Users.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Check your mail for further instructions', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', form=form)
