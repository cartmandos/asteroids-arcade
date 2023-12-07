############################################################
# FILE : game.py

# DESCRIPTION: In this file: class Game.
# methods incl.: constructor, repr, remove ship, remove bomb, bomb rounds updater
# and main game play methods: __play_one_round comprised of sub-functions
# for one round of the game, and play to run game.
############################################################
# Imports
############################################################
import game_helper as gh

############################################################
# Class definition
############################################################


class Game:
    """
    A class representing a battleship game.
    A game is composed of ships that are moving on a square board and a user
    which tries to guess the locations of the ships by guessing their
    coordinates.
    """
    BOMB_NUM_OF_ROUNDS = 3
    INITIAL_EXPLODED_POSITIONS = []

    def __init__(self, board_size, ships):
        """
        Initialize a new Game object.
        :param board_size: Length of the side of the game-board.
        :param ships: A list of ships (of type Ship) that participate in the
            game.
        :return: A new Game object with data of board size, list of Ship objects
        and a dictionary of bombs with keys as positions and item value as turns
        left ob board.
        """
        self.board_size = board_size
        self.ships = ships
        self.bombs = dict()

    def remove_ship(self, ship):
        """removes ship from Game object's ship list"""
        self.ships.remove(ship)

    def del_bomb(self, bomb):
        """removes bomb from Game object's bomb dict"""
        del self.bombs[bomb]

    def update_bomb_round(self, bomb):
        """updates bomb's remaining rounds"""
        self.bombs[bomb] -= 1

    def assess_damage(self):
        """Method assess damage to cells of ships in ship list.
        :returns a list of not hit cells and hit cells."""
        hit_cells, not_hit_cells = list(), list()
        for ship in self.ships:
            for cell in ship.coordinates():
                if ship.cell_status(cell) and cell not in hit_cells:
                    hit_cells.append(cell)
                elif cell not in not_hit_cells:
                    not_hit_cells.append(cell)
        return not_hit_cells, hit_cells

    def __play_one_round(self):
        """
        Note - this function is here to guide you and it is *not mandatory*
        to implement it. The logic defined by this function must be implemented
        but if you wish to do so in another function (or some other functions)
        it is ok.

        The function runs one round of the game :
            1. Get user coordinate choice for bombing.
            2. Move all game's ships.
            3. Update all ships and bombs.
            4. Report to the user the result of current round (number of hits and
             terminated ships)
        :return:
            (some constant you may want implement which represents) Game status:
            GAME_STATUS_ONGOING if there are still ships on the board or
            GAME_STATUS_ENDED otherwise.
        """
        def move_and_detonate():
            """
            Function moves all undamaged ships, detonates bombs if hit by ship.
            :returns hits counter and exploded positions on board (coordinates list).
            """
            hits = 0
            exploded = list()
            for ship in self.ships:
                # move ship if no ship cells are damaged
                if not ship.damaged_cells():
                    ship.move()
                for bomb in self.bombs:
                    if ship.hit(bomb):
                        hits += 1
                        if bomb not in exploded:
                            exploded.append(bomb)
            return hits, exploded

        def update_bombs():
            """
            Function updates bombs in current round and delete bombs that
            have exploded or expired.
            """
            for bomb, rounds_left in list(self.bombs.items()):
                if bomb in exploded_list or rounds_left - 1 == 0:
                    # rounds_left is value before update
                    self.del_bomb(bomb)
                    continue
                if bomb != target:
                    self.update_bomb_round(bomb)

        def update_ships_status():
            """
            Removes all terminated ships and counts them.
            :return: terminated ships counter in current round
            """
            terminations = 0
            for ship in self.ships:
                if ship.terminated():
                    self.remove_ship(ship)
                    terminations += 1
            return terminations

        # asks target input from user and sets bomb on game board
        target = gh.get_target(self.board_size)
        self.bombs[target] = self.BOMB_NUM_OF_ROUNDS
        # moves all not hit ships and detonates bomb,
        # then updates bomb remaining turns
        hits_counter, exploded_list = move_and_detonate()
        update_bombs()
        # assess damage done to ships and builds lists of hit & not hit positions
        not_hit_cells, hit_cells = self.assess_damage()
        print(gh.board_to_string(self.board_size, exploded_list,
                                 self.bombs, hit_cells, not_hit_cells))
        # checks ships to remove from board and counts terminations
        terminated = update_ships_status()
        gh.report_turn(hits_counter, terminated)

    def __repr__(self):
        """
        Return a string representation of the board's game.
        :return: A tuple converted to string (that is, for a tuple x return
            str(x)). The tuple should contain (maintain
        the following order):
            1. Board's size.
            2. A dictionary of the bombs found on the board, mapping their
                coordinates to the number of remaining turns:
                 {(pos_x, pos_y) : remaining turns}
                For example :
                 {(0, 1) : 2, (3, 2) : 1}
            3. A list of the ships found on the board (each ship should be
                represented by its __repr__ string).
        """
        return str((self.board_size, self.bombs, [ship for ship in self.ships]))

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        gh.report_legend()
        not_hit_cells, hit_cells = self.assess_damage()
        print(gh.board_to_string(self.board_size, self.INITIAL_EXPLODED_POSITIONS,
                                 self.bombs, hit_cells, not_hit_cells))
        while self.ships:
            self.__play_one_round()
        gh.report_gameover()


############################################################
# An example usage of the game
############################################################
if __name__ == "__main__":
    game = Game(5, gh.initialize_ship_list(4, 2))
    game.play()
