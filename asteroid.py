############################################################
# FILE : asteroid.py

# DESCRIPTION: This file contains Asteroid class, objects represents
# asteroids in the Asteroids! game. Asteroids have several args
# defining its 2d configuration, note that speed and position are
# defined for 2d.
# Methods in class are getters, unique speed setter that only multiplies
# current speed with given value, this is for parting ways for splitting asteroids.
# Other method involved in basic repositioning (move), checking for a collision
# with other obj in the game, and re-adjust speed due to a collision.
############################################################
# Asteroid class
############################################################


class Asteroid:
    """
    Class representing Asteroid in 2D world.
    consts AXIS_X, AXIS_Y, MIN, MAX are used for the structural implementation
    of object's bounds arg.
    """
    AXIS_X = 0
    AXIS_Y = 1
    MIN = 0
    MAX = 1
    NORMALIZING_FACTOR = -5
    SIZE_COEFFICIENT = 10

    def __init__(self, pos, speed, size, bounds):
        """
        Asteroid object constructor
        :param pos: location on 2d matrix as (x, y)
        :type pos: tuple
        :param speed: Asteroid's speed on 2d matrix, (x, y)
        :type speed: tuple
        :param size: Size of asteroid, integer in the neighborhood of [1, 3]
        :type size: int
        :param bounds: a list containing two tuples for each axis,
        each tuple incl. min and max values for screen bounds.
        for ex. [(min_x, max_x), (min_y, max_y)]
        :type bounds: list
        """
        self.__pos = pos
        self.__speed = speed
        self.__size = size
        self.bounds = bounds

    def get_coordinates(self):
        """
        Asteroid coordinates getter
        :return: Asteroid pos arg (tuple)
        """
        return self.__pos

    def get_size(self):
        """
        Asteroid size getter
        :return: Asteroid size arg (int)
        """
        return self.__size

    def get_speed(self):
        """
        Asteroid speed getter
        :return: Asteroid speed arg (tuple)
        """
        return self.__speed

    def get_x(self):
        """
        Asteroid's X coordinate getter
        :return: X coordinate of asteroid's position
        """
        return self.__pos[self.AXIS_X]

    def get_y(self):
        """
        Asteroid's Y coordinate getter
        :return: Y coordinate of asteroid's position
        """
        return self.__pos[self.AXIS_Y]

    def get_radius(self):
        """
        Asteroid radius getter
        note: This is not an arg of Asteroid class.
        :return: the radius of the asteroid.
        Radius is calculated by the following formula:
        RADIUS = (ASTEROID SIZE * SIZE_COEFFICIENT) - NORMALIZING FACTOR
        """
        return (self.get_size() * self.SIZE_COEFFICIENT) - self.NORMALIZING_FACTOR

    def set_split_ways(self, split_value):
        """
        method sets and changes asteroid speed by multiplying with a given
        multiplication factor in order to part directions of splitting asteroids.
        :param split_value: multiplication factor
        """
        self.__speed = self.__speed[self.AXIS_X] * split_value, \
                       self.__speed[self.AXIS_Y] * split_value

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
        Method sets asteroid's new position as calculated in get_new_coordinate.
        """
        new_coord_x = self.get_new_coordinate(self.AXIS_X, self.bounds[self.AXIS_X])
        new_coord_y = self.get_new_coordinate(self.AXIS_Y, self.bounds[self.AXIS_Y])
        self.__pos = (new_coord_x, new_coord_y)

    def has_intersection(self, obj):
        """
        This method checks if an object had a collision with the asteroid.
        The check is based on the condition that the distance is less/equal
        than/to the sum of asteroid's radius and object's radius.
        Distance formula: ((obj.x_coord - asteroid.x_coord)**2 +
        (obj.y_coord - asteroid.y_coord)**2)**0.5
        :param obj: object of Ship class (but could be implemented for other obj)
        :return: True - object has collided with asteroid, False - else.
        """
        distance = ((obj.get_x() - self.get_x())**2
                    + (obj.get_y() - self.get_y())**2)**0.5
        if distance <= self.get_radius() + obj.get_radius():
            return True
        return False

    def collision_acceleration(self, obj):
        """
        This method defines and sets asteroid's new speed in case of a collision.
        Specifically, it is designed to set new speed values for a splitted
        asteroid, caused by a hit from a torpedo.
        New speed is calculated (for each axis):
        new speed = (torpedo speed + asteroid current speed) / formula divisor
        formula divisor = ((asteroid current speed_x coord)**2 +
        (asteroid current speed_y coord))**0.5
        :param obj: object of Torpedo class
        """
        formula_divisor = ((self.__speed[self.AXIS_X])**2 + (self.__speed[self.AXIS_Y])**2)**0.5
        new_x_speed = (obj.get_speed()[self.AXIS_X] +
                       self.__speed[self.AXIS_X]) / formula_divisor
        new_y_speed = (obj.get_speed()[self.AXIS_Y] +
                       self.__speed[self.AXIS_Y]) / formula_divisor
        self.__speed = (new_x_speed, new_y_speed)
