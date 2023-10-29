import random
import copy

class TTT_cs170_judge:
    def __init__(self):
        self.board = []
        
    def create_board(self, n):
        for i in range(n):
            row = []
            for j in range(n):
                row.append('-')
            self.board.append(row)
            
    def display_board(self):
        for row in self.board:
            print(" ".join(row))
        print()
            
    def is_winner(self, player):
        # Check rows
        for row in self.board:
            if all([cell == player for cell in row]):
                return True
        
        # Check columns
        for col in range(len(self.board)):
            if all([self.board[row][col] == player for row in range(len(self.board))]):
                return True
        
        # Check diagonals
        if all([self.board[i][i] == player for i in range(len(self.board))]):
            return True
        if all([self.board[i][len(self.board) - i - 1] == player for i in range(len(self.board))]):
            return True
        
        return False
    
    def is_board_full(self):
        return all([cell in ['X', 'O'] for row in self.board for cell in row])
    

class Player_1:
    def __init__(self, judge):
        self.board = judge.board
    
    def my_play(self):
        while True:
            row, col = map(int, input("Enter the row and column numbers separated by space: ").split())
            
            if 1 <= row <= len(self.board) and 1 <= col <= len(self.board[0]):
                self.board[row-1][col-1] = 'X'
                break
            else:
                print("Wrong coordination!")


class Player_2:
    def __init__(self, judge):
        self.judge = judge
        self.board = judge.board

    def isMovesLeft(self, board):
        for i in range(3):
            for j in range(3):
                if board[i][j] == '-':
                    return True
        return False
    
    def evaluate(self, board):
        # Checking for Rows for X or O victory.
        for row in range(3):
            if (board[row][0] == board[row][1] and board[row][1] == board[row][2]):
                if (board[row][0] == 'O'):
                    return 1
                elif (board[row][0] == 'X'):
                    return -1

        # Checking for Columns for X or O victory.
        for col in range(3):
            if (board[0][col] == board[1][col] and board[1][col] == board[2][col]):
                if (board[0][col] == 'O'):
                    return 1
                elif (board[0][col] == 'X'):
                    return -1

        # Checking for Diagonals for X or O victory.
        if (board[0][0] == board[1][1] and board[1][1] == board[2][2]):
            if (board[0][0] == 'O'):
                return 1
            elif (board[0][0] == 'X'):
                return -1

        if (board[0][2] == board[1][1] and board[1][1] == board[2][0]):
            if (board[0][2] == 'O'):
                return 1
            elif (board[0][2] == 'X'):
                return -1

        # If none of the above conditions are met, return 0
        return 0

    def minimax(self, board, depth, isMax):
        board_copy = copy.deepcopy(board)
        score = self.evaluate(board_copy)

        # If Maximizer has won the game, return the evaluated score
        if score == 1:
            return score

        # If Minimizer has won the game, return the evaluated score
        if score == -1:
            return score

        # If there are no more moves and no winner, it is a tie
        if not self.isMovesLeft(board_copy):
            return 0

        if isMax:
            best = -1000

            for i in range(3):
                for j in range(3):
                    if board_copy[i][j] == '-':
                        # Make the move
                        board_copy[i][j] = 'O'

                        # Call minimax recursively and choose the maximum value
                        best = max(best, self.minimax(board_copy, depth + 1, not isMax))

                        # Undo the move
                        board_copy[i][j] = '-'

            return best

        else:
            best = 1000

            for i in range(3):
                for j in range(3):
                    if board_copy[i][j] == '-':
                        # Make the move
                        board_copy[i][j] = 'X'

                        # Call minimax recursively and choose the minimum value
                        moveVal = self.minimax(board_copy, depth + 1, not isMax)

                        # Undo the move
                        board_copy[i][j] = '-'

                        if moveVal < best:
                            best = moveVal

            return best

    def my_play(self):
        bestMove = (-1, -1)
        bestScore = -1000
        
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == '-':
                    #try this move
                    self.board[row][col] = 'O'
                    move_score = self.minimax(self.board, 0, False)
                    
                    #undo the move
                    self.board[row][col] = '-'
                    
                    if move_score > bestScore:
                        bestScore = move_score
                        bestMove = (row, col)
                        
        if bestMove != (-1, -1):
            row = bestMove[0]
            col = bestMove[1]                
            self.board[row][col] = 'O'
        


# Main Game Loop
def game_loop():
    n = 3  # Board size
    game = TTT_cs170_judge()
    game.create_board(n)
    player1 = Player_1(game)
    player2 = Player_2(game)
    starter = random.randint(0, 1)
    win = False
    if starter == 0:
        print("Player 1 starts.")
        game.display_board()
        while not win:
            player1.my_play()
            win = game.is_winner('X')
            game.display_board()
            if win:
                print("Player 1 wins!")
                break
            if game.is_board_full():
                print("It's a tie!")
                break

            player2.my_play()
            win = game.is_winner('O')
            game.display_board()
            if win:
                print("Player 2 wins!")
                break
            if game.is_board_full():
                print("It's a tie!")
                break
    else:
        print("Player 2 starts.")
        game.display_board()
        while not win:
            player2.my_play()
            win = game.is_winner('O')
            game.display_board()
            if win:
                print("Player 2 wins!")
                break
            if game.is_board_full():
                print("It's a tie!")
                break
            
            player1.my_play()
            win = game.is_winner('X')
            game.display_board()
            if win:
                print("Player 1 wins!")
                break
            if game.is_board_full():
                print("It's a tie!")
                break

game_loop()
