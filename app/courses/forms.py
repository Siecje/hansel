from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField,\
    TextAreaField, SelectField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from .models import Course


class CourseForm(Form):
    name = StringField('Name', validators=[Required()])
    submit = SubmitField('Create Course')


class AssignmentForm(Form):
    name = StringField('Name', validators=[Required()])
    submit = SubmitField('Add Assignment')
