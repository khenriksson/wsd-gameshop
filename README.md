# Project plan for WSD 2019

Initial ideas of what kinds of views and models are needed, how they relate to each other. Pay attention to the models - the better the initial guess, the faster you get to implement things as changes to models briefly interrupt the whole team. Give an initial draft of what models you plan to have and what fields those models have. Note that Django already has a user model.

Describe the implementation order and timetable.

*Kasper Henriksson*, 647214

*Silvia Geier*, 525132

*Rasmus Laug*, 587633

This is a project plan for the course Web Software Development at Aalto University.
The work is done by the students mentioned, who are committed to creating a webshop for games.

# General description

### Features to be implemented

We plan to implement all the necessary and mandatory 

#### Mandatory features and models

##### Authentication
Both players and developers need to be able to register to the service, and thereafter login or logout of it, using Djanguo auth.
**Implementation order and listed features:**
+ Register
+ Login and logout

##### Basic player and developer functionalities
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

##### Game/service interaction
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

##### Quality of Work
The code is to be commented well and according to the DRY-principle. Testing happens before and after merges, to make sure the code works as planned. The code is to be understood by anyone who wants to read it.

#####  Non-functional requirements
The project needs to have a full final project testament, with information on the most important features, and the project demo is to be perfect. This project is a team effort.

#### Extra features

*These are features, that if time allows, then we'll implement them.*

##### 3rd party login
We want it to be possible for players to login through Facebook, according for example to this [link](https://scotch.io/tutorials/django-authentication-with-facebook-instagram-and-linkedin "Django Authentication with Facebook").

##### Social media sharing
Players/developers could be able to share the media to Twitter, with a link to the game.

##### Tags
Developers could get tags based on how much their games are played or used, such as "Popular game developer" or similar. 

##### In-game transactions
Transactions while playing games, for example to win the game or earn an advantage.

### Views

##### Register
As with the implementation order for the models, registering is probably the first view we need to implement. This register function needs to POST the information gathered from the registration form, and check if it's valid. Whether it's valid, we need to save the user and user information to the database. Some kind of check to see if it's successful is probably also needed, as there might happen changes on the way that interfere with the saving. This relates to the user models showed earlier.  
**Function features:**
+ POST and save user to database
+ Check if successful or unsuccessful, depending on if the form is valid as well

##### Transaction
The buy and wallet model needs a transaction feature that checks if the buy is successful, and also whether or not the user already owns the game.  
**Function features:**
+ Buy game, some kind of POSTs to the service needed, also redirect to successful or unsuccessful purchase

##### Add game
View for adding a game to the service. This probably also needs some kind of form that is POSTed to the database with games.  
**Function features:**
+ POST and save form to database

##### Edit game
**Function features:**
+ Changing info for the game, GETting it and POST the new information to the server

### Forms

We are planning on creating forms at least for registering a user and publishing a game. Registering needs to containt information on user email, their chosen username, first and last name.

# Project work plan

The team plans to meet up regularly, once a week, to code as well as get up to date with what has happened since last time.

### Implementation order and timetable

As this project plan has been approved, we'll start by implementing the models and then move on to the views. The second most important objective is to get a functional test environment for html up, so that we can start implementing visible changes as fast as possible.

For project management we're planning on setting up a Asana project to keep track of features.
The timetable is to start instantly after the project plan approval.

