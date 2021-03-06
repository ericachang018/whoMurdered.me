from flask import Flask, render_template, redirect, request, session, url_for, escape, g, flash
import model
from model import db_session, User, Game, Challenge, Session
from flask.ext.login import LoginManager

import forms


app = Flask(__name__) 
app.debug = True
CSRF_ENABLED=False
app.config.from_object(__name__)

# login_manager = LoginManager()
# login_manager.setup_app(app)

app.secret_key = 'super0secret0key'

@app.route('/', methods=["GET"])
def index():
  return render_template('whokilledme.html')
  
@app.route('/', methods=["POST"])
def redirect_login():
  return url_for(display_login)


@app.route("/login", methods=["GET"])
def display_login():
  return render_template('login.html')

@app.route('/login', methods=['POST'])
def authenticate():
  """this method checks to see if the user is in the database and creates a session 
  for the user and directs them to their current game else it will flash an error"""

  email = request.form['email']
  password = request.form ['password']
  try:
    user = db_session.query(User).filter_by(email=email, password=password).one() 
    session['user_id']=user.id
    return redirect(url_for("current_game"))
  except: 
    flash('Invalid email or password', 'error')
    return redirect(url_for("display_login"))


@app.route('/logout', methods=['POST'])
def logout():
  """this method logs the user out and ends their session. Redirects the user to the log in page"""
  session.pop("user_id", None)
  flash('This message has self destructed you are now free to roam across the country')
  return redirect(url_for("display_login"))


@app.route('/signup', methods=['GET'])
def display_signup():
  form = forms.RegForm()
  return render_template('signup.html', form=form)

@app.route('/signup', methods=['POST'])
def register():
  """ this method writes new unique user information into the users table in the database. then 
  creates a new session and directs them to the current game."""
  form = forms.RegForm()
# if not form. is where the magic happends in flask-wtforms 
  if not form.validate_on_submit():
    print form.errors
    return render_template("signup.html", form=form)
 
  name = form.name.data
  email = form.email.data
  password = form.password.data
  latitude = float(form.lat.data)
  longitude = float(form.long.data)
# from here to the comment above this is flask-wtf library. http://flask.pocoo.org/docs/patterns/wtforms/ to read more about this
  existing = db_session.query(User).filter_by(email=email).first()
  print existing 
  if existing: 
    flash ('Email is already in use please try again')
    return redirect(url_for('display_signup'))
  else: 
    new_user = User(email=email, password=password, name=name, longitude=longitude, latitude=latitude)
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)
    user = db_session.query(User).filter_by(email=email, password=password).one()
    session['user_id'] = user.id
  return redirect(url_for('current_game'))
  

@app.route('/current_game', methods=['GET'])
def current_game():
# TO DO! ERICA  3
  """This method will display the current game. So It needs to look at the session find out 
  which user is currently logged in and what their current mission / challenge is and display_login
  the current challenege """
  
  # name=db_session.query(User).filter_by(name) 
  # HOW DO I DISPLAY A NAME FROM THE DATABASE? AND HOW CAN I DISPLAY MY CHALLENEGE?

  return render_template('current_game.html')

@app.route('/current_game', methods=['POST']) 
# TO DO ! ERICA  3
def check_solution():
  """this method will check the solution if correct it will up date the session record to 
  show the user on the new challenge and display the next challengeif the solution is wrong 
  it will flash an error message."""
  return render_template('current_game.html')


@app.route('/make_games', methods=['GET'])
def display_make_game():
  """This method will display the make game form. """
  return render_template('make_games.html')


@app.route('/make_games', methods=['POST']) 
def create_games(): 
  """this method will write to the game table.""" 
  game_title = request.form['game_title']
  game_description = request.form['game_description'] 
  existing = db_session.query(Game).filter_by(game_title = game_title).first()
  if existing: 
    flash ('This game title is already in use please try again for a unique game title.')
    return redirect(url_for('display_make_game'))
  else:
    new_game = Game(game_title=game_title, game_description=game_description)
    db_session.add(new_game)
    db_session.commit()
    db_session.refresh(new_game)
    game_id = new_game.id
  return redirect(url_for('display_make_challenge', game_id=game_id))

@app.route('/make_challenge/<int:game_id>', methods=['GET'])
def display_make_challenge(game_id):
  """this method will display the make challenge form"""
  return render_template('make_challenge.html', game_id=game_id)

@app.route('/make_challenge/<int:game_id>', methods=['POST'])
# TO DO ERICA 2
def next_challenge(game_id):
  """ if the user CLICKS on +1 CHALLENGE BUTTON this method will WRITE the challenge to the
  challenge table in the database and display a new blank form till user presses submit."""
  story = request.form.get('story')
  puzzle = request.form['puzzle']
  solution = request.form['correct_solution']
  # challenge_position = request.form['challenge_position'] add in a hidden form input that will auto count how many challenges are made
  if story is None or puzzle is None or solution is None: 
    flash ('Please fill out everything on the page as this is all critical information your players will need in order to play your game.')
    return redirect(url_for('display_make_challenge'))
  else:
    new_challenge = Challenge(game_id=game_id, story=story, puzzle=puzzle, solution=solution)
    # how do I add a counter?
    db_session.add(new_challenge)
    db_session.commit()
    db_session.refresh(new_challenge)
  return redirect(url_for('next_challenge', game_id=game_id))
  

@app.route('/make_challenge', methods=['POST'])
# TO DO ERICA 3 
def finish_game_creation():
  """this method will run when user CLICKS SUBMIT BUTTON redirect users to select games page 
  when they are done creating their game. """

  return render_template(url_for('current_game'))
  

@app.route('/select_games', methods=['GET'])
# TO DO ERICA 3 - FIGURE OUT HOW TO MAKE MY ROW DATA CLICKABLE AND MAKE THE GAME LINK ACTIVE 
#SIMILAR TO THE FUNCTION BELOW.
def select_game():
  """This method will query the database for all the games avaliable to play"""
  games = db_session.query(Game).all() 
  return render_template('select_games.html', games=games)


@app.route('/status', methods=['GET'])
# TO DO - GAME ERICA 3 - WAIT TILL I HAVE MORE GAME SESSIONS GOING AND FIGURE OUT HOW TO MAKE THE
#LINKS ACTIVATE THE CURRENT 
def display_status():
  """ this method will display the all the games the user is currently playing and which 
  one is active. The user should be able to toggle between the other games to switch their 
  current active game."""
  status = db_session.query(Session).all()
  return render_template('status.html', status=status)

# @app.teardown_request
# def shutdown_session(exception = None):
#   db_session.remove()


if __name__ == '__main__':
  app.run() 
