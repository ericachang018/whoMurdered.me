# This is the model for my final project 

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
import datetime 

engine = create_engine('sqlite:///kill.db', convert_unicode = False)
db_session = scoped_session(sessionmaker(autocommit = False, 
	autoflush = False, bind = engine))

Base = declarative_base()



def now():
	return datetime.datetime.now()

class User(Base):

	__tablename__ = "users"

	id = Column(Integer, primary_key = True)
	email = Column(String(64), nullable = True)
	password = Column(String(64), nullable = True)
	name = Column(String(64), nullable = True)
	verified = Column(String(64), default = 0)


class Session(Base): 

	__tablename__= "sessions"

	id = Column(Integer, primary_key = True)
	user_id = Column(Integer, ForeignKey("users.id"))
	game_id = Column(Integer, ForeignKey("games.id"))
	game_level = Column(Integer, ForeignKey("challenges.id"))
	started_at = Column(DateTime, default = now())
	completed_at  = Column(DateTime, default = now())


class Game(Base):

	__tablename__ = "games"

	id = Column(Integer, primary_key = True)
	game_title = Column(String(), nullable = True)
	game_description = Column(Text(), nullable = True)


class Challenge(Base):

	__tablename__= "challenges"

	id = Column(Integer, primary_key = True)
	game_id = Column(Integer, ForeignKey("games.id"))
	challenge_position = Column(Integer, nullable = True)
	story = Column(Text(), nullable = True)
	puzzle = Column (Text(), nullable = True)
	solution = Column(Text(), nullable = True)
	latitude = Column(Integer, nullable = True)
	longitude = Column(Integer, nullable = True)

	
def init_db():
	Base.metadata.create_all(engine)


def main():
	pass 

if __name__=="__main__":
	main()