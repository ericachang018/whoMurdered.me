from flask import Flask, render_template, redirect, request, session, url_for, escape, g, flash
import model
from model import db_session, User, Game, Challenge
from flask.ext.login import LoginManager


app = Flask(__name__) 
app.debug = True

# login_manager = LoginManager()
# login_manager.setup_app(app)

app.secret_key = 'super0secret0key'


@app.route('/')
def index():
	return render_template('whokilledme.html')


@app.route("/login", methods=["GET"])
def display_login():
	return render_template('login.html')


@app.route('/login', methods = ['POST'])
def authenticate():
	email = request.form['email']
	password = request.form ['password']
	try:
		user = db_session.query(User).filter_by(email=email, password=password).one() 
		session['user_id'] = user.id
		return redirect( url_for("current_game") )
	except: 
		flash('Invalid email or password', 'error')
		return redirect(url_for("display_login"))


@app.route('/logout', methods = ['POST'])
def logout():
	session.pop("user_id", None)
	flash('This message has self destructed you are now free to rome across the country')
	return redirect(url_for("display_login"))


@app.route('/signup', methods = ['GET'])
def display_signup(): 
	return render_template('signup.html')

@app.route('/signup', methods = ['POST'])
def register():
	name = request.form['name']
	email = request.form['email']
	password = request.form['password']
	confirm_password = request.form['password_confirmed']

	if password != confirm_password:
		flash ('Passwords did not match please try again')
		return redirect(url_for('display_signup'))

	existing = db_session.query(User).filter_by(email= email).first()
	print existing 
	if existing: 
		flash ('Email is already in use please try again')
		return redirect(url_for('display_signup'))
	else: 
		new_user = User(email=email, password=password, name=name )
		db_session.add(new_user) 
		db_session.commit()
		db_session.refresh(new_user)
		user = db_session.query(User).filter_by(email=email, password=password).one()
		session['user_id'] = user.id
	return redirect(url_for('current_game'))
	

@app.route('/current_game')
def current_game():
	return render_template('current_game.html')


@app.route('/make_games', methods = ['GET'])
def display_make_game():
	games = db_session.query(Game).all() 
	return render_template('make_games.html', games = games)

@app.route('/make_games', methods = ['POST'])
def create_games():
	return redirect(url_for('display_make_game'))

# 	return render_template('make_game.html')
# # this will redirect to the form to make a game create a html page

@app.route('/select_games', methods = ['GET'])
def select_game():
	return render_template('select_games.html')

@app.route('/leaderboard', methods = ['GET'])
def display_leaderboard():
	return render_template('leaderboard.html')

@app.route('/status', methods = ['GET'])
def display_status():
	return render_template('status.html')

# @app.teardown_request
# def shutdown_session(exception = None):
# 	db_session.remove()


if __name__ == '__main__':
	app.run() 