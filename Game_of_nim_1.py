Python 3.11.1 (tags/v3.11.1:a7a450f, Dec  6 2022, 19:58:39) [MSC v.1934 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
from games import *

class GameOfNim(Game):
    """Play Game of Nim with first player 'MAX'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (r, n) positions, and a board, in the form of
    a list with number of objects in each row."""
    
    def __init__(self, board=[3, 1]):
        super().__init__()
        self.initial = self.GameState(board)
    
    class GameState:
...         def __init__(self, board, to_move='MAX'):
...             self.board = board
...             self.to_move = to_move
...             self.moves = self.generate_moves()
... 
...         def generate_moves(self):
...             valid_moves = []
...             for r in range(len(self.board)):
...                 for n in range(1, self.board[r] + 1):
...                     valid_moves.append((r, n))
...             return valid_moves
... 
...     def actions(self, state):
...         """Legal moves are at least one object, all from the same row."""
...         return state.moves
... 
...     def result(self, state, move):
...         """Returns the new state after the given move is applied."""
...         row, count = move
...         new_board = state.board.copy()
...         new_board[row] -= count
...         next_to_move = 'MIN' if state.to_move == 'MAX' else 'MAX'
...         return self.GameState(new_board, next_to_move)
... 
...     def utility(self, state, player):
...         """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
...         if self.terminal_test(state):
...             return 1 if player != state.to_move else -1
...         return 0
... 
...     def terminal_test(self, state):
...         """A state is terminal if there are no objects left."""
...         return all(x == 0 for x in state.board)
... 
...     def display(self, state):
...         """Display the current state of the board."""
...         print("board: ", state.board)
... 
... if __name__ == "__main__":
...     nim = GameOfNim(board=[0, 5, 3, 1])  # Creating the game instance
...     print(nim.initial.board)  # must be [0, 5, 3, 1]
...     print(nim.initial.moves)  # must be [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 1), (2, 2), (2, 3), (3, 1)]
...     
...     new_state = nim.result(nim.initial, (1, 3))
...     print(new_state.board)  # After the move (1, 3)
... 
...     utility = nim.play_game(alpha_beta_player, query_player)  # computer moves first
...     if utility < 0:
...         print("MIN won the game")
...     else:
