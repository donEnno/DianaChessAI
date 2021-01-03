"""

- Generally, coordinates/positions are 'A3', 'B3',...
- board[coord] returns the piece at coord
- Try to always have a move to do (just take a random one at the beginning with update_move)

- IMPORTANT: ALWAYS USE COPIES OF THE GAME BOARD VIA DEEPCOPY() IF YOU WANT TO MANIPULATE THE BOARD,
             THIS IS SHOWN IN MR. NOVICE
             
- You can get the board from the gui via gui.chessboard

- DO NOT CHANGE OR ADD THE PARAMS OF THE GENERATE FUNCTION OR ITS NAME!



        -------------------- Useful methods  ---------------------------------------

-------------------- Board methods:

# converts coordinates in the form '(x,y)' (tuple) to 'A4' (string)
def letter_notation(self,coord)

# converts coordinates in the from 'A4' (string) to '(x,y)' (tuple)
def number_notation(self, coord):

# looks through the whole board to check for the king, outputs pos of king like this 'A5' (string)
def get_king_position(self, color):

# get the enemy, color is "white" or "black"
def get_enemy(self, color):

# manually check from the king if other pieces can attack it
# output is boolean
def is_in_check(self, color, debug=False):

def is_in_checkmate(self, color):

# returns a list of all valid moves in the format [('A1','A4'),..], left: from, right: to
def generate_valid_moves(self, color):

# returns a list of all possible moves in the format [('A1','A4'),..], left: from, right: to
def all_possible_moves(self, color):

# checks for limit turn count and checkmate, returns boolean (won/not won)
def check_winning_condition(self,color,end_game=False,print_result=False,gui = None):

# filter out invalid moves for moves of a color, returns list of valid moves
def is_in_check_after_move_filter(self,moves):

# returns boolean (still in check after p1->p2)
def is_in_check_after_move(self, p1, p2):

# time left for choosing move (in seconds)
def get_time_left(self):

# executes move without checking
# !   You have to manually change to the next player 
# with board.player_turn=board.get_enemy(board.player_turn) after this !
def _do_move(self, p1, p2):

# Pretty print boardef pprint(self):

# update the move that will be done (has to be a tuple (from, to))
def update_move(self,move):


---------------GUI methods

# performs the selected move (should ideally be at the end of generate function)
def perform_move(self):


--------------- Piece methods


# returns the landing positions, if the piece were at pos
# ! only landing positions !
def possble_moves(pos)

"""
import random
import math
import copy

# After perform_move(), make sure that the agent does not continue searching for moves!

class BelzGuenther:

    def __init__(self, color, delay=0, threshold=5):
        self.Pos_Table = [[] for i in range(9999901)]
        self.delay = delay
        self.TIME_THRESHOLD = threshold
        self.color = color

    def Hash(self, board):

        value = 1
        for coord in board.keys():
            if board[coord] is not None: value = value * (board.number_notation(coord)[0] + 1) * (board.number_notation(coord)[1] + 1) % 9999901
        return value

    def evaluateGame(self, board):
        color = self.color
        score = 0

        SCORE_WIN = 10000

        SCORE_PAWN = 100
        SCORE_ROOK = 525
        SCORE_BISHOP = 350
        SCORE_KNIGHT = 375

        SCORE_CHECK = 5


        player_wins = board.check_winning_condition(color)
        enemy_wins = board.check_winning_condition(board.get_enemy(color))
        game_ends = player_wins or enemy_wins



        # print("Check winning")
        if player_wins:
            return SCORE_WIN
        elif enemy_wins:
            return -SCORE_WIN


        # material
        for coord in board.keys():
            if (board[coord] is not None):
                figure = board[coord]
                fig_color = board[coord].color

                figurescore = 0
                fig_name = (figure.abbriviation).lower()
                if fig_name == 'p':
                    figurescore = 1
                elif fig_name == 'r':
                    figurescore = 4
                elif fig_name == 'b':
                    figurescore = 2.5
                elif fig_name == 'n':
                    figurescore = 3

                if fig_color == color:
                    score += figurescore
                else:
                    score -= figurescore
        return score

    def max_value(self, board, alpha, beta, depth):

        if depth == 0:
            return self.evaluateGame(board)

        # for saved in self.Pos_Table[self.Hash(board)]:  #durchsucht hashtable
        #     if saved[0] == board.to_string() and saved[1] >= depth:
        #         print('hash hat abgekürzt')
        #         return saved[2]

        v = -math.inf
        moves = board.generate_valid_moves(board.player_turn)
        for move in moves:
            # copy
            _from_fig = board[move[0]]
            _to_fig = board[move[1]]
            player, move_number = board.get_current_state()

            # perform
            board._do_move(move[0], move[1])
            board.switch_players()

            v = max(v, self.min_value(board, alpha, beta, depth - 1))

            # reset
            board[move[0]] = _from_fig
            board[move[1]] = _to_fig
            board.player_turn = player
            board.fullmove_number = move_number

            if v >= beta:
                # self.Pos_Table[self.Hash(board)].append([board.to_string(), depth, v])  #wollen wir das?
                return v
            alpha = max(alpha, v)
        self.Pos_Table[self.Hash(board)].append([board.to_string(), depth, v])
        return v


    def min_value(self, board, alpha, beta, depth):

        # color = self.color

        if depth == 0:
            return self.evaluateGame(board)

        # for saved in self.Pos_Table[self.Hash(board)]:  #durchsucht hashtable
        #     if saved[0] == board.to_string() and saved[1] >= depth:
        #         print('hash hat abgekürzt')
        #         return saved[2]

        v = math.inf
        moves = board.generate_valid_moves(board.player_turn)
        for move in moves:
            # copy
            _from_fig = board[move[0]]
            _to_fig = board[move[1]]
            player, move_number = board.get_current_state()


            # perform
            board._do_move(move[0], move[1])
            board.switch_players()

            v = min(v, self.max_value(board, alpha, beta, depth - 1))

            # reset
            board[move[0]] = _from_fig
            board[move[1]] = _to_fig
            board.player_turn = player
            board.fullmove_number = move_number

            if v <= alpha:
                self.Pos_Table[self.Hash(board)].append([board.to_string(), depth, v])  #wollen wir das?
                return v
            beta = min(beta, v)

        self.Pos_Table[self.Hash(board)].append([board.to_string(), depth, v])
        return v

    def generate_next_move(self, gui):

        board = copy.deepcopy(gui.chessboard)

        search_depth = 3
        max_v = -math.inf
        alpha = -math.inf  # alpha

        best_moves = []

        moves = board.generate_valid_moves(board.player_turn)
        random.shuffle(moves)

        move_values = []

        if len(moves) > 0:
            # always have one move to to
            gui.chessboard.update_move(moves[0])

            for m in moves:

                # COPY
                _from_fig = board[m[0]]
                _to_fig = board[m[1]]
                player, move_number = board.get_current_state()

                board._do_move(m[0], m[1])
                board.switch_players()

                v = self.minimax(gui.chessboard, -math.inf, math.inf, 3)

                move_values.append(v)
                max_v = max(max_v, v)
                alpha = max(alpha, v)

                best_move_index = move_values.index(max(move_values))
                board.update_move(moves[best_move_index])
                gui.perform_move()

                move_values.append(v)
                alpha = max(v, alpha)

                best_move_index = move_values.index(max(move_values))
                board.update_move(moves[best_move_index])
                gui.perform_move()

            # DO NOT REMOVE THIS, SHOULD BE AT THE END OF THE GENERATE FUNCTION
            board.engine_is_selecting = False

    def minimax(self, board, depth, maximizing_player, alpha=-math.inf, beta=math.inf):
        color = self.color

        if depth == 0:  # or game over
            return self.evaluateGame(board)

        moves = board.generate_valid_moves(board.player_turn)
        random.shuffle(moves)

        if maximizing_player:
            max_v = -math.inf

            for m in moves:

                # COPY
                _from_fig = board[m[0]]
                _to_fig = board[m[1]]
                player, move_number = board.get_current_state()

                # PERFORM
                board._do_move(m[0], m[1])
                board.switch_players()

                v = self.minimax(board, depth-1, alpha, beta,  False)

                # RESET
                board[m[0]] = _from_fig
                board[m[1]] = _to_fig
                board.player_turn = player
                board.fullmove_number = move_number

                max_v = max(max_v, v)
                alpha = max(alpha, v)
                if beta <= alpha:
                    break
            return max_v

        else:
            min_v = math.inf
            for m in moves:
                v = self.minimax(board, depth-1, alpha, beta, True)
                min_v = min(min_v, v)
                beta = min(beta, v)
                if beta <= alpha:
                    break
            return min_v













