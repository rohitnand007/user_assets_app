from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired

from ..models import Asset


class AssetForm(FlaskForm):
    """
    Form for user to add to edit his Assets
    """
    comments = StringField('Comments', validators=[DataRequired()])
    submit = SubmitField('Submit')
