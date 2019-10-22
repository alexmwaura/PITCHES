from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import Required

class PitchForm(FlaskForm):
    title = StringField('Pitch Title',validators = [Required()])
    pitch = TextAreaField("Pitch review",validators =[Required()])
   
    submit = SubmitField("Submit")

class UpdateProfile(FlaskForm):
    bio = TextAreaField("Tell us about you.",validators = [Required()])
    submit = SubmitField('Submit')    

class CommentForm(FlaskForm):
	description = TextAreaField('Add comment',validators=[Required()])
	submit = SubmitField()

class UpvoteForm(FlaskForm):
	submit = SubmitField()


class Downvote(FlaskForm):
	submit = SubmitField()
