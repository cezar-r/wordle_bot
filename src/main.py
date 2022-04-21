from bot import WordleBot

def main():
	bot = WordleBot(first_guess = "soare", cur_wordle = 304)
	bot.run()


if __name__ == '__main__':
	main()