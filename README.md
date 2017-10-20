# Web Software Development Project: Haze

A term project for the course CS-C3170 Web Software Development taught in spring 2017 at Aalto University. 
The goal of the project was to implement an online game store for JavaScript games. 
The service has two types of users: players and developers. Developers can add their games to the 
service and set a price for it. Players can buy games on the platform and then play purchased games online.
We have deployed our app on Heroku:  [https://shielded-tor-84132.herokuapp.com/index/](https://shielded-tor-84132.herokuapp.com/index/). You can login as a test developer (username: 'test_developer', pass: 'asdf') or a test player (username: 'test_player', pass: 'asdf') 

## Basic Features 

### Authentication:
* Login, logout and register (both as player or developer)
* Email authentication (the link is actually not sent because we didn't have a real SMTP-server)
* Third party login (Google)

### Player Functionalities:
* Buy games using a mock-up payment system 
* Play games (See also game/service interaction)
* Search games by name or category
* Security restrictions, players are only allowed to play the games they’ve purchased

### Developer Functionalities:
* Add a game (URL) and set price for that game and manage that game 
* Remove the game 
* Modify URL
* Basic game inventory and sales statistics (how many of the developer's games have been bought and when)
* Security restrictions, developers are only allowed to modify/add/etc. their own games


### Game/Service Interaction
New games are added to the inventory by giving a link to an URL of the game, which is an HTML file that is displayed in an iFrame to the player. The platform supports a simple message system, the games and the service exchange messages to submit score and save/load the game's state. The gamplay page shows the game in an iFrame, the leaderboard and the player's best and
last submitted scores.

### REST API
We implemented a simple REST API that allows useres to retrieve different kind of information. Mainly, users
can look for games in different ways as well as scores associated with a certain game. 

### Mobile Friendly
We put much effort into making our application responsive. The continuously tested our application with different
screen sizes and also on mobile phones after deploying our application to Heroku. We used responsive classes of
the Bootstrap framework as well as viewport tags to ensure this behaviour. 


## Team and Work Allocation

#### Max Reuter
- payment service
- REST API
- searching by query and category
- registration
- third-party login
- email verification
- database design

#### Mikhail Mishin
- payment service
- Heroku deployment
- sales statistics
- unit testing setup
- code reviews
- service/game interaction
- templates
- configuration
- database design

#### Ekaterina Dorrer
- page structure
- Bootstrap configuration
- responsive design
- basic profile functionality
- game leadboards and personal scores
- templates
- CSS
- HTML


## 4. Technology Stack
### Frontend:
* Bootstrap
* JQuery

### Backend:
* Django
* PostgeSQL
