import random
import pandas as pd


class Roll:
    """
    Represents a roll

    name: the name of the roll
    wins_against: a list of roll names that this roll wins against
    lose_against: a list of roll names that this roll looses against
    """

    def __init__(self, name, wins_against, lose_against):
        self.name = name
        self.wins_against = wins_against
        self.lose_against = lose_against


class Player:
    """
    Represents a player

    name: the name of the player
    wins: the total number of wins this player has achieved.
    """

    def __init__(self, name):
        self.name = name
        self.wins = 0

    def add_win(self):
        self.wins += 1


def build_rolls():
    """
    reads in roll rules from input file

    :return: a list of valid rolls in the game
    """

    rolls = []

    rules = pd.read_csv('battle-table.csv')


    for idx, row in rules.iterrows():

        attacker = row.Attacker

        wins_against = list(row[row == 'win'].index)
        lose_against = list(row[row == 'lose'].index)

        roll = Roll(attacker, wins_against, lose_against)

        rolls.append(roll)

    return rolls


def get_players_name():
    """
    prompts for and validates player name

    :return: the player name
    """

    prompt = 'please enter your name: '

    while True:
        name = input(prompt)

        # if its a blank name, prompt user to re-enter the name
        if name == '':
            prompt = '>> you cannot have a blank name - please try again\n\n'
            prompt = prompt + 'please enter your name: '
        else:
            return name


def get_player_roll(player, rolls):
    """
    Retrieves the player's roll

    :param player: the current player
    :param rolls: a list of valid rolls within the game
    :return: the payer's roll
    """

    prompt = '{}, it\'s your move: '.format(player.name.title())

    while True:
        move = input(prompt)

        # convert to lower case
        move = move.strip().lower()

        # check to see if the given roll exists
        roll = [r for r in rolls if r.name.lower() == move]

        # if the roll is valid return it, otherwise, reprompt for player roll
        if len(roll) > 0:
            return roll[0]
        else:
            prompt = '>> I do not understand that roll - please try again\n\n'
            prompt = prompt + '{}, it\'s your move (rock, paper, scissors): '.format(player.name.title())


def get_computer_roll(player, rolls):
    """
    randomly selects a roll for the computer from the set of valid rolls

    :param player: the computer player
    :param rolls: a list of valid rolls
    :return: the computer's roll
    """

    # randomly select a roll
    secure_random = random.SystemRandom()
    roll = secure_random.choice(rolls)

    print('\n{} has selected {}.'.format(player.name.title(), roll.name))

    return roll


def print_intro(rolls):
    """
    prints the introduction to the game with rules
    """

    roll_names = ''

    for idx, r in enumerate(rolls):
        if idx == 0:
            roll_names = '    ' + r.name
        elif idx % 6 == 0:
            roll_names = roll_names + ',\n    ' + r.name
        else:
            roll_names = roll_names + ', ' + r.name

    print('*' * 50)
    print(' Welcome to Rock, Paper, Scissors, and MORE!')
    print()
    print(' The rules:')
    print(' - You have 15 moves to select from:')
    print(roll_names)
    print(' - First to 3 games wins.')
    print('*' * 50)
    print()


def print_outro(player1, player2):
    """
    prints the game outro and summary of win or lose
    """

    # print game summary
    if player1.wins == 3:
        result = 'You won :)'
    else:
        result = 'You lost :('

    print()
    print('*' * 25)
    print(' Game Over - {}'.format(result))
    print('*' * 25)


def print_game_start(game_count):
    """
    prints an intro to the game start

    :param game_count: the current game number
    """

    # print current game title
    print()
    print('-' * 9)
    print(' Game #{}'.format(game_count))
    print('-' * 9)

def print_game_end(player1, player1_move, player2, player2_move):
    """
    print a summary of the game

    :param player1: the first player
    :param player1_move: the first players roll
    :param player2: the second player
    :param player2_move: the seoncd players roll
    """

    # check & print game results
    if player1_move == player2_move:
        print('Its a tie - let\'s go again')
        return

    if player2_move.name in player1_move.wins_against:
        print('{} wins this round.'.format(player1.name.title()))
        player1.add_win()

    else:
        print('{} wins this round.'.format(player2.name.title()))
        player2.add_win()

    print('{} - {}'.format(player1.name, player1.wins))
    print('{} - {}'.format(player2.name, player2.wins))


def game_loop(player1, player2, rolls):
    """
    Controls the game logic

    :param player1: the first player
    :param player2: the second player
    :param rolls: a list of valid rolls in the game
    """

    game_count = 1

    # while a player has not yet won
    while (player1.wins < 3) and (player2.wins < 3):

        # begin game
        print_game_start(game_count)

        # get player rolls
        player1_move = get_player_roll(player1, rolls)
        player2_move = get_computer_roll(player2, rolls)

        # spacing
        print()

        # end game
        print_game_end(player1, player1_move, player2, player2_move)

        # increase roll count
        game_count += 1


def main():
    """
    main game logic
    """

    # build roll rules
    rolls = build_rolls()

    # print intro
    print_intro(rolls)

    # get player name
    name = get_players_name()

    # create players
    player1 = Player(name)
    player2 = Player('computer')

    # start game
    game_loop(player1, player2, rolls)

    # print game summary
    print_outro(player1, player2)


if __name__ == '__main__':
    main()