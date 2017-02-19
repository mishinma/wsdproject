#Final Submission (scroll down to see original project plan)
## 1. Team
547592 - Max Reuter
519656 - Mikhail Mishin
539940 - Ekaterina Dorrer

## 2. Implemented Features
### Authentication
During registration, new users have to choose if they want to sign up as a player or a developer.
After submitting the registration form, new users are sent an activation link via mail to verify
their email address. After clicking on the activation link, users are free to login and play, buy,
as well as edit games, depending on what account type they chose.
Internally we use as many built in Django features as possible. For instance, we choose to not
create custom users but rather assign user objects to a certain user group that defines their
rights. We added the `permission_required` tag to sensitive views to enforce access control.
Furthermore, users can choose to login via Google. However, logging in via third-party only
grants player rights. We are very pleased with the authentication of our application and ran
into little issues. We would give ourselves 200 points in this category.

### Player Functionalities
As mentioned earlier, players can play and buy games. We ensure that players can only play
games they have pruchased previously and redirect them to the purchase page if they try
to access the gameplay page directly. Players can find games in a multitude of ways:
- scroll through the index page where all games are listed, ordered by their creation date (available to everyone)
- choose a category from the dropdown menu and scroll through the games of a certain category (available to everyone)
- place a search query to look for games by their name, which also finds partial matches and filters out
unnecessary terms like articles (available to everyone)
- scroll through the list of purchased games (only available to logged in players)

Moreover, we also added some basic profile functionality like changing username, email and password.
We are very pleased with the implemented functionalities for players. We would give ourselves 300 points
in this category.

### Developer Functionalities
Developers are restricted to publishing and editing games. Attempting to play a game as a developer will
result in a 403. However, developers can still scroll through games and view the details page of games.
Instead of the 'My Games' tab of players, developers have a 'My Inventory' tab which provides an
overview over all theiry published games, as well as sales statistics. Developers can edit their current
which allows them change every aspect about their game. On the edit page (also while creating a game)
developers can also put their games on sale which will be represented in the UI by a red sale logo to players.
We wanted to include pictures for games but as Heroku does not provide a proper file system, it is not
supported (uploading a picture will not affect the record in the database). Instead we use a static placeholder
that hints how game logos should work. The aforementioned sales statistics, which is found on the 'My Inventory'
page, shows the overall sales as well as sales of individual games. The graphs are rendered dynamically
by making AJAX calls to the backend. Developers, just like players, can also edit their accounts data.
We are very pleased with how the developer functionality turned out and would award ourselves 200 points.

### Game/Service Interaction
The gamplay page shows the game in an iFrame, an overall leaderboard and the player's best as well as
last submitted score. We implemented support for all message types that were described in the project
description. Thus, games can send load, save, score and setting messages to the application which will
process the message and report errors if any occur. In fact, our application relies on receiving a
'setting' message when loading a game specify the dimenions of the iFrame. All communcation on the gameplay
page including pupulating as well as updating the displayed scores and messages from the game are handled
as AJAX calls by the backend. The Game/Service interaction works very well with the provided test game. We
are happy about the game/service interaction and would give ourselves 200 points.

### Quality of Work
The tried to implement the seperation-of-concerns principle as much as possible and therefore templates
are almost exclusively used for displaying data. However, because we wanted to create genereic, re-usable
templates, we had to shift small parts of the logic to templates. This logic mostly used to determining
what user group the user belongs to or if a certain button type should be displayed. Moreover, we many
small templates and used them as components to ensure a great look and feel for the user.
Unfortunately, we did not have time comment our code and more importantly to write docstrings for our
funtions. However, we think our code is quite clean and easy to understand, which makes up for the missing
comments. This is due to fact that we created helper functions for many calls, making the actual code
much easier to understand (fat models, skinny views principle. As for testing, we heavily utilised unit
testing to ensure code changes did not break existing functionality. Alltogether, we implemented 60 tests
that test various functions of our application. We are very pleased with the quality and design of our
implementation. Furthermore, we think our unit test setup ensures great code quality. We would award
ourselves 100 points.

### Non-Functional Requirements
Although our projects plan is not very detailed, we still think that it nicely summarised the goals we had
when starting the project, especially when keeping in mind that we were informed about its necessety during
exam time. As for communication, we heavily relied our Telegram group and also created a Trello board to keep
track of what was left to do and what had already been completed. As our GitLab repository, we always kept
our master branch clean and made sure to implement features on seperate branches before merging them to master.
This also allowed to track changes nicely and revert in case problems occurred. We accepted almost 80 merge
requests and the history of our master branch shows nicely how the projects evolved. Eventhough there are not
many comments in our code, we still think we did a very good job in terms of non-functional requirements and
would give ourselves 150 points.

### Save/Load and Resolution feature
As already described earlier, we implemented all of these additional features using jQuery and our backend.
Users can have one save slot for each game. When they save again, the old save is overwritten. Also, our
application relies on the resolution message to set the iFrame to the correct size. As these features work
very well and pass all other tests, we would award ourselves 100 points

### Third-Party Login (Google)
We implemented third-party login with a Google account using 'social django'. We configured to app to work
nicely with our backend and configured some custom functions to keep our backend synced when someone logs
in using a third-party service. Unfortunatly, the deployment to Heroky broke this feature but we are working
on fixing it.

### REST API
We implemented a simple REST API that allows useres to retrieve different kind of informations. Mainly, users
can look for games in different ways as well as scores associated with a certain game. We intentionally decided
to not include any endpoint functionality that would require authentication because OAUTH seemed like too much
for such a simple project and Basic HTTP Authentication seemed like very bad usability for this kind of API.
Because we think the API is well structured and well tested we would still assign us 75 points.

### Mobile Friendly
We put much effort into making our application responsive. The continuously tested our application with different
screen sizes and also on mobile phones after deploying our application to Heroku. We used responsive classes of
the Bootstrap framework as well as viewport tags to ensure this behaviour. We would assign ourselves 50 points.

# Project Plan
## 1. Team
547592 - Max Reuter
519656 - Mikhail Mishin
539940 - Ekaterina Dorrer 

## 2. Goal
Create an online game store for JavaScript games

## 3. Features
*Minimum functional requirements*:
* Register as a player and developer
* As a developer: add games to their inventory, see list of game sales
* As a player: buy games, play games, see game high scores and record their score to it

### Authentication:
* Register with email, pick a username
* Login and logout with email/username and password
* Use email to login
* Use Django auth  

### Basic player functionalities:
* Search of games by name, game category and developer name
* Sort the search by popularity, category
* Buy games with the payment system 
* Play games
* Security restrictions, e.g. player is only allowed to play the games they’ve purchased
* Also consider how your players will find games (are they in a category, is there a search functionality?)

### Basic developer functionalities:
* Add a game (URL) and set price for that game and manage that game 
* Remove the game 
* Modify URL
* Change price permanently and temporarily (sales, offers etc.)
* Basic game inventory and sales statistics (how many of the developers' games have been bought and when)
* Security restrictions, developers are only allowed to modify/add/etc. their own games, developer can only add games to their own inventory, etc.

### Game/service interaction:
* When player has finished playing a game (or presses submit score), the game sends a postMessage to the parent window containing the current score. This score must be recorded to the player's scores and to the global high score list for that game. See section on Game Developer Information for details.
* Messages from service to the game must be implemented as well

### Quality of Work
* Quality of code (structure of the application, comments)
* Purposeful use of framework (Don't-Repeat-Yourself principle, Model-View-Template separation of concerns)
* User experience (styling, interaction)
* Meaningful testing

### Non-functional requirements:
* Project plan
* Overall documentation, demo, teamwork, and project management as seen from the history of the GitLab project

### Save/load and resolution feature:
* The service supports saving and loading for games with the simple message protocol described in Game Developer Information
* 3rd party login
* Allow OpenID, Gmail or Facebook login to the system. 

### RESTful API
* Design and Implement RESTful API to the service
* Showing sales of games for anyone registered

### Own game 
* Develop a simple game in JavaScript that communicates with the service: pick the right color game.
* You can host the game as a static file in your Django project or elsewhere. But you should include it in your repository.
* Do not start this before you have a working implementation of the service

### Mobile Friendly
* Bootstrap with 3 screen sizes (desktop, tablet, phone)
* Enable sharing games and scores in social media (Facebook, Twitter, Google+, etc.), including Facebook groups and private messages.
* Include metadata, the shared items has a description and an image.

### _Extra features_:
1. Mobile controls for the games
2. Private user profile - games bought and played, statistics
3. Gift games to other players

## 4. Technology Stack
### Frontend:
* Bootstrap
* JQuery

### Backend:
* Django
* PostgeSQL

## 5. Priorities
* Functionality 
* Robustness


## 6. Process and Time Schedule
### Weeks 51-52: 
* Database design 
* First deployment to Heroku
* Testing

### Weeks 1-2: 
* Basic page structure and functionality
* URL mapping 
* Basic views
* Page design with Invision
* Get Bootstrap going
* Testing

### Weeks 3-4: 
* Finish mandatory requirements
* Start developing the extra features
* More testing

### Weeks 5-6: 
* Polish
* Develop game
* Final testing

### Week 7:
* Buffer

## 7. Project management
### Communication:
* Regular meetings
* Trello boards
* Telegram chat


## 9. Testing
* Create testing database
* Unit testing
* Black box testing
* White box testing
* Integrity testing
* Continuous integration testing
* User testing

## 8. Risk Analysis
* Insufficient time
* Buffer week should be enough to address this issue