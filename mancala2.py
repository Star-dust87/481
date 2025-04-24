import sys
import random
from copy import deepcopy
import time

# Game constants
PLAYER_1_PITS = ('A', 'B', 'C', 'D', 'E', 'F')
PLAYER_2_PITS = ('G', 'H', 'I', 'J', 'K', 'L')
OPPOSITE_PIT = {'A': 'G', 'B': 'H', 'C': 'I', 'D': 'J', 'E': 'K',
                'F': 'L', 'G': 'A', 'H': 'B', 'I': 'C', 'J': 'D',
                'K': 'E', 'L': 'F'}
NEXT_PIT = {'A': 'B', 'B': 'C', 'C': 'D', 'D': 'E', 'E': 'F', 'F': '1',
            '1': 'L', 'L': 'K', 'K': 'J', 'J': 'I', 'I': 'H', 'H': 'G',
            'G': '2', '2': 'A'}
PIT_LABELS = 'ABCDEF1LKJIHG2'
STARTING_NUMBER_OF_SEEDS = 4

class MancalaGame:
    def __init__(self):
        self.board = self.get_new_board()
        self.current_player = '1'
        
    def get_new_board(self):
        """Return a new Mancala board in starting position"""
        return {pit: STARTING_NUMBER_OF_SEEDS for pit in PLAYER_1_PITS + PLAYER_2_PITS} | {'1': 0, '2': 0}
    
    def display_rules(self):
        """Display game rules and guidelines"""
        print("""
=== MANCALA RULES AND GUIDELINES ===

Game Setup:
- Each player has 6 small pits and 1 store (on their right)
- Start with 4 seeds in each small pit
- Player 1: Pits A-F, Store 1
- Player 2: Pits G-L, Store 2

Basic Rules:
1. Players take turns moving seeds from their pits
2. Seeds are dropped one by one counter-clockwise
3. Skip opponent's store when dropping seeds
4. If last seed lands in your store, take another turn
5. If last seed lands in your empty pit, capture opposite seeds

Special Rules:
- Landing in your store → Extra turn
- Landing in empty pit → Capture opposite
- Game ends when one side empty
- Remaining seeds go to owner's store

Strategy Tips:
1. Early Game:
   - Keep seeds in back pits (A,B for P1; K,L for P2)
   - Look for store landings
   
2. Mid Game:
   - Create capture opportunities
   - Chain multiple moves
   - Control seed distribution
   
3. Late Game:
   - Count seeds carefully
   - Force favorable endgame
   - Plan multi-step captures
""")
        input("\nPress Enter to continue...")

    def display_help(self):
        """Display move help and pit labels"""
        print("""
Player 1's pits: A B C D E F
Player 2's pits: G H I J K L
Player 1's store: 1
Player 2's store: 2

Type 'rules' to show rules
Type 'quit' to exit
""")

class MancalaAI:
    def __init__(self, difficulty='medium'):
        self.difficulty = difficulty
        self.max_depth = {'easy': 2, 'medium': 4, 'hard': 6}[difficulty]
        
    def evaluate_board(self, board, player):
        """Enhanced evaluation function"""
        p1_store = board['1']
        p2_store = board['2']
        p1_seeds = sum(board[pit] for pit in PLAYER_1_PITS)
        p2_seeds = sum(board[pit] for pit in PLAYER_2_PITS)
        p1_empty = sum(1 for pit in PLAYER_1_PITS if board[pit] == 0)
        p2_empty = sum(1 for pit in PLAYER_2_PITS if board[pit] == 0)
        
        if player == '1':
            score = (p1_store - p2_store) * 2
            score += (p1_seeds - p2_seeds)
            score += (p2_empty - p1_empty) * 0.5
            for i, pit in enumerate(PLAYER_1_PITS):
                score += board[pit] * (i + 1) / 10
            for pit in PLAYER_1_PITS:
                if board[pit] == 0 and board[OPPOSITE_PIT[pit]] > 0:
                    score += 0.5
        else:
            score = (p2_store - p1_store) * 2
            score += (p2_seeds - p1_seeds)
            score += (p1_empty - p2_empty) * 0.5
            for i, pit in enumerate(reversed(PLAYER_2_PITS)):
                score += board[pit] * (i + 1) / 10
            for pit in PLAYER_2_PITS:
                if board[pit] == 0 and board[OPPOSITE_PIT[pit]] > 0:
                    score += 0.5
        return score

    def get_valid_moves(self, board, player):
        """Get list of valid moves for the player"""
        pits = PLAYER_1_PITS if player == '1' else PLAYER_2_PITS
        return [pit for pit in pits if board[pit] > 0]

    def minimax(self, board, depth, alpha, beta, maximizing_player, player):
        """Minimax algorithm with alpha-beta pruning"""
        if depth == 0 or checkForWinner(board) != 'no winner':
            return self.evaluate_board(board, player), None

        valid_moves = self.get_valid_moves(board, '1' if maximizing_player else '2')
        if not valid_moves:
            return self.evaluate_board(board, player), None

        best_move = valid_moves[0]
        if maximizing_player:
            max_eval = float('-inf')
            for move in valid_moves:
                board_copy = deepcopy(board)
                next_player = makeMove(board_copy, '1', move)
                eval_score, _ = self.minimax(board_copy, depth - 1, alpha, beta, 
                                          next_player == '1', player)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in valid_moves:
                board_copy = deepcopy(board)
                next_player = makeMove(board_copy, '2', move)
                eval_score, _ = self.minimax(board_copy, depth - 1, alpha, beta,
                                          next_player == '1', player)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def get_move(self, board, player):
        """Get the best move for the AI player"""
        if self.difficulty == 'easy' and random.random() < 0.3:
            valid_moves = self.get_valid_moves(board, player)
            return random.choice(valid_moves)
            
        _, move = self.minimax(board, self.max_depth, float('-inf'), float('inf'),
                             player == '1', player)
        return move

def getNewBoard():
    s = STARTING_NUMBER_OF_SEEDS
    return {'1': 0, '2': 0, 'A': s, 'B': s, 'C': s, 'D': s, 'E': s,
            'F': s, 'G': s, 'H': s, 'I': s, 'J': s, 'K': s, 'L': s}

def displayBoard(board):
    seedAmounts = []
    for pit in 'GHIJKL21ABCDEF':
        numSeedsInThisPit = str(board[pit]).rjust(2)
        seedAmounts.append(numSeedsInThisPit)

    print("""
+------+------+--<<<<<-Player 2----+------+------+------+
2      |G     |H     |I     |J     |K     |L     |      1
       |  {}  |  {}  |  {}  |  {}  |  {}  |  {}  |
S      |      |      |      |      |      |      |      S
T  {}  +------+------+------+------+------+------+  {}  T
O      |A     |B     |C     |D     |E     |F     |      O
R      |  {}  |  {}  |  {}  |  {}  |  {}  |  {}  |      R
E      |      |      |      |      |      |      |      E
+------+------+------+-Player 1->>>>>-----+------+------+

""".format(*seedAmounts))

def askForPlayerMove(playerTurn, board):
    while True:
        if playerTurn == '1':
            print('Player 1, choose move: A-F (or QUIT)')
        elif playerTurn == '2':
            print('Player 2, choose move: G-L (or QUIT)')
        response = input('> ').upper().strip()

        if response == 'QUIT':
            print('Thanks for playing!')
            sys.exit()
        
        if response == 'RULES':
            return 'rules'

        if (playerTurn == '1' and response not in PLAYER_1_PITS) or (
            playerTurn == '2' and response not in PLAYER_2_PITS
        ):
            print('Please pick a letter on your side of the board.')
            continue
        if board.get(response) == 0:
            print('Please pick a non-empty pit.')
            continue
        return response

def makeMove(board, playerTurn, pit):
    seedsToSow = board[pit]
    board[pit] = 0

    while seedsToSow > 0:
        pit = NEXT_PIT[pit]
        if (playerTurn == '1' and pit == '2') or (
            playerTurn == '2' and pit == '1'
        ):
            continue
        board[pit] += 1
        seedsToSow -= 1

    if (pit == playerTurn == '1') or (pit == playerTurn == '2'):
        return playerTurn

    if playerTurn == '1' and pit in PLAYER_1_PITS and board[pit] == 1:
        oppositePit = OPPOSITE_PIT[pit]
        board['1'] += board[oppositePit]
        board[oppositePit] = 0
    elif playerTurn == '2' and pit in PLAYER_2_PITS and board[pit] == 1:
        oppositePit = OPPOSITE_PIT[pit]
        board['2'] += board[oppositePit]
        board[oppositePit] = 0

    return '2' if playerTurn == '1' else '1'

def checkForWinner(board):
    player1Total = sum(board[pit] for pit in PLAYER_1_PITS)
    player2Total = sum(board[pit] for pit in PLAYER_2_PITS)

    if player1Total == 0:
        board['2'] += player2Total
        for pit in PLAYER_2_PITS:
            board[pit] = 0
    elif player2Total == 0:
        board['1'] += player1Total
        for pit in PLAYER_1_PITS:
            board[pit] = 0
    else:
        return 'no winner'

    if board['1'] > board['2']:
        return '1'
    elif board['2'] > board['1']:
        return '2'
    else:
        return 'tie'

def game_loop(mode, ai_player):
    """Main game loop"""
    gameBoard = getNewBoard()
    playerTurn = '1'  # Player 1 goes first

    while True:
        print('\n' * 60)
        displayBoard(gameBoard)
        
        if mode == '1' or (mode == '2' and playerTurn == '1'):
            playerMove = askForPlayerMove(playerTurn, gameBoard)
            if playerMove == 'rules':
                MancalaGame().display_rules()
                continue
        else:
            print(f'Player {playerTurn} (AI) is thinking...')
            time.sleep(1)
            playerMove = ai_player.get_move(gameBoard, playerTurn)
            print(f'Player {playerTurn} (AI) chooses pit {playerMove}')
            time.sleep(1)

        playerTurn = makeMove(gameBoard, playerTurn, playerMove)
        
        winner = checkForWinner(gameBoard)
        if winner in ('1', '2', 'tie'):
            displayBoard(gameBoard)
            if winner == 'tie':
                print('Game Over - It\'s a tie!')
            else:
                print(f'Game Over - Player {winner} wins!')
            sys.exit()

def main():
    """Main function"""
    print("Welcome to Mancala!")
    game = MancalaGame()
    game.display_rules()
    
    print('''Choose game mode:
1. Human vs Human
2. Human vs AI
3. AI vs AI
4. Show Rules Again
''')
    
    while True:
        mode = input('Enter choice (1-4): ').strip()
        if mode in ('1', '2', '3', '4'):
            break
        print("Invalid choice. Please enter 1-4.")
    
    if mode == '4':
        game.display_rules()
        return main()
    
    ai_difficulty = 'medium'
    if mode in ('2', '3'):
        print('\nSelect AI difficulty:')
        print('1. Easy')
        print('2. Medium')
        print('3. Hard')
        diff_choice = input('Enter difficulty (1-3): ').strip()
        ai_difficulty = {
            '1': 'easy',
            '2': 'medium',
            '3': 'hard'
        }.get(diff_choice, 'medium')

    ai_player = MancalaAI(ai_difficulty)
    game_loop(mode, ai_player)

if __name__ == '__main__':
    main()