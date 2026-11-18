"""CodSoft AI Internship - Task 2: Unbeatable Tic-Tac-Toe AI
Minimax with Alpha-Beta pruning. Human = X, AI = O (you can choose who starts)."""
import math

WINS = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
HUMAN, AI = "X", "O"


def winner(b):
    for a, c, d in WINS:
        if b[a] != " " and b[a] == b[c] == b[d]:
            return b[a]
    return None


def moves(b):
    return [i for i, v in enumerate(b) if v == " "]


def minimax(b, is_ai, alpha, beta, depth):
    w = winner(b)
    if w == AI:
        return 10 - depth          # prefer faster wins
    if w == HUMAN:
        return depth - 10          # prefer slower losses
    if " " not in b:
        return 0
    if is_ai:
        best = -math.inf
        for m in moves(b):
            b[m] = AI
            best = max(best, minimax(b, False, alpha, beta, depth + 1))
            b[m] = " "
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return best
    best = math.inf
    for m in moves(b):
        b[m] = HUMAN
        best = min(best, minimax(b, True, alpha, beta, depth + 1))
        b[m] = " "
        beta = min(beta, best)
        if beta <= alpha:
            break
    return best


def best_move(b):
    best, move = -math.inf, None
    for m in moves(b):
        b[m] = AI
        score = minimax(b, False, -math.inf, math.inf, 1)
        b[m] = " "
        if score > best:
            best, move = score, m
    return move


def show(b):
    print()
    for r in range(3):
        print(" " + " | ".join(b[r*3:r*3+3]))
        if r < 2:
            print("---+---+---")
    print()


def play():
    b = [" "] * 9
    print("Tic-Tac-Toe: you are X, AI is O. Enter 1-9 (top-left=1, bottom-right=9).")
    turn_human = input("Do you want to go first? (y/n): ").strip().lower() != "n"
    show(b)
    while True:
        if turn_human:
            try:
                m = int(input("Your move (1-9): ")) - 1
                if m not in moves(b):
                    raise ValueError
            except ValueError:
                print("Invalid move, try again.")
                continue
            b[m] = HUMAN
        else:
            b[best_move(b)] = AI
            print("AI plays:")
        show(b)
        w = winner(b)
        if w:
            print("You win!" if w == HUMAN else "AI wins!")
            break
        if " " not in b:
            print("It's a draw!")
            break
        turn_human = not turn_human


if __name__ == "__main__":
    play()
