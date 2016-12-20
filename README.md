# Project Plan
## 1. Team
547592 - Max Reuter
519656 - Mikhail Mishin
539940 - Ekaterina Dorrer 

## 2. Goal
Create an online game store for JavaScript games. The

## 3. Features
*Minimum functional requirements*:
* Register as a player and developer
* As a developer: add games to their inventory, see list of game sales
* As a player: buy games, play games, see game high scores and record their score to it

### Authentication:
* Register with email, pick a username
* Login and logout with email/username and password. 
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