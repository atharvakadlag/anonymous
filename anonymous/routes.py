from flask import redirect, url_for, render_template
from flask import session, request, flash, abort, request
from flask_login import login_user, login_required, current_user, logout_user
from anonymous import app, forms, db, models
from anonymous.utils import *
import time
c = {
    "RED": "\033[1;31m",
    "BLUE": "\033[1;34m",
    "CYAN": "\033[1;36m",
    "GREEN": "\033[0;32m",
    "RESET": "\033[0;0m",
    "BOLD": "\033[;1m",
    "REVERSE": "\033[;7m"
}


def cprint(string, color):
    print(c[color], string, c["RESET"])


@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    messages = models.Messages.query.order_by(models.Messages.id.desc()).paginate(page=page, per_page=5)
    return render_template('index.html', messages=messages)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = models.Users.query.filter_by(email=form.email.data).first()
        if verify(form.password.data, user.password):
            login_user(user)
            flash(f'Login Successfull as {user.name}', 'success')
            next = request.args.get('next')
            if not is_safe_url(next):
                return abort(400)
            return redirect(next or url_for('home'))
        else:
            flash('Login Unsuccessfull, check email and password', 'danger')
    return render_template('login.html', form=form)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        user = models.Users(name=form.name.data, username=form.username.data,
                            email=form.email.data, password=encrypt(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash('Registration Successfull', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account/update_account", methods=['POST', 'GET'])
@login_required
def update_account():
    form = forms.UpdateForm()
    filter_form = forms.FilterMessagesForm()

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


@app.route("/account/my_messages", methods=['POST', 'GET'])
@login_required
def user_messages():
    form = forms.FilterMessagesForm()
    delete_message_form = forms.DeleteMessageForm()

    messages = models.Messages.query.filter(
        (models.Messages.receiver == 'tim') | (models.Messages.user_id == 2))

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


@app.route('/new_message', methods=['POST', 'GET'])
def new_message():
    form = forms.NewMessageForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            user_id = current_user.id
        else:
            user_id = 1
        message = models.Messages(
            receiver=form.receiver.data, content=form.content.data, user_id=user_id)
        db.session.add(message)
        db.session.commit()
        flash('Message posted successfully.', 'success')
        return redirect(url_for('home'))
    return render_template('new_message.html', form=form)


@app.route('/account/change_password', methods=['POST', 'GET'])
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


@app.cli.command("init_db")
def init_db():
    """Initialise the database"""
    db.drop_all()
    db.create_all()
    user = models.Users(name='Anonymous', username='anonymous', email='anonymous@anonymous.anonymous',
                        password='$5$rounds=535000$qm4TQTpM76vBksEs$d5T8pZFVkoMlmFOC.yxoVd2DIDDd2Z.ZUC6qw/pmup4')
    db.session.add(user)
    db.session.commit()
