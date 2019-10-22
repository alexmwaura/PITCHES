from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import Required

class PitchForm(FlaskForm):

    content = TextAreaField('YOUR PITCH')
    submit = SubmitField('Create Pitch')

class UpdateProfile(FlaskForm):
    bio = TextAreaField("Tell us about you.",validators = [Required()])
    submit = SubmitField('Submit')    

class CommentForm(FlaskForm):

    comment_id = TextAreaField('Comment', validators=[Required()])
    submit = SubmitField('Sumbit') 

class CategoriesForm(FlaskForm):
    name = TextAreaField('Write your comment')
    submit = SubmitField('Submit')



