My final project for hackbright is a webapp augumented reality game (Fall - 2013) 

users can create many games 
users can have many games running (sessions)
users must complete first game before they are allowed to creat their own games

games have multiple challenges 

each challenge has
	a game id which ties to the game database

	a challenge position - which denotes how far 
	along you are in the game 

	a story - which will be engaging to make the 
	players want to keep playing 

	a puzzle - some sort of riddle, puzzle, search, 
	or location based challenge that will unlock 
	coordinates that will progress the game forward 

	a solution - this will check the user input for 
	the correct answer and if it is correct it will 
	show gps coordinates 

	latitude / longitude will access google maps for 
	people to check in and if they are with in 30 meters 
	of the location will progress the game one more step

2014 - Updates

Goals for this year. 

- Write instructions on how to run locally (Done) 
- Uninstall all un-neccessary pip packages
- Make my application work with out bugs. 
	- Fix opening page hidden link which triggers first game
	- Add a feature where first game must be completed before other
	parts of the game can be accessed ie creating your own game, 
	accessing other games on db. 
	- Fix log in feature (maybe add a facebook signin or google sign in)
	- Make "Games" Tab - Make each of your running games clickable and 
	it will redirect you to your current challenge of that game set.
	- In "Make Games" add a done button next to submit so the user 
	"finish" creating their game. This will redirect them to a review page to 
	make sure they are happy with game before submitting. 
	- Make "Current game" show you your current challenge on your active game. 
 
- Push to Heroku 



---------------- How to install and run locally ------------------ 
Some of the conventions used below include 
>> Things typed into your terminal. 


1. Git clone repo in desired location 
>> git clone https://github.com/ericachang018/whoMurdered.me.git

2. Make a virtual enviroment (optional)
>> virtualenv env 

3 Activate your new virtual enviroment
>> source env/bin/activate 

4. Install requirements. 
>> pip install --upgrade -r requirements.txt

5. Run application  
>>python murder.py

6. After running the application you will see a url which 
will point to a local host. Follow http://127.0.0.1:5000 to interact with your 
local copy of whoMurdered.me 

This is what you should see. 
 * Running on http://127.0.0.1:5000/
 * Restarting with reloader  



