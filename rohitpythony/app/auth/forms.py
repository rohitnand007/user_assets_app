from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from ..models import User


class RegistrationForm(FlaskForm):
    """
    Form for users to create new account
    """
    # email = StringField('Email', validators=[DataRequired(), Email()])

    name = StringField('name', validators=[DataRequired()])
    department = StringField('department', validators=[DataRequired()])
    position = StringField('position', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
                                        DataRequired(),
                                        EqualTo('confirm_password')
                                        ])
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Register')

    def validate_username(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('Username is already in use.')


class LoginForm(FlaskForm):
    """
    Form for users to login
    """
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')