from flask import render_template,request,redirect,url_for,abort
from . import main
from flask_login import login_required
from .forms import PitchForm,UpdateProfile
from .. import db
from ..models import Pitches,User


@main.route('/')
def index():
    '''
    View root page function that returns the indexpage and its data
    '''
    user = User.query.filter_by(username ='uname').first()
    pitches = Pitches.query.all()
    title = 'Welcome to one minute pitches'
    return render_template('index.html',pitches = pitches,title = title)





@main.route('/pitches/<uname>', methods=['GET','POST'])
@login_required
def pitches(uname):
  pitch_form = PitchForm()
  user = User.query.filter_by(username = uname).first()
  if pitch_form.validate_on_submit():
    pitch = Pitches(pitch = pitch_form.pitch.data,user = user)
    db.session.add(pitch)
    db.session.commit()
    return redirect(url_for('main.index'))

  title='Pitches'
  return render_template('pitch.html',title=title,pitch_form=pitch_form)


@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)
    
        

@main.route("/user/<uname>",methods = ["GET","POST"])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname = user.username))

    return render_template('profile/update.html',form = form)


