import sys
import os

from console_bot import ConsoleWordleBot
from game import Game


def simulate(n_simulations = int(sys.argv[1]), first_words = sys.argv[2:]):
	"""
	This method simulates <n_simulation> games using <first_words> as
	the first guess(es). It then displays the result of using each first word
	
	Parameters
	----------
	n_simulations:		int
						number of games to play
	firt_words:			list
						list of first guesses to use
	"""
	os.system('cls' if os.name == 'nt' else 'clear')
	print(f"Simulating {n_simulations} games of wordle trying '{', '.join(first_words[:-1])}, {first_words[-1]}' as first guesses\n\n")
	bots = []
	for word in first_words:
		bots.append(ConsoleWordleBot(word))
	for i in range(n_simulations):
		print(f"Playing game {i+1}/{n_simulations}", end = "\r")
		game = Game()
		for bot in bots:
			bot.play_game(game)
	os.system('cls' if os.name == 'nt' else 'clear')
	for bot in bots:
		bot.display_data()


def main():
	if not sys.argv:
		n_simulations = int(input("Enter number of simulations:\n"))
		first_words = input("Enter first words to try separated by whitespace:\n").split()
		simulate(n_simulations, first_words)
	else:
		simulate()


if __name__ == '__main__':
	main()