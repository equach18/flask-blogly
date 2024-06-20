from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)

with app.app_context():
    db.create_all()

@app.route('/')
def homepage():
    """Redirects to list of users."""

    return redirect("/users")

@app.route('/users')
def list_users():
    """Show all users with links for more details. Contains link to add a user"""
    users = User.query.all()
    return render_template("index.html", users=users)

@app.route('/users/new')
def show_form():
    """Shows an add form for users"""
    return render_template("new_user.html")

@app.route('/users/new', methods=['POST'])
def add_user():
    """Processes the add form, adding a new user and goes back to /users"""

    first_name = request.form['first-name']
    last_name = request.form['last-name']
    img_url = request.form['img-url'] or None

    user = User(first_name=first_name, last_name=last_name, image_url=img_url)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user_info(user_id):
    """Shows information about the given user."""
    user = User.query.get_or_404(user_id)
    return render_template('profile.html', user=user)


@app.route('/users/<int:user_id>/edit')
def show_edit(user_id):
    """Shows the edit page for the user. """
    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    """Finalize the edits of a user"""
    user = User.query.get_or_404(user_id)

    user.first_name = request.form['first-name'] or user.first_name
    user.last_name = request.form['last-name'] or user.last_name
    user.img_url = request.form['img-url'] or None

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Finalize the edits of a user"""
    user = User.query.get_or_404(user_id)

    user.query.filter_by(id = user_id).delete()
    
    db.session.commit()

    return redirect('/users')