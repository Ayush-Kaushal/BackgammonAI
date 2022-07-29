import copy


class GameState:
    def __init__(self, board, bar, player):
        self.board = board
        self.bar = bar
        self.player = player
        self.moves = []

    def can_bear_off(self, board, bar, player):
        bear_off = (bar[player] == 0)

        if not bear_off:
            return bear_off

        for i in range(1, 19):
            index = i if(player == 1) else (25 - i)
            bear_off = (len(board[index]) == 0) or (board[index][0] != player)
            if not bear_off:
                break

        return bear_off

    def get_bear_off_move(self, board, roll, player):
        poss_moves = []

        index = (25 - roll) if(player == 1) else roll
        end = 25 if(player == 1) else 0

        if len(board[index]) != 0 and board[index][0] == player:
            poss_moves.append([index, end])

        for i in range(1, 6):
            index = 18 + i if(player == 1) else (7 - i)
            if len(board[index]) != 0 and board[index][0] == player:
                index2 = index + roll if(player == 1) else index - roll
                if 0 < index2 < 25:
                    if (len(board[index2]) == 0) or (len(board[index2]) == 1) or (board[index2][0] == player):
                        poss_moves.append([index, index2])

        if len(poss_moves) != 0:
            return poss_moves

        else:
            for i in range(roll - 1, 0, -1):
                index = (25 - i) if(player == 1) else i
                end = 25 if(player == 1) else 0
                if len(board[index]) != 0 and board[index][0] == player:
                    return [[index, end]]

        return poss_moves

    def get_normal_moves(self, board, roll, player):
        poss_moves = []

        for i in range(1, 24):
            index = i if(player == 1) else (25 - i)
            if len(board[index]) != 0 and board[index][0] == player:
                index2 = (index + roll) if(player == 1) else (index - roll)
                if 0 < index2 < 25:
                    if len(board[index2]) <= 1 or board[index2][0] == player:
                        poss_moves.append([index, index2])

        return poss_moves

    def get_bar_moves(self, board, roll, player):
        index = roll if(player == 1) else (25 - roll)
        if len(board[index]) <= 1 or board[index][0] == player:
            return [-1, index]
        else:
            if player == 1:
                return []
            else:
                return [[]]

    def get_moves(self, board, bar, dice_rolls, player, mv, moves):
        if len(dice_rolls) == 0:
            moves.append(mv)
            return
        roll = dice_rolls[0]
        if bar[player] != 0:
            move = self.get_bar_moves(board, roll, player)
            if move == [[]]:
                self.get_moves(board, bar, dice_rolls[1:], player, mv + [[]], moves)
            elif len(move) != 0:
                bar[player] -= 1
                if len(board[move[1]]) == 1 and board[move[1]][0] != player:
                    board[move[1]].pop()
                board[move[1]].append(player)
                self.get_moves(board, bar, dice_rolls[1:], player, mv + [move], moves)
            else:
                self.get_moves(board, bar, dice_rolls[1:], player, mv, moves)
        else:
            if self.can_bear_off(board, bar, player):
                move = self.get_bear_off_move(board, roll, player)
            else:
                move = self.get_normal_moves(board, roll, player)
            if len(move) != 0:
                for m in move:
                    temp_board = copy.deepcopy(board)
                    temp_board[m[0]].pop()
                    if len(temp_board[m[1]]) == 1 and temp_board[m[1]][0] != player:
                        temp_board[m[1]].pop()
                    temp_board[m[1]].append(player)
                    self.get_moves(temp_board, bar, dice_rolls[1:], player, mv + [m], moves)
            else:
                self.get_moves(board, bar, dice_rolls[1:], player, mv + [[]], moves)
