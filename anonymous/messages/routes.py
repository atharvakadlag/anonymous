from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user
from anonymous import db, models
from anonymous.messages import forms



messages = Blueprint('messages', __name__)


@messages.route('/new_message', methods=['POST', 'GET'])
def new_message():
    form = forms.NewMessageForm()

    # check if referal
    u = request.args.get('u', None)
    if u:
        form.receiver.data = u

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
        return redirect(url_for('main.home'))
    return render_template('new_message.html', form=form)