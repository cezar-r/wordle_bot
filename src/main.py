from bot import WordleBot

def main():
	bot = WordleBot(first_guess = "slate", cur_wordle = 317)
	bot.run()


if __name__ == '__main__':
	main()
