import sys
import os
import random

from console_bot import ConsoleWordleBot
from game import Game
from words import POSS_ANSWERS

poss_answers = list(POSS_ANSWERS).copy()

def simulate(n_simulations, first_words):
    """
    This method simulates <n_simulation> games using <first_words> as
    the first guess(es). It then displays the result of using each first word
    
    Parameters
    ----------
    n_simulations:      int
                        number of games to play
    firt_words:         list
                        list of first guesses to use
    """
    def print_progress_bar(iteration, prefix = "Progress", suffix = 'Complete', decimals = 1, length = 80, fill ='█', end = "\r"):
        """This method prints a progress bar to the screen"""
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(n_simulations)))
        filled_length = int(length * iteration // n_simulations)
        bar = fill * filled_length + '-' * (length - filled_length)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = end)


    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"Simulating {n_simulations} games of wordle trying '{', '.join(first_words[:-1])}, {first_words[-1]}' as first guesses\n\n")
    bots = []
    for word in first_words:
        bots.append(ConsoleWordleBot(word))
    for i in range(n_simulations):
        print_progress_bar(i)
        answer = random.choice(poss_answers)
        poss_answers.pop(poss_answers.index(answer))
        game = Game(answer)
        for bot in bots:
            try:
                bot.play_game(game)
            except Exception as e:
                print(f'\rERROR ON WORD {answer}')
                print(f'{e}')
                exit()
    os.system('cls' if os.name == 'nt' else 'clear')
    for bot in bots:
        bot.display_data()


def main():
    if not sys.argv:
        n_simulations = int(input("Enter number of simulations:\n"))
        first_words = input("Enter first words to try separated by whitespace:\n").split()
        simulate(n_simulations, first_words)
    else:
        simulate(int(sys.argv[1]), sys.argv[2:])


if __name__ == '__main__':
    main()