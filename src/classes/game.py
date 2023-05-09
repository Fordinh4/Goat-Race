# ----------------------------------------------------
# Game implementation
# ----------------------------------------------------


from typing import List
from .goat import Goat
from .board import Board
from .player import Player

GOATS_PER_PLAYER = 4
WINNING_NUMBER_GOATS = 3
VALID_COLUMNS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
SIDE_JUMP_SIZE = 1
FORWARD_JUMP_SIZE = 1


class Game:
    '''
    Represents the Goat Race game
    '''

    ################################################
    #
    # The following methods MUST be in your solution
    # 
    ################################################
    def __init__(self, width: int, height: int, obstacle_positions: List = []):
        '''Initializes the game'''

        self.board = Board(width, height, obstacle_positions)
        self.players = []
        self.phase = 1
        self.turn = 0

    def __str__(self) -> str:
        '''Returns a visual snapshot of the game'''
        temp_players = []

        temp_str = str(self.board)
        for player in self.players:
            temp_players.append(player.check_color())
        temp_str += "Players: {}\n".format(", ".join(temp_players))
        temp_str += "Phase: {}\n".format(self.phase)
        temp_str += 'Player whose turn it is: {}\n'.format(self.players[self.turn].color)

        return temp_str

    def get_phase(self) -> int:
        '''Returns the game phase'''
        return self.phase

    def get_turn(self) -> int:
        '''Returns the index of the player whose turn it is'''
        return self.turn

    def get_current_player(self) -> Player:
        '''Returns the current player'''
        return self.players[self.turn]

    def get_goats_blocked(self, player: Player) -> int:
        '''Returns the number of goats blocked for a given player'''

        goats_blocked = 0
        fmt_obstacles = []

        # Change the location of the obstacle from (3, "C") to (2, 2)
        for obstacle in self.board.obstacle_positions:
            fmt_obstacles.append((obstacle[0] - 1, VALID_COLUMNS.index(obstacle[1])))

        for goat in player.goats:
            # Have the location for each goat that the player have
            row, col = goat.check_location()

            if col == self.board.get_width():
                # Check if the goat in the last column
                goats_blocked += 1

            elif (row, col) != self.board.get_board()[row][col].peek().check_location():
                # Check if the current goat is at the top of the stack or under other goat
                goats_blocked += 1


            elif (row, col + 1) in fmt_obstacles and (row - 1, col) in fmt_obstacles and (
                    row + 1, col) in fmt_obstacles:
                # Check three conditions which the goat stuck in all three direction - up, down, and forward then
                # it's consider block. Else it's not!
                goats_blocked += 1

        return goats_blocked

    def get_goats_per_player(self) -> List[int]:
        '''Return a list that contains the number of goats per player.'''
        num_goats = []
        for player in self.players:
            num_goats.append(player.check_goatsNumber())

        return num_goats

    def set_phase(self, phase: int) -> None:
        '''Sets the game phase'''
        self.phase = phase

    def set_turn(self, turn: int) -> None:
        '''Sets the game turn'''
        self.turn = turn

    def add_player(self, player: Player) -> None:
        '''Adds a player to the list of players'''
        self.players.append(player)

    def add_goat(self, row: int, column: str) -> None:
        '''Add goat to stack in given location (row, column).'''

        try:
            goat = Goat(self.get_current_player().color)
            goat.set_row(row)
            goat.set_column(column)

        except:
            raise Exception("Cannot add a goat to the given location!")

        else:
            self.board.get_board()[row - 1][VALID_COLUMNS.index(column)].push(goat)
            self.get_current_player().add_goat(goat)

    def move_sideways(self, move):
        '''Executes sideways move if valid '''

        # CHECK IF VALID:
        initial_row = move[0][0] - 1
        initial_column = VALID_COLUMNS.index(move[0][1])
        final_row = move[1][0] - 1
        final_column = VALID_COLUMNS.index(move[1][1])
        fmt_obstacles = []

        for obstacle in self.board.obstacle_positions:
            # Change the location of the obstacle from (3, "C") to (2, 2)
            fmt_obstacles.append((obstacle[0] - 1, VALID_COLUMNS.index(obstacle[1])))

        if (initial_row, initial_column) != self.board.get_board()[initial_row][initial_column].peek().check_location():
            # Check if the current goat is the top goat or not.
            raise Exception("Your goat is not on the top!")

        elif self.board.get_board()[initial_row][initial_column].peek().color != self.players[self.turn].check_color():
            # Check if the player choose to move other players' goat or not!
            raise Exception("You cannot move other player goat!")

        elif abs(final_row - initial_row) != SIDE_JUMP_SIZE:
            # To make sure it can only move one block up or down.
            raise Exception(f"You can only jump {SIDE_JUMP_SIZE} block up or down!")

        elif not (0 <= final_row < self.board.get_height()):
            # To make sure it stay inside the board
            raise Exception("You step outside of the board!")

        elif (final_row, final_column) in fmt_obstacles:
            # To make sure it cannot move onto an obstacle.
            raise Exception("You cannot jump on an obstacle!")

        # EXECUTE THE MOVE:
        # I pop the goat on the current location
        current_goat = self.board.get_board()[initial_row][initial_column].pop()

        # Set the new row for the current goat
        # I add 1 because in the set_row(), since I set -1 of set_row in the goat.py.
        current_goat.set_row(final_row + 1)

        # Then push that goat to the new location!
        self.board.get_board()[final_row][final_column].push(current_goat)

    def move_forward(self, move, dice_outcome):
        '''Executes forward move if valid '''

        initial_row = move[0][0] - 1
        initial_column = VALID_COLUMNS.index(move[0][1])
        final_row = move[1][0] - 1
        final_column = VALID_COLUMNS.index(move[1][1])
        fmt_obstacles = []

        for obstacle in self.board.obstacle_positions:
            # Change the location of the obstacle from (3, "C") to (2, 2)
            fmt_obstacles.append((obstacle[0] - 1, VALID_COLUMNS.index(obstacle[1])))

        if initial_row != dice_outcome - 1:
            # A player can only move forward a goat that is on the same row as the dice outcome
            raise Exception("Your goat is not on the same row as the dice outcome!")

        elif (initial_row, initial_column) != self.board.get_board()[initial_row][
            initial_column].peek().check_location():
            # Check if the current goat is the top goat or not.
            raise Exception("Your goat is not on the top!")

        elif initial_row != final_row:
            raise Exception("You can only move forward in the same row!")

        elif abs(final_column - initial_column) != FORWARD_JUMP_SIZE:
            # To make sure it can only move one block forward.
            raise Exception(f"You can only jump {FORWARD_JUMP_SIZE} block forward!")

        elif not (0 <= final_column < self.board.get_width()):
            # To make sure it stay inside the board
            raise Exception("You step outside of the board!")

        elif (final_row, final_column) in fmt_obstacles:
            # To make sure it cannot move onto an obstacle.
            raise Exception("You cannot jump on an obstacle!")

        # EXECUTE THE MOVE:
        # I pop the goat on the current location
        current_goat = self.board.get_board()[initial_row][initial_column].pop()

        # Set the new row and new column for the current goat
        # I add 1 because in the set_row(), since I set -1 of set_row in the goat.py.
        current_goat.set_row(final_row + 1)
        current_goat.set_column(final_column)

        # Then push that goat to the new location!
        self.board.get_board()[final_row][final_column].push(current_goat)

    def check_row(self, row: int) -> None:
        '''Checks if a row is valid'''
        if not (0 <= row - 1 < self.board.get_height()):
            raise Exception("Please enter the valid row!")

    def check_valid_move_format(self, move: List) -> None:
        '''Checks if the given location is an appropriate list of tuples'''

        for location in move:
            if type(location) != tuple:
                raise Exception("Please enter the correct format!")
            elif not (0 <= location[0] - 1 < self.board.get_height()):
                raise Exception("Please enter the correct row!")
            elif location[1] not in VALID_COLUMNS:
                raise Exception("Please enter the correct column!")

    def check_nonempty_row(self, row) -> bool:
        '''Returns whether there are non-blocked goats in a row'''
        fmt_obstacles = []

        # Change the location of the obstacle from (3, "C") to (2, 2)
        for obstacle in self.board.obstacle_positions:
            fmt_obstacles.append((obstacle[0] - 1, VALID_COLUMNS.index(obstacle[1])))

        for col in range(self.board.get_width() - 1):
            # -1 to avoid checking the last column which is the finish line

            if not self.board.get_board()[row - 1][col].isEmpty():
                goat_row, goat_col = self.board.get_board()[row - 1][col].peek().check_location()

                if (goat_row, goat_col + 1) not in fmt_obstacles:
                    # Run the for loop until it meet any goat that can move forward
                    return True

        # If after the for loop and there are no goats that can jump forward or the row is empty, return False
        return False

    def check_starting_goat_placement(self, row: int) -> bool:
        '''Checks that goat is not placed in a high stack'''

        check = True
        temp_len_stack = []
        board = self.board.get_board()

        # Append all the len of stack in the first column to find the min
        for i in range(len(board)):
            temp_len_stack.append(board[i][0].size())

        # Check if the given row is larger then the min of that column -> False
        if board[row - 1][0].size() > min(temp_len_stack):
            check = False

        return check

    def check_winner(self) -> bool:
        '''
            Returns whether one player has won by getting 
            the necessary goats to the Destination
        '''
        # Check the goats for every player
        for player in self.players:
            count_win_goat = 0

            for goat in player.goats:
                if goat.column == self.board.get_width() - 1:
                    # If any goat reach the final column -> increase the count
                    count_win_goat += 1

            if count_win_goat == WINNING_NUMBER_GOATS:
                # If there are three goats at the last column
                return True
        return False

    def check_tie(self) -> bool:
        '''
            Returns whether there is a tie since 
            no player has possible moves
        '''
        count = 0
        # Check if each player have the goat blocked equal to the goat per player which is 4 -> count + 1
        for player in self.players:
            if self.get_goats_blocked(player) == GOATS_PER_PLAYER:
                count += 1

        # If the count (players that cannot move their goats) = to the current amount of player -> return True or
        # it's mean tie!
        return count == len(self.players)

    ################################################
    #
    # The following methods do NOT need to be
    # included in your solution, but they might
    # give you an idea of possible useful methods
    # to include.
    # 
    ################################################
    def get_goats_blocked_per_player(self) -> List[int]:
        '''
            Returns a list that contains the number 
            of goats blocked per player.
        '''
        pass

    def get_starting_gate_sizes(self) -> List[int]:
        '''
            Returns a list containing how many goats
            are in each row of the starting gate
        '''
        pass

    def get_top_goat(self, row: int, column: str) -> Goat:
        '''
            Obtains a goat at a specific location
            Inputs:
                - row: the row where the goat will be obtained from
                - column: the column where the goat will be obtained from
            Returns:
                The goat at the top of the stack in the specified location
        '''
        pass

    def get_goats_destination_per_player(self, destination: str) -> List[int]:
        '''
            Return a list that contains the number 
            of goats per player in the destination.
        '''
        pass

    def check_column(self, column: str) -> None:
        '''Checks if a column is valid'''

        pass

    def check_location(self, location) -> None:
        ''' Checks if location is in the board'''

        pass

    def check_jump(self, row: int, column: str) -> None:
        '''Checks if available stack to jump'''

        pass

    def check_forward_move(self, forward_move: List, dice_outcome: int) -> None:
        '''
            Checks if player can move goat forward
            Inputs:
                - forward_move: list with tuple of initial and final locations
                - dice_outcome: dice outcome (integer between 1 and 6)
        '''
        pass

    def check_sideways_move(self, sideways_move: List[tuple]) -> None:
        '''
            Checks if player can move goat sideways
            Inputs:
                - forward_move: list with tuple of initial and final locations
        '''
        pass

    def check_same_color(self, row: int, column: str) -> None:
        '''
            Checks if the color of the current 
            player and the goat on top coincide
        '''
        pass

    def move_goat(self, move: List) -> None:
        '''
            Lets a goat jump in the board
            Inputs:
                - move: list with tuple of initial and final locations
        '''
        pass 


if __name__ == '__main__':
    pass
