import random
class Tic(object):
    terminalStates=(
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6])

    winners = ('X-win', 'Draw', 'O-win')

    def __init__(self, board=[]):
        if len(board) == 0:
            self.squares = [None for i in range(9)]
        else:
            self.squares = board
            
    def winner(self): #Will check for if player or computer won
        for player in ('X', 'O'):
            positions = self.getBoard(player) #Checks for the current positions
            for terminal in self.terminalStates:   #Checks if any terminalStates are triggered
                win = True
                for pos in terminal:
                    if pos not in positions:
                        win = False
                if win:
                    return player

    def getBoard(self, player): #Returns the squares that the player has played.
        return [k for k, v in enumerate(self.squares) if v == player]


    def printBoard(self): #Uses a for loop to iterate through the length of the board and prints them (Spots 0-9)
        for element in [self.squares[i:i + 3] for i in range(0, len(self.squares), 3)]:
            print (element) #unfortuantly I couldn't get python to print _ instead of none. I don't know of any hack to fix that.


    def available_moves(self): #Checks for the value of None in the array to see the open squares
        return [k for k, v in enumerate(self.squares) if v is None]

    def complete(self):#Checks if the game is finished (If any terminal states are satisfied)
        if None not in [v for v in self.squares]:
            return True
        if self.winner() != None:
            return True
        return False

    def player_won(self):#used for alphaBeta for prediction
        return self.winner() == 'X'

    def AI_won(self): #used for alphaBeta for prediction
        return self.winner() == 'O'

    def tied(self):
        return self.complete() == True and self.winner() is None


    def make_move(self, position, player):#Places the move on the board
        self.squares[position] = player

    def alphabeta(self, node, player, alpha, beta):
        if node.complete():
            if node.player_won():
                return -1
            elif node.tied():
                return 0
            elif node.AI_won():
                return 1
        for move in node.available_moves():
            node.make_move(move, player)
            valOfChoice = self.alphabeta(node, get_enemy(player), alpha, beta) #self call to "place" moves and test if they are actually the best move
            node.make_move(move, None)
            if player == 'O':
                if valOfChoice > alpha:
                    alpha = valOfChoice
            else:
                if valOfChoice < beta:
                    beta = valOfChoice
                if beta <= alpha:
                    return alpha
        if player == 'O':
            return alpha
        else:
            return beta


def determine(board, player):
    a = -2
    choices = []
    if len(board.available_moves()) == 9:
        return 4
    for move in board.available_moves():
        board.make_move(move, player)
        value = board.alphabeta(board, get_enemy(player), -2, 2)
        board.make_move(move, None)
        if value > a:
            a = value
            choices = [move]
        elif value == a:
            choices.append(move)
    return random.choice(choices) #Orginally was going to use numpy for this but this seems like a good workaround


def get_enemy(player):
    if player == 'X':
        return 'O'
    return 'X'

if __name__ == "__main__":
    continueProgram = True
    while(continueProgram):

        board = Tic()
        print("None means that space is available to be played. ")
        print("The value of 1 is the top left corner. The value of 3 is the top right corner. The value of 7 is the bottom left corner. The value of 9 is the bottom right corner.")
        while not board.complete():
            player = 'X'
            print()
            print("What is your move? Type 1-9 to choose your move. Any non number will crash the program.")
            player_move = int(input("Next Move: ")) - 1
            if not player_move in board.available_moves():
                continue
            board.make_move(player_move, player)

            if board.complete():
                break
            player = get_enemy(player)
            computer_move = determine(board, player) #Call to determine the next best move using alphaBeta
            board.make_move(computer_move, player)
            board.printBoard()

        print ("Value of winner: " + board.winner())
        if board.winner() == 0:
            print("Computer Won")
        elif board.winner() == 1:
            print("Player Won")
        else:
            print ("The game ended in a tie.")
        print ("The winner is: ", board.winner())
        print()
        print("Do you want to play again?")
        play_again = str(input("Type Y/N: "))
        if play_again == "Y":
            continue
        elif play_again == "N":
            continueProgram = False
            print("Thanks for playing!")

