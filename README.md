# Project Plan
## 1. Team
547592 - Max Reuter
519656 - Mikhail Mishin
539940 - Ekaterina Dorrer 

## 2. Goal
Create an online game store for JavaScript games. The

## 3. Features
###Minimum functional requirements:
*Register as a player and developer
*As a developer: add games to their inventory, see list of game sales
*As a player: buy games, play games, see game high scores and record their score to it
###Authentication:
*Login, logout and register (both as player or developer). Email validation is not required for the minimum points but is required to get more than 100 points. For dealing with email in Django see https://docs.djangoproject.com/en/1.10/topics/email/#email-backends You do not need to configure a real SMTP-server, using Django's Console Backend is enough for full points.
*Use Django auth
Basic player functionalities (mandatory, 100-300 points):
Buy games, payment is handled by the course’s mockup payment service: http://payments.webcourse.niksula.hut.fi/ 
Play games. See also game/service interaction
Security restrictions, e.g. player is only allowed to play the games they’ve purchased
Also consider how your players will find games (are they in a category, is there a search functionality?)
Basic developer functionalities (mandatory 100-200 points):
Add a game (URL) and set price for that game and manage that game (remove, modify)
Basic game inventory and sales statistics (how many of the developers' games have been bought and when)
Security restrictions, e.g. developers are only allowed to modify/add/etc. their own games, developer can only add games to their own inventory, etc.
Game/service interaction (mandatory 100-200 points):
When player has finished playing a game (or presses submit score), the game sends a postMessage to the parent window containing the current score. This score must be recorded to the player's scores and to the global high score list for that game. See section on Game Developer Information for details.
Messages from service to the game must be implemented as well
Quality of Work (mandatory 0-100 points)
Quality of code (structure of the application, comments)
Purposeful use of framework (Don't-Repeat-Yourself principle, Model-View-Template separation of concerns)
User experience (styling, interaction)
Meaningful testing
Non-functional requirements (mandatory 0-200 points)
Project plan (part of final grading, max. 50 points)
Overall documentation, demo, teamwork, and project management as seen from the history of your GitLab project (and possible other sources that you submit in your final report)
Save/load and resolution feature :
The service supports saving and loading for games with the simple message protocol described in Game Developer Information
3rd party login (0-100 points)
Allow OpenID, Gmail or Facebook login to your system. This is the only feature where you are supposed to use third party Django apps in your service.
RESTful API (0-100 points)
Design and Implement some RESTful API to the service
E.g. showing available games, high scores, showing sales for game developers (remember authentication)
Own game (0-100 points)
Develop a simple game in JavaScript that communicates with the service (at least high score, save, load)
Note that it does not need to be the greatest game ever, going a little beyond the given example test game is enough.
Also note, that you can only get points for one game that you develop.
You can host the game as a static file in your Django project or elsewhere. But you should include it in your repository.
Do not start this before you have a working implementation of the service
Mobile Friendly (0-50 points)
Attention is paid to usability on both traditional computers and mobile devices (smart phones/tablets)
It works with devices with varying screen width and is usable with touch based devices (see e.g. http://en.wikipedia.org/wiki/Responsive_web_design )
Social media sharing (0-50 points)
Enable sharing games in some social media site (Facebook, Twitter, Google+, etc.)
Focus on the metadata, so that the shared game is “advertised” well (e.g. instead of just containing a link to the service, the shared items should have a sensible description and an image)

###Extra features:
1. Mobile controls for the games

## 4. Technology Stack
Frontend:
* Bootstrap
* JQuery

Backend:
* Django
* PostgeSQL

## 5. Priorities



## 6. Process and Time Schedule

Weeks 1-2: 
Weeks 3-4: 
Monday, Feb 1st: 

## 7. Project management



## 9. Testing


## 8. Risk Analysis