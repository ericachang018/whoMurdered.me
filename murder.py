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
	"""this method checks to see if the user is in the database and creates a session 
	for the user and directs them to their current game else it will flash an error"""

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
	"""this method logs the user out and ends their session. Redirects the user to the log in page"""
	session.pop("user_id", None)
	flash('This message has self destructed you are now free to rome across the country')
	return redirect(url_for("display_login"))


@app.route('/signup', methods = ['GET'])
def display_signup(): 
	return render_template('signup.html')

@app.route('/signup', methods = ['POST'])
def register():
	""" this method writes new unique user information into the users table in the database. then 
	creates a new session and directs them to the current game."""
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
	

@app.route('/current_game', methods = ['GET'])
def current_game():
# TO DO! ERICA 	3
	"""This method will display the current game. So It needs to look at the session find out 
	which user is currently logged in and what their current mission / challenge is and display_login
	the current challenege """
	return render_template('current_game.html')

@app.route('/current_game', methods = ['POST'])	
# TO DO ! ERICA  3
def check_solution():
	"""this method will check the solution if correct it will up date the session record to 
	show the user on the new challenge and display the next challengeif the solution is wrong 
	it will flash an error message."""
	return render_template('current_game.html')


@app.route('/make_games', methods = ['GET'])
# TO DO ERICA! 1
def display_make_game():
	"""this method will display the make game form. """
 
	return render_template('make_games.html', games = games)

@app.route('/make_games', methods = ['POST'])
# TO DO ERICA 1. 
def create_games(): 
	"""this method will write to the game table."""  
	return redirect(url_for('display_make_game'))


@app.route('/make_challenge', methods = ['GET'])
# TO DO ERICA 1. 
def display_make_challenge():
	"""this method will display the make challenge form"""
	return render_template('make_challenge.html')

@app.route('/make_challenge', methods = ['POST'])
# TO DO ERICA 2
def next_challenege():
	""" if the user CLICKS on +1 CHALLENEGE BUTTON this method will WRITE the challenge to the
	challenge table in the database and display a new blank form till user presses submit."""
	return render_template('make_challenge.html')
	

@app.route('/make_challenge', methods = ['POST'])
# TO DO ERICA 2
def finish_game_creation():
	"""this method will run when user CLICKS SUBMIT BUTTON redirect users to select games page 
	when they are done creating their game. """
	pass

@app.route('/select_games', methods = ['GET'])
# TO DO ERICA 1
def select_game():
	"""This method will query the database for all the games avaliable to play"""
	games = db_session.query(Game).all() 
	return render_template('select_games.html', games = games)


@app.route('/status', methods = ['GET'])
def display_status():
	""" this method will display the all the games the user is currently playing and which 
	one is active. The user should be able to toggle between the other games to switch their 
	current active game."""
	status = db_session.query(Session).all()
	return render_template('status.html', status = status)

# @app.teardown_request
# def shutdown_session(exception = None):
# 	db_session.remove()


if __name__ == '__main__':
	app.run() 