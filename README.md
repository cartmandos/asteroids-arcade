# Asteroids

```
###########################################################
#                                                         #
#     _    ____ _____ _____ ____   ___ ___ ____  ____  _  #
#    / \  / ___|_   _| ____|  _ \ / _ \_ _|  _ \/ ___|| | #
#   / _ \ \___ \ | | |  _| | |_) | | | | || | | \___ \| | #
#  / ___ \ ___) || | | |___|  _ <| |_| | || |_| |___) |_| #
# /_/   \_\____/ |_| |_____|_| \_\\___/___|____/|____/(_) #
#                                                         #
###########################################################
```

The classic arcade game - Asteroids!
A Python implementation using object-oriented programming principles.

## Key Features

- Fully Functional: Enjoy the classic Asteroids experience with ship movement, asteroid collisions, and torpedoes.
- OOD: The game is implemented using a modular structure with Ship, Asteroid, GameRunner, and Screen classes.

## Getting Started

Clone the repository: git clone <https://github.com/cartmandos/asteroids-retro.git>

Run the game:

``` bash
python main.py
```

Enjoy! 🚀

## Classes

### Ship Class 🛸

The Ship class manages the ship's position, speed, and heading values.
It provides essential methods for 2D travel, including turning and accelerating.

### Asteroid Class ☄️

The Asteroid class handles the position, speed, and size of asteroids.
It includes methods for responsive movement, collision detection, and acceleration.

### GameRunner Class 👾

The GameRunner class represents the game play.
It holds instances of the Ship class (player), user score, lives, a list of asteroids, and a dictionary of torpedoes.
The class methods run the game in a "passive approach" by listening to user input and reacting on a timed re-occurring loop.
GameRunner holds initial values that are constructed for the game, such as, steroids size, splits,
user lives, torpedo limit and lifetime, etc.
This helps maintain a separation of concerns between the game instance and the objects within, allowing for modularity and easy adjustment of game parameters and allows more flexibility for future enhancements and features.

### Screen Class 🖥

The Screen class takes care of the UI - graphics and drawing the game.

## Design Decisions

### Guidelines

- **Modular Design**: Each class focuses on its specific functionality, enhancing maintainability and flexibility.

- **Object Independence**: Objects are unaware of other objects and game mechanics, allowing for easier modifications and future enhancements.

- **OOP Principles**: Utilizes inheritance and polymorphism to achieve cleaner and more efficient code.

### Challenges and Solutions

- **Code Repetition**: Balanced object independence with efficient method design to reduce code repetition.

- **Asteroid Splitting**: Implemented splitting logic within the Asteroid class for greater modularity and flexibility.

- **Argument Definition**: Chose separate position and speed arguments for clarity and ease of use.

### Considerations Explained 🤔

- **Method Repetition**: Despite similar methods in different classes, such as the movement formula which is identical for Ship, Asteroid and
Torpedo (ie. get_coordinate method). I had to make a choice if I want to put the
method public (for ex. in GameRunner) so all objects could use it and avoid some
sort of "code repetition", and also could maybe get rid of "bounds" arg that
is already defined in GameRunner class.
I chose to give each object the method because I wanted to give GameRunner independence
on game play parameters and RUNNING the game, not the objects.
IMHO, it provides better modularity and flexibility for a change in the way a specific object
moves, without having to refactor the other objects or GameRunner.

- **Asteroid Splitting Implementation**: I had to decide where to implement the splitting of the asteroids.
I could (as I first did) to implement the all code for splitting in GameRunner,
since it involves handling with a Torpedo obj., Asteroid obj., setting them and
giving them speed values through other formula than the "ordinary" constructed
asteroid. But I decided to add accelerate method and new set method that changes
speed (to adjust for asteroids to part ways). It seems more natural to give the
Asteroid class to handle its object's speed and speed setting, but also it allowed
me to implement the accelerate method in a more general way for other objects.
So if for example I now want to get asteroid be affected from collision with themselves
or new object, or split from a collision with ship, it's much easier.
Also it's possible with small changes to make asteroids to split into more than 2
asteroids.

- **Class Argument Definition**: When started the project, I had to decide how I'm going to define class args,
specifically position and speed. Knowing it will have vast impact on the code
further on. I could have write pos and speed as implied in the ex9 pdf, which
is a tuple/list in the format of (X coord, X coord speed). or even give coordinates
separate args; x, y instead of one tuple in format of (x,y).
It also involved looking at the formulas given and parameters that I needed for
the implementation.
I decided to create pos and speed separately, each as a tuple of its axis x & y.
Most of the times I needed the position/speed of an object and it was easier to
implement this way. Also, I could make more general methods for one axis and then
call them for each axis separately which seemed more elegant. Furthermore, I think
that way it's more informative args and since tuples are immutable it adds another
dimension of "privacy" to obj. args.

#### cheers 🍻
