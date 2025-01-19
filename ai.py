import math
import random

BLACK = 1
WHITE = 2

# オセロボード初期状態
board = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 1, 2, 0, 0],
    [0, 0, 2, 1, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
]

# 角を明確に優先する評価マップ
POSITION_SCORES = [
    [1000, 1000, 1000, 1000, 1000, 1000],  # 角は1000点、角周りは-100点で危険
    [1000, -200, -5, -5, -200, 1000], # 角周辺は非常に危険なので低評価
    [1000, -5, 1, 1, -5, 1000],
    [1000, -5, 1, 1, -5, 1000],
    [1000, -200, -5, -5, -200, 1000],
    [1000, 1000, 1000, 1000, 1000, 1000],
]

def can_place_x_y(board, stone, x, y):
    if board[y][x] != 0:
        return False
    opponent = 3 - stone
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        found_opponent = False
        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            nx += dx
            ny += dy
            found_opponent = True
        if found_opponent and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            return True
    return False

def valid_moves(board, stone):
    return [(x, y) for y in range(len(board)) for x in range(len(board[0])) if can_place_x_y(board, stone, x, y)]

def make_move(board, stone, x, y):
    board[y][x] = stone
    opponent = 3 - stone
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        flip_positions = []
        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            flip_positions.append((nx, ny))
            nx += dx
            ny += dy
        if flip_positions and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            for fx, fy in flip_positions:
                board[fy][fx] = stone
    return board

def evaluate_board(board, stone):
    score = 0
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == stone:
                score += POSITION_SCORES[y][x]
            elif board[y][x] == 3 - stone:
                score -= POSITION_SCORES[y][x]
    return score

def minimax(board, stone, depth, alpha, beta, maximizing_player):
    if depth == 0 or is_terminal(board):
        return evaluate_board(board, stone), None

    best_move = None
    if maximizing_player:
        max_eval = -math.inf
        for move in valid_moves(board, stone):
            x, y = move
            new_board = [row[:] for row in board]
            make_move(new_board, stone, x, y)
            eval, _ = minimax(new_board, 3 - stone, depth - 1, alpha, beta, False)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = math.inf
        for move in valid_moves(board, stone):
            x, y = move
            new_board = [row[:] for row in board]
            make_move(new_board, stone, x, y)
            eval, _ = minimax(new_board, 3 - stone, depth - 1, alpha, beta, True)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

def is_terminal(board):
    return not (valid_moves(board, BLACK) or valid_moves(board, WHITE))

class EdgePriorityAI:
    def face(self):
        return "🌟"

    def place(self, board, stone):
        _, move = minimax(board, stone, depth=4, alpha=-math.inf, beta=math.inf, maximizing_player=True)
        if move is None:
            return random.choice(valid_moves(board, stone))  # 手がある場合はランダム選択
        return move
run_othello(EdgePriorityAI())
