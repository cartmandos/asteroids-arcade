############################################################
# FILE : torpedo.py

# DESCRIPTION: This file contains Torpedo class, objects represents
# torpedoes in the Asteroids! game. Torpedoes have position, heading (in degrees)
# and speed that is accelerating depending on ship's speed, launched at init.
# Methods in class are getters, movement method for re-positioning and a method
# to launch (accelerate speed).
############################################################
# Imports
############################################################
import math
############################################################
# Torpedo class
############################################################


class Torpedo:
    """
    Class representing Torpedo in 2D world.
    consts AXIS_X, AXIS_Y, MIN, MAX are used for the structural implementation
    of object's bounds arg.
    Torpedo's RADIUS is a const.
    """
    AXIS_X = 0
    AXIS_Y = 1
    MIN = 0
    MAX = 1
    RADIUS = 4
    INITIAL_SPEED = (0, 0)
    ACCELERATION_FACTOR = 2

    def __init__(self, pos, heading, speed, bounds):
        """
        Torpedo object constructor
        Torpedo is launched by launch method at initialization according to
        speed given in param.
        Note that speed DOES NOT change after constructed.
        :param pos: location on 2d matrix as (x, y)
        :type pos: tuple
        :param heading: Torpedo's heading in degrees
        :param speed: initial speed, specifically ship's speed when launched
        speed is defined on 2D matrix, (x, y)
        :type speed: tuple
        :param bounds: a list containing two tuples for each axis,
        each tuple incl. min and max values for screen bounds.
        for ex. [(min_x, max_x), (min_y, max_y)]
        :type bounds: list
        """
        self.__pos = pos
        self.__heading = heading
        self.__speed = self.launch(speed)
        self.bounds = bounds

    def get_speed(self):
        """
        Torpedo speed getter
        :return: torpedo's speed arg (tuple)
        """
        return self.__speed

    def get_heading(self):
        """
        Torpedo heading getter
        :return: torpedo's heading arg (in degrees)
        """
        return self.__heading

    def get_radius(self):
        """
        Torpedo radius getter
        note: This is not an arg of Torpedo class.
        :return: a const (number) defining torpedo's radius
        """
        return self.RADIUS

    def get_x(self):
        """
        Torpedo's X coordinate getter
        :return: X coordinate of torpedo's position
        """
        return self.__pos[self.AXIS_X]

    def get_y(self):
        """
        Torpedo's Y coordinate getter
        :return: Y coordinate of torpedo's position
        """
        return self.__pos[self.AXIS_Y]

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
        new_coord = self.__pos[axis]
        dif_axis = axis_bounds[self.MAX] - axis_bounds[self.MIN]
        new_coord = (self.__speed[axis] + new_coord - axis_bounds[self.MIN]) \
            % dif_axis + axis_bounds[self.MIN]
        return new_coord

    def move(self):
        """
        Method sets torpedo's new position as calculated in get_new_coordinate.
        """
        new_coord_x = self.get_new_coordinate(self.AXIS_X, self.bounds[self.AXIS_X])
        new_coord_y = self.get_new_coordinate(self.AXIS_Y, self.bounds[self.AXIS_Y])
        self.__pos = (new_coord_x, new_coord_y)

    def degree_to_rad(self):
        """
        this helper method converts degrees to radians
        :return: heading of torpedo in radians
        """
        return self.__heading * (math.pi / 180)

    def launch(self, speed):
        """
        This method launches the torpedo when Torpedo constructs new object,
        and accelerate speed according to the following formula:
        AXIS X SPEED:
            new speed_x = speed param_x + ACCELERATION FACTOR * cos(heading in radians)
        AXIS Y SPEED:
            new speed_y = speed param_y + ACCELERATION FACTOR * sin(heading in radians)
        ACCELERATION FACTOR: a const defining accelerating factor, defined in class as 2.
        :param speed: speed param given from constructor,
        ship's speed in (x, y) format.
        :return: new speed after launching in (x, y) format
        """
        new_x_speed = speed[self.AXIS_X]\
                      + (self.ACCELERATION_FACTOR * math.cos(self.degree_to_rad()))
        new_y_speed = speed[self.AXIS_Y] \
                      + (self.ACCELERATION_FACTOR * math.sin(self.degree_to_rad()))
        return new_x_speed, new_y_speed
