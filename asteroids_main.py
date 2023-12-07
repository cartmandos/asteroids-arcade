############################################################
# FILE : asteroids_main.py

# DESCRIPTION: This file contain GameRunner class and main func.
# GameRunner class is the main handler of the Asteroids! game.
# It holds the screen object in which GUI is operated through.
# Screen min and max values of the screen for axis x & y.
# Moreover it constructs and holds the object of the ship (controlled by user),
# user lives in the game, keep user score, the asteroids and
# torpedoes in the game.
#
# User starts with lives as defined in const. if ship intersect with asteroid,
# one life is taken. ship can shoot torpedoes, destroy asteroids, and
# get points according to points dict defined in consts.
# In case of collision, win, lose or quit user gets a msg accordingly.
#
# Gameplay is built on passive reaction to user, with running the main loop,
# over and over, creating movements and be responsive to user input.
#
# Main Function: runs the game with a parameter of asteroids amount, that
# will determine number of asteroids in the game.
############################################################
# Imports
############################################################
import sys
import random
from screen import Screen
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo

DEFAULT_ASTEROIDS_NUM = 5
############################################################
# GameRunner class
############################################################


class GameRunner:
    """
    A class representing a Asteroids! game.
    A game is composed of a ship that is traveling in 2D, can turn, accelerate
    and shoot torpedoes against asteroids while avoiding being hit by them.

    Gameplay works in passive reaction to user, "listening" to user input while
    looping main game runner loop.

    Consts:
    *Msgs in case of asteroid collision and end game scenarios.
    *Asteroids initial size and speed is defined in the class consts,
    note that asteroids are constructed in init method. the size of the
    asteroid and its speed could be changed or given randomly.
    * Torpedo's limit on screen and torpedo lifetime (defined by loops of the
    main runner) is also defined in consts as part of the gameplay.
    * Initial user/ship lives is set in consts.
    * Points for each asteroid hit, defined in dict const. according to asteroid's
    size.
    * consts relating to splitting asteroids due torpedo hit, are defined as const.
    and could be changed (with a little more adjustment in code) to split more.
    """
    TITLE_COLLISION = "Collision!"
    MSG_COLLISION = "Better watch out...\n Remaining lives: "
    TITLE_WIN = "Victory!"
    MSG_WIN = "You rock!\n Final score: "
    TITLE_LOST = "GAME OVER"
    MSG_LOST = "Maybe next time..."
    TITLE_QUIT_GAME = "QUIT GAME"
    MSG_QUIT_GAME = "Are you sure?"
    ASTEROID_INITIAL_SIZE = 3
    MIN_ASTEROID_SPEED = 1
    MAX_ASTEROID_SPEED = 3
    TORPEDO_LIMIT = 15
    TORPEDO_LIFETIME = 200
    INITIAL_LIVES = 3
    DEAD = 0
    INITIAL_SCORE = 0
    INTERCEPTION_POINTS = {1: 100, 2: 50, 3: 20}
    MIN_SPLIT_SIZE = 2
    SPLIT_VALUES = [-1, 1]

    def __init__(self, asteroids_amnt):
        """
        This is the constructor for GameRunner
        :param asteroids_amnt: number of asteroids to add to the game
        :type asteroids_amnt: int
        :return: a new GameRunner obj. with args in field incl.:
        Screen object - GUI, and its screen min & max values for each axis in 2D.
        Ship object, responsive to user input keyboard press.
        Ship lives defining lives in game and score to keep track of points.
        Also, a list of asteroids in the game, in the amount as give in param,
        and are constructed in this method!
        Dictionary of torpedoes, with object as keys and remaining "lifetime"
        as dict value, torpedoes are set by user presses on "space" in keyboard,
        dict is limited to 15 torpedoes.
        """
        self._screen = Screen()

        self.screen_max_x = Screen.SCREEN_MAX_X
        self.screen_max_y = Screen.SCREEN_MAX_Y
        self.screen_min_x = Screen.SCREEN_MIN_X
        self.screen_min_y = Screen.SCREEN_MIN_Y

        self.ship = self.__set_ship()
        self.__ship_life = self.INITIAL_LIVES
        self.__score = self.INITIAL_SCORE
        self.__asteroids = [self.__set_asteroids() for i in range(asteroids_amnt)]
        self.__torpedoes = dict()

    def get_screen_bounds(self):
        """
        Screen bounds getter
        This is the accepted format in all classes of the game!
        :return: screen min & max value for each axis in the format of a list
        with two tuples, first for axis X, second for Axis Y. each tuple of
        (min, max) format.
        """
        return [(self.screen_min_x, self.screen_max_x),
                (self.screen_min_y, self.screen_max_y)]

    def get_lives(self):
        """
        ship lives getter
        :return: ship's current lives arg (int)
        """
        return self.__ship_life

    def get_score(self):
        """
        user score getter
        :return: current score arg (int)
        """
        return self.__score

    def get_random_coordinates(self):
        """
        This method gets pseudo-random (x, y) coordinates
        for initiating ship and asteroids start positions.
        :return: coordinates within screen bounds, tuple in the format of (x, y).
        """
        x = random.randint(self.screen_min_x, self.screen_max_x)
        y = random.randint(self.screen_min_y, self.screen_max_y)
        return (x, y)

    def get_random_asteroid_speed(self):
        """
        This method gets pseudo-random asteroid speed, min and max values
        defined in class consts.
        :return: random speed for each axis, tuple in the format of (x, y).
        """
        return (random.randint(self.MIN_ASTEROID_SPEED, self.MAX_ASTEROID_SPEED),
                random.randint(self.MIN_ASTEROID_SPEED, self.MAX_ASTEROID_SPEED))

    def __set_ship(self):
        """
        This method sets ship in class arg
        :return: new Ship object with randomized coordinates
        """
        return Ship(self.get_random_coordinates(), self.get_screen_bounds())

    def __set_asteroids(self):
        """
        This method sets new asteroid in list of asteroids class arg.
        This method also registers it to Screen!
        Note that asteroids get random position BUT will not have the same
        position as ship in initialization.
        :return: new Asteroid obj with random position, random speed,
        and size as in class consts.
        """
        x, y = self.get_random_coordinates()
        while (x, y) == self.ship.get_coordinates():
            x, y = self.get_random_coordinates()
        new_asteroid = Asteroid((x, y), self.get_random_asteroid_speed(),
                                self.ASTEROID_INITIAL_SIZE, self.get_screen_bounds())
        self._screen.register_asteroid(new_asteroid, new_asteroid.get_size())
        return new_asteroid

    def set_torpedo(self):
        """
        This method sets new torpedo in game, adds it to dict in torpedoes class
        arg with lifetime as in class consts.
        This method also registers the torpedo to Screen!
        Torpedoes are launched as they are set and note that method
        will not set new torpedo if user reached torpedoes limit.
        """
        if len(self.__torpedoes) == self.TORPEDO_LIMIT:
            return
        new_torpedo = Torpedo(self.ship.get_coordinates(), self.ship.get_heading(),
                              self.ship.get_speed(), self.get_screen_bounds())
        self.__torpedoes[new_torpedo] = self.TORPEDO_LIFETIME
        self._screen.register_torpedo(new_torpedo)

    def __kill_one_life(self):
        """This method subtracts one life from ship life"""
        self.__ship_life -= 1

    def __destroy_asteroid(self, asteroid):
        """
        This method removes asteroid from both class arg list of asteroids and
        screen (un-register), and then checks game status.
        :param asteroid: this is the asteroid meant for disposal
        :type asteroid: Asteroid
        """
        self._screen.unregister_asteroid(asteroid)
        self.__asteroids.remove(asteroid)
        self.check_game_status()

    def ship_asteroid_collision(self):
        """
        This method responds to a ship-asteroid collision scenario in the game.
        It will kill one ship life, update screen lives and give output msg.
        """
        self.__kill_one_life()
        self._screen.remove_life()
        self._screen.show_message(self.TITLE_COLLISION, self.MSG_COLLISION + str(self.get_lives()))

    def __disarm_torpedo(self, torpedo):
        """
        This method will un-register a torpedo from screen & delete it from
        class arg torpedoes dict.
        :param torpedo: this is the torpedo for disposal
        :type torpedo: Torpedo
        """
        self._screen.unregister_torpedo(torpedo)
        del self.__torpedoes[torpedo]

    def split_asteroid(self, asteroid, torpedo):
        """
        This method handles with splitting an asteroid after hit by torpedo.
        This method will construct new asteroid based on given asteroid parameters,
        then will set new speed in motion and set values to adjust new asteroid
        path to part ways from other new asteroids.
        This method registers the asteroid to Screen and after constructing
        new asteroids, sends the asteroid param for disposal.
        :param asteroid: This is the asteroid that needs to split
        :type asteroid: Asteroid
        :param torpedo: this is the torpedo that hit the asteroid
        :type torpedo: Torpedo
        :return:
        """
        for i in range(len(self.SPLIT_VALUES)):
            new_asteroid = Asteroid(asteroid.get_coordinates(),
                                    asteroid.get_speed(), asteroid.get_size() - 1,
                                    self.get_screen_bounds())
            # Sets new speed in motion
            new_asteroid.collision_acceleration(torpedo)
            # Sets speed for asteroids to part ways
            new_asteroid.set_split_ways(self.SPLIT_VALUES[i])
            self._screen.register_asteroid(new_asteroid,
                                           new_asteroid.get_size())
            self.__asteroids.append(new_asteroid)
        self.__destroy_asteroid(asteroid)

    def interact_user_input(self):
        """
        This method interacts with user input on key presses
        using Screen methods. It comprises of if conditions, each responds
        according to user's input.
        If user pressed 'left' - ship turns left
        If user pressed 'right' - ship turns right
        if user pressed 'up' - ship accelerates
        if user pressed 'space' - torpedo is launched
        """
        if self._screen.is_left_pressed():
            self.ship.turn_left()
        if self._screen.is_right_pressed():
            self.ship.turn_right()
        if self._screen.is_up_pressed():
            self.ship.accelerate()
        if self._screen.is_space_pressed():
            self.set_torpedo()

    def asteroid_sequence(self):
        """
        This initiates asteroids sequence in game loop.
        For each loop method will:
        Draw asteroids to screen, adjust their movement, check if asteroids
        had collision with ship and if it did will send to to corresponding method
        and then will destroy the asteroid.
        """
        for asteroid in self.__asteroids:
            self._screen.draw_asteroid(asteroid, asteroid.get_x(),
                                       asteroid.get_y())
            asteroid.move()

            if asteroid.has_intersection(self.ship):
                self.ship_asteroid_collision()
                self.__destroy_asteroid(asteroid)

    def torpedo_sequence(self):
        """
        This initiates torpedoes sequence in game loop.
        For each loop method will:
        Draw torpedoes to screen, adjust their movement, check if a torpedo
        hit an asteroid.
        If hit:
        1) will update user score.
        2) will split asteroids if hit asteroid is bigger than one.
        3) destroy the asteroid.
        4) disarm torpedo - del from dict. and un-register from screen.
        In any case, it will subtract one "life"(life=loop) from torpedo
        remaining lifetime and will disarm it if reached zero.
        """
        # listed the items in dict to be able to change dict size within loop
        for torpedo, rounds in list(self.__torpedoes.items()):
            self._screen.draw_torpedo(torpedo, torpedo.get_x(),
                                      torpedo.get_y(), torpedo.get_heading())
            torpedo.move()
            exploded = False
            for asteroid in self.__asteroids:
                if asteroid.has_intersection(torpedo):
                    self.update_score(asteroid.get_size())
                    if asteroid.get_size() >= self.MIN_SPLIT_SIZE:
                        self.split_asteroid(asteroid, torpedo)
                    else:
                        self.__destroy_asteroid(asteroid)
                    exploded = True
            rounds -= 1
            if rounds == 0 or exploded:
                self.__disarm_torpedo(torpedo)

    def check_game_status(self):
        """
        This method checks game status.
        It will respond with a suiting msg and end the game for the following scenarios:
        1) user pressed "q" button - user wants to quit game
        2) no more asteroids left - win scenario
        3) no more ship lives left - lose scenario
        """
        title, msg = "", ""
        if self._screen.should_end():
            title, msg = self.TITLE_QUIT_GAME, self.MSG_QUIT_GAME
        if not self.__asteroids:
            title, msg = self.TITLE_WIN, self.MSG_WIN + str(self.get_score())
        elif self.__ship_life == self.DEAD:
            self.end_game(self.TITLE_LOST, self.MSG_LOST)
        if title:
            self.end_game(title, msg)

    def update_score(self, asteroid_size):
        """
        This method updates and keeps track of user score.
        It will set new score after hitting an asteroid according to points dict,
        and will update score on screen.
        :param asteroid_size: hit asteroid's size
        :type asteroid_size: int
        """
        points = self.INTERCEPTION_POINTS[asteroid_size]
        self.__score += points
        self._screen.set_score(self.__score)

    def end_game(self, title, msg):
        """
        This method will end the game with an informative msg as given in param
        according to scenarios listed in check game status method,
        and end the game (exit GUI).
        :param title: title for windowed msg
        :param msg: msg for windowed msg
        """
        self._screen.show_message(title, msg)
        self._screen.end_game()
        sys.exit()

    def run(self):
        self._do_loop()
        self._screen.start_screen()

    def _do_loop(self):
        # You don't need to change this method!
        self._game_loop()

        # Set the timer to go off again
        self._screen.update()
        self._screen.ontimer(self._do_loop,5)

    def _game_loop(self):
        """
        This method is the game loop. it runs on set times and so reacting
        passively to user.
        For each loop this method:
        1) Draws the ship on screen and adjusts ship movement.
        2) Initiates asteroid sequence.
        3) Initiates torpedo sequence.
        4) Checks game status.
        """
        self._screen.draw_ship(self.ship.get_x(),
                               self.ship.get_y(), self.ship.get_heading())
        self.interact_user_input()
        self.ship.move()
        self.asteroid_sequence()
        self.torpedo_sequence()
        self.check_game_status()

############################################################
# MAIN
############################################################


def main(amnt):
    """
    main func. runs game.
    :param amnt: number of asteroids
    """
    runner = GameRunner(amnt)
    runner.run()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main( int( sys.argv[1] ) )
    else:
        main( DEFAULT_ASTEROIDS_NUM )
