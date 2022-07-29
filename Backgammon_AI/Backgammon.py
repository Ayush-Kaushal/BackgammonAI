import copy
from Game_State import GameState


class Backgammon:

    def opponent(self, player):
        opp = {1: 2,
               2: 1}
        return opp[player]

    def actions(self, state, dice_rolls):
        board = copy.deepcopy(state.board)
        bar = copy.deepcopy(state.bar)
        player = state.player
        moves = []
        if dice_rolls is not None:
            if len(dice_rolls) == 4:
                state.get_moves(copy.deepcopy(board), copy.deepcopy(bar), copy.deepcopy(dice_rolls), player, [], moves)
            else:
                m1 = []
                m2 = []
                state.get_moves(copy.deepcopy(board), copy.deepcopy(bar), copy.deepcopy(dice_rolls), player, [], m1)
                state.get_moves(copy.deepcopy(board), copy.deepcopy(bar), copy.deepcopy(list(reversed(dice_rolls))), player, [], m2)
                moves = m1 + m2

        return moves

    def result(self, state, move=None):
        board = copy.deepcopy(state.board)
        bar = copy.deepcopy(state.bar)

        player = state.player
        if move is None:
            return GameState(board, bar, self.opponent(player))
        for m in move:
            if len(m) == 0:
                continue
            if m[0] == -1:
                bar[player] -= 1
                if len(board[m[1]]) == 1 and board[m[1]][0] != player:
                    bar[board[m[1]][0]] += 1
                    board[m[1]].pop()

                board[m[1]].append(player)

            else:
                board[m[0]].pop()
                if len(board[m[1]]) == 1 and board[m[1]][0] != player:
                    bar[board[m[1]][0]] += 1
                    board[m[1]].pop()

                board[m[1]].append(player)
        return GameState(board, bar, self.opponent(player))
