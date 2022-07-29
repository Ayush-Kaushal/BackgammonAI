infinity = float('inf')
player = 1
all_rolls = [[i, j] if i != j else [i]*4 for i in range(1, 7) for j in range(i, 7)]


def eval_func(state):
    board = state.board
    bar = state.bar
    value_max = 0
    value_min = 0

    max_player = 1
    opponent = 2

    for i in range(1, 26):
        if i == 25:
            value_max += 2*len(board[i])
            continue

        if len(board[i]) > 0:
            if board[i][0] == max_player:
                if len(board[i]) == 1:
                    value_max -= 0.5
                if len(board[i]) >= 2:
                    value_max += 3
                    if len(board[i]) > 4:
                        value_max -= 0.4*(len(board[i]) - 4)
                if 19 <= i <= 24:
                    value_max += 0.75*len(board[i])
                elif 13 <= i <= 18:
                    value_max += 0.5*len(board[i])
                elif 7 <= i <= 12:
                    value_max += 0.25*len(board[i])

            else:
                if len(board[i]) >= 2:
                    value_min += 3
                    if len(board[i]) > 4:
                        value_min -= 0.4*(len(board[i]) - 4)
                if 1 <= i <= 6:
                    value_min += 0.75*len(board[i])
                elif 7 <= i <= 12:
                    value_min += 0.5*len(board[i])
                elif 13 <= i <= 18:
                    value_min += 0.25*len(board[i])

    evaluation = (value_max - value_min) * 0.01 + 0.035 * (bar[opponent] - bar[max_player])
    return evaluation


def max_value(state, game, roll, alpha, beta, depth):
    actions = game.actions(state, roll)
    v = -infinity
    if not actions:
        return expectinode(game.result(state), game, alpha, beta, depth)
    for a in actions:
        ev = expectinode(game.result(state, a), game, alpha, beta, depth)
        v = max(v, ev)
        alpha = max(alpha, v)

        if beta <= alpha:
            break
    return v


def min_value(state, game, roll, alpha, beta, depth):
    actions = game.actions(state, roll)
    v = infinity
    if not actions:
        return expectinode(game.result(state), game, alpha, beta, depth)
    for a in actions:
        ev = expectinode(game.result(state, a), game, alpha, beta, depth)
        v = min(v, ev)
        beta = min(beta, ev)
        if beta <= alpha:
            break
    return v


def expectinode(state, game, alpha, beta, depth):
    if depth == 0:
        val = eval_func(state)
        return val

    if player == state.player:
        fun = max_value
    else:
        fun = min_value
    v = 0

    count_two = 15
    count_four = 6
    new_alpha = alpha
    new_beta = beta

    for roll in all_rolls:
        v += (1/36 if len(roll) == 4 else 1/18) * fun(state, game, roll, new_alpha, new_beta, depth - 1)
        if len(roll) == 2:
            count_two -= 1
            probability = 1/18
        else:
            count_four -= 1
            probability = 1/36

        expected_max_value = v + 0.855 * (1/18*count_two + 1/36*count_four)
        expected_min_value = v - 0.855 * (1/18*count_two + 1/36*count_four)

        if expected_max_value <= alpha or expected_min_value >= beta:
            break

        if alpha != -infinity:
            new_alpha = probability * (alpha - expected_max_value + (0.855 * probability))
        if beta != infinity:
            new_beta = probability * (beta - expected_min_value - (0.855 * probability))

    return v


def get_best_move(state, game, dice_rolls):
    best_action = None
    beta = infinity

    # depth = 0 implements depth 1 search for expectiminimax tree.
    depth = 1

    actions = game.actions(state, dice_rolls)
    best_score = -infinity
    if not actions:
        return expectinode(game.result(state), game, best_score, beta, depth)
    for a in actions:
        new_state = game.result(state, a)
        ev = expectinode(new_state, game, best_score, beta, depth)
        if best_score < ev:
            best_score = ev
            best_action = a
        if beta <= best_score:
            break
    return best_action
