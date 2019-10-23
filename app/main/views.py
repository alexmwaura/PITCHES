from flask import render_template, request, redirect, url_for, abort
from . import main
from flask_login import login_required, current_user
from ..models import User, PitchCategory, Pitches, Comments
from .forms import UpdateProfile, PitchForm, CommentForm, CategoriesForm
from .. import db, photos


@main.route('/')
def index():
    """View root page function that returns index page and the various news sources"""

    title = 'Welcome to one minute pitches'
    categories = PitchCategory.get_categories()

    return render_template('index.html', title=title, categories=categories)



@main.route('/category/pitch/new/<int:id>', methods=['GET', 'POST'])
@login_required
def new_pitch(id):
    '''
    Function to check Pitches form
    '''
    form = PitchForm()
    category = PitchCategory.query.filter_by(id=id).first()

    if category is None:
        abort(404)

    if form.validate_on_submit():
        actual_pitch = form.content.data
        new_pitch = Pitches(actual_pitch=actual_pitch,
                            user_id=current_user.id, category_id=category.id,upvotes = 0,downvotes = 0)
        new_pitch.save_pitch()
        return redirect(url_for('.category', id=category.id))

    return render_template('new_pitch.html', pitch_form=form, category=category)


@main.route('/category/new',methods=['GET','POST'])
@login_required
def new_category():
	form = CategoriesForm()
	if form.validate_on_submit():
		name = form.name.data
		new_category = PitchCategory(name=name)
		new_category.save_category()
		return redirect(url_for('.new_category'))
	title = 'New Pitch Category'
	return render_template('new_category.html',categories_form=form)	
@main.route('/category/<int:id>')
def category(id):
    '''
    category route function returns a list of pitches in the category chosen
    '''

    category = PitchCategory.query.get(id)
    if category is None:
        abort(404)

    pitches = Pitches.get_pitches(id)
    return render_template('category.html', category=category, pitches=pitches)


@main.route('/pitch/<int:id>', methods=['GET', 'POST'])
@login_required
def single_pitch(id):
    '''
    Function the returns a single pitch for comment to be added
    '''

    pitches = Pitches.query.get(id)

    if pitches is None:
        abort(404)

    comment = Comments.get_comments(id)
    return render_template('pitch.html', pitches=pitches, comment=comment)



@login_required
@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username=uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user)


@main.route('/user/<uname>', methods=['GET', 'POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', uname=user.username))

    return render_template('profile/update.html', form=form)


@main.route('/user/<uname>/update/pic', methods=['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username=uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile', uname=uname))




@main.route('/pitch/new/<int:id>', methods=['GET', 'POST'])
@login_required
def new_comment(id):
    '''
    Function that returns a list of comments for the particular pitch
    '''
    form = CommentForm()
    pitches = Pitches.query.filter_by(id=id).first()

    if pitches is None:
        abort(404)

    if form.validate_on_submit():
        comment_id = form.comment_id.data
        new_comment = Comments(comment_id=comment_id,
                               user_id=current_user.id, pitches_id=pitches.id)
        new_comment.save_comment()
        return redirect(url_for('.category', id=pitches.category_id))

    return render_template('comment.html', comment_form=form)


@main.route('/like/<pitch_id>')
@login_required
def upvote(pitch_id):
    pitches = Pitches.query.get(pitch_id)
    pitches.like_pitch()

    return redirect(url_for('main.single_pitch',id=pitch_id))

@main.route('/dislike/<pitch_id>')
@login_required
def downvote(pitch_id):
    pitches = Pitches.query.get(pitch_id)
    pitches.dislike_pitch()

    return redirect(url_for('main.single_pitch',id = pitch_id))    