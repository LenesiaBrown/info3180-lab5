from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed

class MovieForm(FlaskForm):
    title = StringField('Movie Title', validators=[InputRequired()])      
    description = TextAreaField('Summary of Movie', validators=[InputRequired()])
    poster = FileField('Movie Poster Image', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Only Image Files!')
                                         ])
    submit = SubmitField('Upload')