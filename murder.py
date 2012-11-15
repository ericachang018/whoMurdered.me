from flask import Flask, render_template, redirect, request, session, url_for, escape, g, flash
import model
from model import db_session, User
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
def login():
	return render_template('login.html')


@app.route('/login', methods = ['POST'])
def authenticate():
	email = request.form['email']
	password = request.form ['password']
	print email, password
	try:
		user = db_session.query(User).filter_by(email=email, password=password).one() 
		session['user_id'] = user.id
		return redirect( url_for("current_game") )
	except: 
		flash('Invalid email or password', 'error')
		return redirect(url_for("login"))


@app.route('/logout', methods = ['POST'])
def logout():
	session.pop("user_id", None)
	flash('This message has self destructed you are now free to rome across the country')
	return redirect(url_for("login"))



@app.route('/signup', methods = ['GET'])
def signup(): 
	return render_template('signup.html')

@app.route('/signup', methods = ['POST'])
def register():
	email = request.form['email']
	password = request.form['password']
	confirm_password = request.form['password_confirmed']

	if password != confirm_password:
		flash ('Passwords did not match please try again')
		redirect(url_for('signup'))

	existing = db_session.query(User).filter_by(email= email).first
	print existing 
	if existing: 
		flash ('Email is already in use please try again')
		redirect(url_for('signup'))
	else:
		new_user = User(email=email, password=password, name=name )
		db_session.add(new_user) 
		db_session.commit
		db_session.refresh(new_user)
		session['user_id'] = user.id
	return redirect(url_for('current_game'))

# need to fix the error that says view function did not return a response
# currently in this state it will skip over everything and return the current game
	
	

@app.route('/current_game')
def current_game():
	return render_template('current_game.html')


@app.route('/make_game', methods = ['POST'])
def make_game():
	pass
# 	return render_template('make_game.html')
# # this will redirect to the form to make a game create a html page

# @app.route('/select_game')
# def select_game():
# 	game_list = mode.session.query(model.Game).all()
# 	return render_template('select_game.html', games=game_list)
# this page will redirect to the select game page and desplay all games 
# from the games table 


# @app.teardown_request
# def shutdown_session(exception = None):
# 	db_session.remove()


if __name__ == '__main__':
	app.run() 