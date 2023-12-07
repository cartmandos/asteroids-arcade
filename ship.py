############################################################
# FILE : ship.py

# DESCRIPTION: This File contains class Ship for the game Asteroids!.
# Ship class has getters for all args, and radius getter (const.),
# other method are for ship's movement in the 2D game -
# turning (degrees), accelerating and moving.
############################################################
# Imports
############################################################
import math
############################################################
# Ship class
############################################################


class Ship:
    """
    A class representing a ship in Asteroids! game.
    A ship travels, accelerates and turns clockwise on screen in 2D and when
    getting to screen borders appears from the other end as if screen is has no borders.
    Ship can launch torpedo against asteroids.
    Note that ship has NO SPEED LIMIT.
    Ship's Radius is a const.
    Degrees for urning the ship are defined with TURN_RIGHT_DEGREE, TURN_LEFT_DEGREE.
    consts AXIS_X, AXIS_Y, MIN, MAX are used for the structural implementation
    of object's bounds arg.
    """
    AXIS_X = 0
    AXIS_Y = 1
    MIN = 0
    MAX = 1
    RADIUS = 1
    SHIP_INITIAL_DEGREE = 0
    SHIP_INITIAL_SPEED = (0, 0)
    TURN_RIGHT_DEGREE = -7
    TURN_LEFT_DEGREE = 7

    def __init__(self, pos, bounds):
        """
        Asteroid object constructor
        :param pos: location on 2d matrix as (x, y)
        :type pos: tuple
        :param bounds: a list containing two tuples for each axis,
        each tuple incl. min and max values for screen bounds.
        for ex. [(min_x, max_x), (min_y, max_y)]
        :type bounds: list
        :return: a new Ship obj. with given params, and also speed and heading
        as defined in initial consts.
        """
        self.__pos = pos
        self.__speed = self.SHIP_INITIAL_SPEED
        self.__heading = self.SHIP_INITIAL_DEGREE
        self.bounds = bounds

    def get_coordinates(self):
        """
        Ship's coordinates getter
        :return: ship pos arg (tuple)
        """
        return self.__pos

    def get_speed(self):
        """
        Ship's speed getter
        :return: ship speed arg (tuple)
        """
        return self.__speed

    def get_heading(self):
        """
        Ship's heading getter
        :return: ship heading arg (in degrees)
        """
        return self.__heading

    def get_x(self):
        """
        Ship's Y coordinate getter
        :return: Y coordinate of ship's position
        """
        return self.__pos[self.AXIS_X]

    def get_y(self):
        """
        Ship's Y coordinate getter
        :return: Y coordinate of ship's position
        """
        return self.__pos[self.AXIS_Y]

    def get_radius(self):
        """
        Ship radius getter
        note: This is not an arg of Ship class.
        :return: a const (number) defining ship's radius
        """
        return self.RADIUS

    def turn_right(self):
        """
        Turns the ship right (clockwise) with predefined degrees in class consts,
        by adding const.(pos number) to current heading.
        """
        self.__heading += self.TURN_RIGHT_DEGREE

    def turn_left(self):
        """
        Turns the ship left (counter-clockwise) with predefined degrees in class
        consts, by adding const.(neg number) to current heading.
        """
        self.__heading += self.TURN_LEFT_DEGREE

    def get_new_coordinate(self, axis, axis_bounds):
        """
        This method defines object's movement in the game with
        a formula each coordinate and its axis:
        new coord = speed + old coord - AxisMinCoord) % AXIS DIFFERENCE + AxisMinCoord
        AXIS DIFFERENCE defined: AxisMaxCoord - AxisMinCoord
        while AxisMinCoord & AxisMaxCoord are the min & max bounds in the game.
        :param axis: a const (AXIS_X or AXIS_Y) as defined in class consts
        :param axis_bounds: the bounds of the specific axis, a tuple for the axis
        :type axis_bounds: tuple
        from object's bounds arg.
        :return: new coordination according to formula within a given axis, x or y.
        """
        dif_axis = axis_bounds[self.MAX] - axis_bounds[self.MIN]
        new_coord = (self.__speed[axis] + self.__pos[axis] - axis_bounds[self.MIN]) % dif_axis + axis_bounds[self.MIN]
        return new_coord

    def move(self):
        """
        Method sets ship's new position as calculated in get_new_coordinate.
        """
        new_coord_x = self.get_new_coordinate(self.AXIS_X, self.bounds[self.AXIS_X])
        new_coord_y = self.get_new_coordinate(self.AXIS_Y, self.bounds[self.AXIS_Y])
        self.__pos = (new_coord_x, new_coord_y)

    def degree_to_rad(self):
        """
        this helper method converts degrees to radians
        :return: heading of ship in radians
        """
        return self.__heading * (math.pi / 180)

    def accelerate(self):
        """
        This method accelerates the ship's speed, and sets new speed.
        Formula for each axis:
        Axis X: new speed = current speed + cos(heading in rad)
        Axis X: new speed = current speed + sin(heading in rad)
        """
        new_x_speed = self.__speed[self.AXIS_X] + math.cos(self.degree_to_rad())
        new_y_speed = self.__speed[self.AXIS_Y] + math.sin(self.degree_to_rad())
        self.__speed = (new_x_speed, new_y_speed)
