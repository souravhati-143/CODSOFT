# TASK 2: Tic-Tac-Toe AI using Minimax Algorithm
# CodSoft AI Internship

import math

def print_board(board):
    """Print the Tic-Tac-Toe board."""
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n")

def check_winner(board, player):
    """Check if a player has won."""
    win_combos = [
        [0,1,2], [3,4,5], [6,7,8],  # rows
        [0,3,6], [1,4,7], [2,5,8],  # columns
        [0,4,8], [2,4,6]             # diagonals
    ]
    for combo in win_combos:
        if all(board[i] == player for i in combo):
            return True
    return False

def is_draw(board):
    """Check if the game is a draw."""
    return all(cell != ' ' for cell in board)

def get_available_moves(board):
    """Return list of available positions."""
    return [i for i, cell in enumerate(board) if cell == ' ']

def minimax(board, depth, is_maximizing):
    """
    Minimax algorithm to find the best move for AI.
    AI = 'O' (maximizer), Human = 'X' (minimizer)
    """
    if check_winner(board, 'O'):
        return 10 - depth
    if check_winner(board, 'X'):
        return depth - 10
    if is_draw(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for move in get_available_moves(board):
            board[move] = 'O'
            score = minimax(board, depth + 1, False)
            board[move] = ' '
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for move in get_available_moves(board):
            board[move] = 'X'
            score = minimax(board, depth + 1, True)
            board[move] = ' '
            best_score = min(score, best_score)
        return best_score

def get_best_move(board):
    """Find the best move for AI using Minimax."""
    best_score = -math.inf
    best_move = None

    for move in get_available_moves(board):
        board[move] = 'O'
        score = minimax(board, 0, False)
        board[move] = ' '
        if score > best_score:
            best_score = score
            best_move = move

    return best_move

def play_game():
    """Main game loop."""
    board = [' '] * 9

    print("=" * 40)
    print("   Welcome to Tic-Tac-Toe AI!")
    print("   You are X, AI is O")
    print("   Board positions:")
    print("    1 | 2 | 3 ")
    print("   ---+---+---")
    print("    4 | 5 | 6 ")
    print("   ---+---+---")
    print("    7 | 8 | 9 ")
    print("=" * 40)

    while True:
        print_board(board)

        # Human turn
        while True:
            try:
                move = int(input("Your move (1-9): ")) - 1
                if move < 0 or move > 8:
                    print("Please enter a number between 1 and 9.")
                elif board[move] != ' ':
                    print("That spot is already taken! Try another.")
                else:
                    break
            except ValueError:
                print("Invalid input. Please enter a number.")

        board[move] = 'X'

        if check_winner(board, 'X'):
            print_board(board)
            print("🎉 Congratulations! You won!")
            break

        if is_draw(board):
            print_board(board)
            print("🤝 It's a draw!")
            break

        # AI turn
        print("AI is thinking...")
        ai_move = get_best_move(board)
        board[ai_move] = 'O'
        print(f"AI played at position {ai_move + 1}")

        if check_winner(board, 'O'):
            print_board(board)
            print("🤖 AI wins! Better luck next time.")
            break

        if is_draw(board):
            print_board(board)
            print("🤝 It's a draw!")
            break

    play_again = input("\nPlay again? (yes/no): ").strip().lower()
    if play_again in ['yes', 'y']:
        play_game()
    else:
        print("Thanks for playing! Goodbye!")

if __name__ == "__main__":
    play_game()