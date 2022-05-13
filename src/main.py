from bot import WordleBot

def main():
	bot = WordleBot(first_guess = "slate", cur_wordle = 324)
	bot.run()


if __name__ == '__main__':
	main()


'''
Psuedo

class Bot:

	interacts w// Wordle website
		selenium
	stores data
		data.json
		write()
		read()
	checks for new wordle
	plays wordle
		use info from Wordle website
		use algo to solve
			for every possible word after obtaining guess results
				find all possible evaluation combinations
				find entropy of word using sum(p*log2(1/p))
			guess = max(entropy)
		send guess to Wordle website
	display
		read data and display
'''
=======
>>>>>>> c4f99d6fdf8c004a5dec47116dadacba2ef4d666
