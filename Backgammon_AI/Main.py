import copy
import random
from Expectiminimax import *
from Game_State import GameState
from Backgammon import Backgammon

start_state = [[], [1, 1], [], [], [], [], [2, 2, 2, 2, 2], [], [2, 2, 2], [], [], [], [1, 1, 1, 1, 1],
               [2, 2, 2, 2, 2], [], [], [], [1, 1, 1], [], [1, 1, 1, 1, 1], [], [], [], [], [2, 2], []]

start_bar = [0, 0, 0]


def print_board(board, bar):
    max_checker = max(bar[1], bar[2])

    for i in range(1, 25):
        if len(board[i]) > max_checker:
            max_checker = len(board[i])

    max_checker = max(5, max_checker)

    player1 = " X "
    player2 = " O "

    print("+", end="")
    for i in range(13, 19):
        print(f"{i}-", end="")
    print("|   |", end="")
    for i in range(19, 25):
        print(f"{i}-", end="")
    print("+", end='\t   ')
    for i in range(0, len(board[25])):
        print("X", end="")

    print()

    for i in range(0, max_checker):
        print("|", end="")
        for j in range(13, 19):
            if len(board[j]) > i:
                if board[j][0] == 1:
                    print(f"{player1}", end="")
                else:
                    print(f"{player2}", end="")
            else:
                print("   ", end="")

        if bar[1] > 0:
            print(f"|{player1}|", end="")
            bar[1] -= 1
        else:
            print("|   |", end="")

        for j in range(19, 25):
            if len(board[j]) > i:
                if board[j][0] == 1:
                    print(f"{player1}", end="")
                else:
                    print(f"{player2}", end="")
            else:
                print("   ", end="")

        print("|")

    for i in range(max_checker, 0, -1):
        print("|", end="")
        for j in range(12, 6, -1):
            if len(board[j]) >= i:
                if board[j][0] == 1:
                    print(f"{player1}", end="")
                else:
                    print(f"{player2}", end="")
            else:
                print("   ", end="")

        if bar[2] >= i:
            print(f"|{player2}|", end="")
            bar[2] -= 1
        else:
            print("|   |", end="")

        for j in range(6, 0, -1):
            if len(board[j]) >= i:
                if board[j][0] == 1:
                    print(f"{player1}", end="")
                else:
                    print(f"{player2}", end="")
            else:
                print("   ", end="")
        print("|")

    print("+", end="")
    for i in range(12, 6, -1):
        if i >= 10:
            print(f"{i}-", end="")
        else:
            print(f"-{i}-", end="")

    print("|   |", end="")
    for i in range(6, 0, -1):
        if i >= 10:
            print(f"{i}-", end="")
        else:
            print(f"-{i}-", end="")
    print("+", end="\t   ")
    for i in range(0, len(board[0])):
        print("O", end="")
    print()


def roll_dice():
    first_roll = random.randint(1, 6)
    second_roll = random.randint(1, 6)
    if first_roll == second_roll:
        return [first_roll, first_roll, first_roll, first_roll]
    return [first_roll, second_roll]


def game_over(state):
    if len(state.board[0]) == 15:
        print()
        print("YOU WIN")
        exit()
    elif len(state.board[25]) == 15:
        print()
        print("COMPUTER WINS")
        exit()


if __name__ == '__main__':
    print()

    print("WELCOME TO BACKGAMMON")
    print("*"*80)

    print()

    print("1 : New Game")
    print("0: Exit")

    choice = input(">> ")
    while choice not in {"1", "0"}:
        print("Invalid Choice")
        choice = input("Enter your Choice again >> ")

    if choice == '0':
        exit()

    board = start_state
    bar = start_bar
    print()
    print_board(copy.deepcopy(board), copy.deepcopy(bar))

    print()
    choice = input("PRESS ENTER TO ROLL THE DICE >> ")
    while choice != "":
        choice = input("PRESS ENTER TO ROLL THE DICE >> ")

    dice_rolls = roll_dice()
    while len(dice_rolls) == 4:
        dice_rolls = roll_dice()

    first_roll = dice_rolls[0]
    second_roll = dice_rolls[1]

    print()
    print(f"Dice Rolls are : {first_roll, second_roll}")

    player = 1
    if second_roll > first_roll:
        player = 2

    game_state = GameState(board, bar, player)
    game = Backgammon()

    while True:
        if player == 1:
            print("Computer is playing...")
            moves = get_best_move(game_state, game, dice_rolls)
            print("Moves played by Computer are : ")
            if moves is not None:
                print("\n".join(" ".join(str(m) for m in move) for move in moves))

            game_state = game.result(game_state, moves)
            print_board(copy.deepcopy(game_state.board), copy.deepcopy(game_state.bar))
            game_over(game_state)
            player = game_state.player

        else:
            print()
            print("PLAY YOUR TURN : ")

            while True:

                moves = []
                move = list(map(int, input("Enter First Move : ").split()))
                moves.append(move)

                move = list(map(int, input("Enter Second Move : ").split()))
                moves.append(move)
                if len(dice_rolls) == 4:
                    move = list(map(int, input("Enter Third Move : ").split()))
                    moves.append(move)

                    move = list(map(int, input("Enter Fourth Move : ").split()))
                    moves.append(move)

                valid_moves = game.actions(game_state, dice_rolls)
                if moves not in valid_moves:
                    print("INVALID MOVE")
                    print()
                else:
                    break

            game_state = game.result(game_state, moves)
            print_board(copy.deepcopy(game_state.board), copy.deepcopy(game_state.bar))
            game_over(game_state)
            player = game_state.player

        print()
        choice = input("PRESS ENTER TO ROLL THE DICE >> ")
        while choice != "":
            print()
            choice = input("PRESS ENTER TO ROLL THE DICE >> ")

        dice_rolls = roll_dice()
        first_roll = dice_rolls[0]
        second_roll = dice_rolls[1]

        print()
        if len(dice_rolls) == 4:
            print(f"Dice Rolls are : {first_roll, first_roll, first_roll, first_roll}")
        else:
            print(f"Dice Rolls are : {first_roll, second_roll}")
