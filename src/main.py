from bot import WordleBot

def main():
	bot = WordleBot(first_guess = "slate", cur_wordle = 312)
	bot.run()


if __name__ == '__main__':
	main()


'''TODO

Continue running simulations and comparing guesses to wordle bot
Find a way to look through every word in vocab as guess
Add word commonality
'''