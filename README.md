# EDIT 14.2.2020

Descriptions and points given. 
*Kasper Henriksson*, 647214

*Silvia Geier*, 525132

*Rasmus Laug*, 587633

The application is deployed at [Powerful-Wildwood](https://powerful-wildwood-65729.herokuapp.com/), and too not mix the Heroku requirements we've deployed it from the Herokudep branch. This may not be the best practice but as we didn't want to put too much time on setting up individual requirements/settings, we felt this was the best option. 

If the user is not logged in and only looks at the front page, there is very little the user can do except search for games. 
If the player clicks on a game they’ll see the details related to it, along with a signup/login information.

When the user signs up they’ll get to choose whether to be a “regular” player or a developer. If they choose not to be a developer, some features won’t be seen, such as the add game. 
If the player clicks on one of the games, the information related to it will be shown, along with a buy button, and if they press it it’ll direct to the payment app, with buy and cancel buttons. Clicking Your Games will show all the games that have been bought by the player.

If the user signs up as a developer, they will be able to Add Games and see how much they’ve earned through their games in the Your Games tab. They can also buy other players games and play them as well.

When users sign up, they have to activate the account through email confirmation. The email confirmation is currently sent to https://mailtrap.io/inboxes. To see the email, click the Demo Inbox and the latest email to the left. Unfortunately the email has to be copied due to mailtrap reasons.

***Login details mailtrap:***

Email: kasper.henriksson@aalto.fi

Password: igD5v@pJ95DF4QX

***Login codes:***

Username: developer

Password: tjena123

***Login codes:***

Username: player

Password: tjena123

## Features implemented:

### Authentication (mandatory, 100-200 points):
**200 points**

*Motivation:* We've implemented everything mandatory, and in addition the email confirmation with tokens and using mailtrap inbox for testing.

### Basic player functionalities (mandatory, 100-300 points):
**300 points**

*Motivation:* All the basic functionalities are implemented, including buying games, playing games as well as the security restrictions. We also have a search bar that isn't case sensitive when searching.

### Basic developer functionalities (mandatory 100-200 points):
**200 points**

*Motivation:* The basic developer functionalities are well implemented, as well as some sales statistics over how much they've made from each game. With a little more time it would have been fun to implement a little deeper statistics. The security restrictions should also be in place.

### Game/service interaction (mandatory 100-200 points):
**200 points**

*Motivation:* This is implemented in full. This is one of the features that Silvia spent the most time on, as we had some early difficulties with it.

### Quality of Work (mandatory 0-100 points)
**100 points**

*Motivation:* The structure should be relatively clean with separate files and a well separated Model-View-Template. In our own opinion we fill the minimum requirements for the UX, as it's something where immense time could be put down. We spent the last few days documenting the code, in a manner that in our opinion let's everyone understand what happens. At least with basic understanding.

### Non-functional requirements (mandatory 0-200 points)
**200 points**

*Motivation:* Our project plan was well defined. The documentation was mostly done using Telegram as we wanted to keep close touch as much as possible. For this we used Telegram's built in "pin" function to keep track of important files such as the final.

### Save/load and resolution feature (0-100 points):
**100 points**

*Motivation:* This has been fully implemented.

### 3rd party login (0-100 points)
**100 points**

*Motivation:* 3rd party login implemented with double backends and possible to use Google account.

### Own game (0-100 points)
**100 points**

*Motivation:* Adventures of Ron created by Rasmus

### Mobile Friendly (0-50 points)
**40 points**

*Motivation:* The playing of game isn’t really super mobile friendly but it works, and everything else should be dynamic. The problem lies when trying to "play" the games, as the main frame isn't very reactive.

### Done by Silvia:

* Game-service interaction
* The model GameData and its use
* Everything in game.js
* In views.py all functions related to this - saving scores, saving and loading game states, fetching high scores, all urls related to these
* How you can see and play the game and your actions in detail.html

* Navbar mostly as a whole
* Game search functionality
* In views.py search_games, navbar functionality

* User profile
* Profile page
* Personal info editing form & functionalities

* Player / Developer difference
* Selecting in signup
* Possibility to ‘upgrade’ to developer mode on profile page


### Done by Kasper:

* Setting up the project beginning, models and forms
* User settings
* First version of the Detail showing information of the game
* Signup function and user authorization
* Confirmation email
* Activation token and activate function
* AddGame form and function
* Developer view function in your games
* Securing the functions and making sure what’s available for users not logged in
* Editing game
* Sign in
* Send email function, could be used universally but now used in confirmation email, should be secure enough to not allow subject header injections
* All transaction related function
* Also, fixed all version-control that came up during development



Front related:
* Footer stays in the same place
* Implemented the base.html to make sure all other html’s extend it with the block content.
* Card type for games




### Done by Rasmus:


* Implemented 3rd party login: with Google
* Initial Heroku deployment and setting the app up to use Herokus  PostgreSQL.
* Own game I.e "Adventures of ron". Simple jumping game.
* Edit and remove game functionalities.
* Custom 404 handler and the page.


Front related
* Your_ games  and edit game view
* In your_games how the developer games are shown.
* Some small tweaks with the 'Main' view.




# Project plan for WSD 2019

Initial ideas of what kinds of views and models are needed, how they relate to each other. Pay attention to the models - the better the initial guess, the faster you get to implement things as changes to models briefly interrupt the whole team. Give an initial draft of what models you plan to have and what fields those models have. Note that Django already has a user model.

Describe the implementation order and timetable.

*Kasper Henriksson*, 647214

*Silvia Geier*, 525132

*Rasmus Laug*, 587633

This is a project plan for the course Web Software Development at Aalto University.
The work is done by the students mentioned, who are committed to creating a webshop for games.

# General description

## Features to be implemented

We plan to implement all the necessary and mandatory first of all, and then move on the extra ones in case time lets us.

### Mandatory features and models
***

#### Authentication
Both players and developers need to be able to register to the service, and thereafter login or logout of it, using Djanguo auth.
**Implementation order and listed features:**
+ Register
+ Login and logout

#### Basic player and developer functionalities
Players can buy games through a payment service handled by the course mockup service [Tilkkutakki](https://tilkkutakki.cs.aalto.fi/payments/ ). They're also able to play games, and **only** games they've purschased. There needs to be a simple category for games, as well as a search function.

Developers can add games, set prices for and manage that game, that is to be some kind of administrator of their own games. They have their own game inventory with sales statistics, showing how much money they've made from all games and also individually by game. They can **only** modify their own games. 

As developers can be players as well, this model is to be implemented as one **user** and with another **wallet** model for handling own money. This could be done for example like this:

```
class User(models.Model):  
    user = models.OneToOneField(User)
    username = models.CharField(max_length=40)  
    user_id = models.CharField(max_length=16)  
```

```
class Wallet(models.Model):
    wallet_id = models.CharField(max_length=16, unique=True)  
    wallet_amount = FloatField()  
    owner = models.ForeignKey('User', ...)
```

```
class Payment(models.Model):
    pay_id = models.CharField(max_length=32)
    pay_amount = FloatField()
    pay_buyer = ForeignKey('User',...)
    pay_seller = ForeignKey('User',...)
    pay_success = BooleanField()
```

As players are only allowed to play their own games and not others, we need a model implemented for the game access. Example:
```
class GameAccess(models.Model):
    game = models.ForeignKey('Game',...)  
    player = models.ForeignKey('User',...)
```

**Implementation order and listed features:**
+ User implementation for developer and player
+ Adding games
    + Search function implemented concurrently
    + Set prices
    + Game inventory
+ Transactions
+ Security issus
+ Statistics for developers

#### Game/service interaction
Scores are recorded to the player's scores and to the global high score for the game list. Messages from the service to the game must be implemented as well. 

The game model needs an own ID, as well as the owner user, and showing how many times it has been purschased. We do feel that integer is enough for now, even though it might go over 16 bits.

```
class Game(models.Model):
    game_id = models.CharField(max_length=16, unique=True)  
    game_developer = models.ForeignKey('user_id', ...)
    purchases = models.IntegerField()  
    game_url = URLField(max_length=200)
    price = FloatField()
```

**Implementation order and listed features:**
+ Recording scores implemented after or concurrently with adding games

#### Quality of Work
The code is to be commented well and according to the DRY-principle. Testing happens before and after merges, to make sure the code works as planned. The code is to be understood by anyone who wants to read it.

####  Non-functional requirements
The project needs to have a full final project testament, with information on the most important features, and the project demo is to be perfect. This project is a team effort.

### Extra features
***

*These are features, that if time allows, then we'll implement them.*

#### 3rd party login
We want it to be possible for players to login through Facebook, according for example to this [link](https://scotch.io/tutorials/django-authentication-with-facebook-instagram-and-linkedin "Django Authentication with Facebook").

#### Social media sharing
Players/developers could be able to share the media to Twitter, with a link to the game.

#### Tags
Developers could get tags based on how much their games are played or used, such as "Popular game developer" or similar. 

#### In-game transactions
Transactions while playing games, for example to win the game or earn an advantage.

### Views
***

#### Register
As with the implementation order for the models, registering is probably the first view we need to implement. This register function needs to POST the information gathered from the registration form, and check if it's valid. Whether it's valid, we need to save the user and user information to the database. Some kind of check to see if it's successful is probably also needed, as there might happen changes on the way that interfere with the saving. This relates to the user models showed earlier.  
**Function features:**
+ POST and save user to database
+ Check if successful or unsuccessful, depending on if the form is valid as well

#### Transaction
The buy and wallet model needs a transaction feature that checks if the buy is successful, and also whether or not the user already owns the game.  
**Function features:**
+ Buy game, some kind of POSTs to the service needed, also redirect to successful or unsuccessful purchase

#### Add game
View for adding a game to the service. This probably also needs some kind of form that is POSTed to the database with games.  
**Function features:**
+ POST and save form to database

#### Edit game  
**Function features:**
+ Changing info for the game, GETting it and POST the new information to the server

### Forms
***

We are planning on creating forms at least for registering a user and publishing a game. Registering needs to containt information on user email, their chosen username, first and last name.

# Project work plan

The team plans to meet up regularly, once a week, to code as well as get up to date with what has happened since last time.

## Implementation order and timetable

As this project plan has been approved, we'll start by implementing the models and then move on to the views. The second most important objective is to get a functional test environment for html up, so that we can start implementing visible changes as fast as possible.

For project management we're planning on setting up a Asana project to keep track of features.
The timetable is to start instantly after the project plan approval.

