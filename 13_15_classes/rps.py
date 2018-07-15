import random


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


def build_the_three_rolls():
    """
    creates the rock, paper, scissor rolls

    :return: a list of rolls within the game
    """

    rock = Roll('rock', 'scissors', 'paper')
    paper = Roll('paper', 'rock', 'scissors')
    scissors = Roll('scissors', 'paper', 'rock')

    return [rock, paper, scissors]


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

    prompt = '{}, it\'s your move (rock, paper, scissors): '.format(player.name.title())

    while True:
        move = input(prompt)

        # convert to lower case
        move = move.strip().lower()

        # check to see if the given roll exists
        roll = [r for r in rolls if r.name == move]

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


def print_score(player):
    """
    prints the player's score

    :param player: the player
    """

    print('{} - {}'.format(player.name, player.wins))


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

        # print current game title
        print()
        print('-' * 9)
        print(' Game #{}'.format(game_count))
        print('-' * 9)

        # get player rolls
        player1_move = get_player_roll(player1, rolls)
        player2_move = get_computer_roll(player2, rolls)

        # spacing
        print()

        # check & print game results
        if player2_move.name in player1_move.wins_against:
            print('{} wins this round.'.format(player1.name.title()))
            player1.add_win()
        elif player2_move.name in player1_move.lose_against:
            print('{} wins this round.'.format(player2.name.title()))
            player2.add_win()
        else:
            print('Its a tie - let\'s go again')

        # print scores
        print_score(player1)
        print_score(player2)

        # increase roll count
        game_count += 1


def print_game_intro():
    """
    prints the game intro
    """
    print('*' * 35)
    print(' Welcome to Rock, Paper, Scissors')
    print()
    print(' The rules:')
    print(' - First to 3 wins.')
    print('*' * 35)
    print()


def print_game_outro(player1, player2):
    """
    prints the game outro
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


def main():
    """
    main game logic
    """

    # print game intro
    print_game_intro()

    # build roll rules
    rolls = build_the_three_rolls()

    # get player name
    name = get_players_name()

    # create players
    player1 = Player(name)
    player2 = Player('computer')

    # start game
    game_loop(player1, player2, rolls)

    # print game summary
    print_game_outro(player1, player2)


if __name__ == '__main__':
    main()