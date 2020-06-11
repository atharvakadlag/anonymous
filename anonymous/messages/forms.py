from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, HiddenField
from wtforms.validators import Length, DataRequired


class NewMessageForm(FlaskForm):
    receiver = StringField('To:', [DataRequired(), Length(max=100)])
    content = TextAreaField('Message:', [DataRequired()])
    submit = SubmitField('Submit')


class FilterMessagesForm(FlaskForm):
    msg_filter = SelectField('Filter Messages:', choices=[(
        'all', 'All'), ('sent', 'Sent'), ('received', 'Received')])


class DeleteMessageForm(FlaskForm):
    msg_id = HiddenField("msg_id")
    submit = SubmitField("Delete")
