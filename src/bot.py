import os
import time
import json
import warnings
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from words import WORDBANK, PREV_ANSWERS

warnings.filterwarnings("ignore")
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path = "C:\Program Files (x86)\chromedriver.exe", service_log_path='NUL', options = options)
url = "https://www.nytimes.com/games/wordle/"
driver.get(url)
time.sleep(1)


class Bot:
	"""
	This class represents the bot that plays wordle
	Its data is stored in a json file and its first guess is
	given by the mathematically optimal first word; soare
	The current wordle should be set to whatever wordle the 
	previous days wordle was
	"""
	def __init__(self, filename = "data.json", first_guess = "soare", cur_wordle = 302):
		self.filename = filename
		self.first_guess = first_guess
		self.cur_wordle = cur_wordle
		self.data = json.load(open(self.filename))

	def run(self):
		"""
		This method runs the bot. It checks if there is
		a new wordle to played, and if there is, it attempts
		to complete the puzzle. Otherwise, it continuously 
		checks for a new wordle every 5 seconds
		"""
		dots = 1
		while not self._new_wordle():
			dots_str = "." * dots
			print("Waiting for new wordle" + dots_str, end = "\r")
			if dots == 3:
				dots = 1
			else:
				dots += 1
			time.sleep(5)

		os.system('cls' if os.name == 'nt' else 'clear')
		print("New Wordle Found!")
		self._complete_new_wordle()
		self.run()

	def _new_wordle(self):
		"""
		This method checks if there is a new wordle or not
		It refreshes the page and checks if there is a new
		puzzle. If there is, it returns true.

		Returns
		-------
		bool:	true if new wordle, otherwise false
		"""
		# returns true if new wordle is loaded, otherwise false	
		driver.refresh() # delete if autorefreshes at midnight
		inner_texts = [my_elem.get_attribute("outerHTML") for my_elem in driver.execute_script("""return document.querySelector('game-app').shadowRoot.querySelector('game-row').shadowRoot.querySelectorAll('game-tile[letter]')""")]
		if inner_texts == []:
			self.cur_wordle += 1
			return True
		return False

	def _complete_new_wordle(self):
		"""
		This method attempts to solve the wordle puzzle
		For every guess, it looks through every possible word
		and uses information theory to pick the optimal word
		for the next guess. It then writes out information
		about the game to the file
		"""
		guess = self.first_guess
		guesses = 0
		prev_guesses = []
		poss_words = WORDBANK
		while guesses < 6:
			guesses += 1
			guess_results = self._guess(guess)
			prev_guesses.append(guess)
			if self._guessed_word(guess_results):
				self._write_out(prev_guesses, True)
				return
			poss_words = self._find_poss_words(guess, guess_results, poss_words)
			guess = self._new_guess(guess_results, guess, prev_guesses,  poss_words)

		self._write_out(prev_guesses, False)

	def _guessed_word(self, guess_results):
		"""
		This method checks if a word has been guessed
		It looks through a list of evaluation tiles and
		if they are all green, it returns true

		Parameters
		----------
		guess_results:	list
						list of evalution tiles ("correct", "present", or "absent")

		Returns
		-------
		bool:			true if tiles are correct, otherwise false
		"""
		for evaluation in guess_results:
			if evaluation != "correct":
				return False
		return True

	def _write_out(self, prev_guesses, won):
		"""
		This method writes out the game data to a file

		Parameters
		----------
		prev_guesses:	list
						list of guesses used
		won:			bool
						true if game was won
		"""
		key = "wordle_" + str(self.cur_wordle)
		data = self.data['data']
		new_entry = {}
		game_data = {}
		game_data['won'] = won
		for i, guess in enumerate(prev_guesses):
			game_data[i + 1] = guess
		new_entry[key] = game_data
		data['game_history'].append(new_entry)
		data['games_played'] += 1
		if won:
			data['cur_streak'] += 1
		else:
			data['cur_streak'] = 0
		data['max_streak'] = max(data['max_streak'], data['cur_streak'])
		data['win_rate'] = self._calc_win_rate(data)

		json_string = json.dumps({"data" : data}, indent=4)
		with open(self.filename, 'w') as outfile:
			outfile.write(json_string)
		self._display_stats()

	def _display_stats(self):
		"""
		This method displays the bots data to the console
		"""
		self.data = json.load(open(self.filename))
		data = self.data['data']
		games_played = data['games_played']
		win_rate = data['win_rate']
		cur_streak = data['cur_streak']
		max_streak = data['max_streak']

		print(f'\nGames played: {games_played}\nWin rate: {win_rate}%\nCurrent streak: {cur_streak}\nMax streak: {max_streak}\n')
		win_rate_data = {}
		wins = 0
		for game in data['game_history']:
			game_data = list(game.values())[0]
			if game_data['won']:
				guesses = len(game_data) - 1
				if guesses in win_rate_data:
					win_rate_data[guesses] += 1
				else:
					win_rate_data[guesses] = 1
				wins += 1
		win_rate_data = list(sorted(list(win_rate_data.items()), key = lambda x: x[1]))[::-1]
		most_bars = win_rate_data[0][1]
		for i in range(1, 7):
			if i not in dict(win_rate_data):
				print(f"{i}  | 0")
			else:
				print(f"{i}  {'|' * round((dict(win_rate_data)[i] / most_bars) * 10 + 1)} {dict(win_rate_data)[i]}")
		weighted_sum = 0
		total = 0
		for n_guesses, amount in win_rate_data:
			weighted_sum += n_guesses * amount
			total += amount
		avg = weighted_sum / total
		print(f"Average: {round(avg, 2)}")
		print()

	def _calc_win_rate(self, data):
		"""
		This method calculates the win rate of the bot

		Parameters
		----------
		data:		dict
					bots overall game data
		"""
		if data['games_played'] == 0:
			return 0
		wins = 0
		for game in data['game_history']:
			game_data = list(game.values())[0]
			if game_data['won']:
				wins += 1
		return round(wins / data['games_played'] * 100)

	def _new_guess(self, guess_results, guess, prev_guesses, poss_words):
		"""
		This method is the brains behind finding what the next guess should be
		It looks through every possible word, and creates all possible outcomes of 
		that guess 
		i.e., (absent, present, correct, correct, present), (absent present, correct, correct, absent), etc
		It then calculates the entropy for each word, which can be thought of as the amount of
		information gained by picking said word. The word with the highest entropy is returned
		Watch https://www.youtube.com/watch?v=v68zYyaEmEA for more info

		Parameters
		----------
		guess_results:			list
								list of evaluation results from previous guess
		guess:					str
								previous guess
		prev_guesses:			list
								list of previous guesses
		poss_word:				list
								list of possible words
		
		Returns
		-------
		sorted_entropy[0][0]:	str
								word with highest entropy
		"""
		word_entropy_dict = {}
		for word in poss_words:
			if word not in prev_guesses or word not in PREV_ANSWERS:
				combinations = self._create_all_combinations(guess_results, word, guess, [], [])
				entropy_dict = self._find_next_poss_words(combinations, word, poss_words)
				entropy = self._get_entropy(entropy_dict, poss_words)
				word_entropy_dict[word] = entropy
		sorted_entropy = list(sorted(word_entropy_dict.items(), key = lambda x: x[1]))[::-1]
		return sorted_entropy[0][0]

	def _create_all_combinations(self, guess_results, word, guess_word, combinations, cur_combination):
		"""
		This method is a recursive search-based algorithm that creates every possible combination
		of evaluations (with same caveats)

		Parameters
		----------
		guess_results:			list
								list of evaluation results from previous guess
		word:					str
								potential new word to guess with
		guess_word:				str
								previous guess
		combinations:			
		"""
		if len(cur_combination) == 5 :
			combinations.append(cur_combination.copy())
			return combinations
		guess = guess_results[0]
		# if the current letter matches the other words letter at the same location, it must have the same evaluation
		if word[0] == guess_word[0]:
			cur_combination.append(guess)
			combinations = self._create_all_combinations(guess_results[1:], word[1:], guess_word[1:], combinations, cur_combination)
			cur_combination.pop()
		# if the evaluation of the current letter is green, and the current letter is not the same as the previous letter, it cannot be correct
		elif guess == 'correct' and word[0] != guess_word[0]:
			for evaluation in ['present', 'absent']:
				cur_combination.append(evaluation)
				combinations = self._create_all_combinations(guess_results[1:], word[1:], guess_word[1:], combinations, cur_combination)
				cur_combination.pop()
		# if the evaluation of the current letter is present and the current words letter is in the previous guess, it must cannot be absent
		elif guess == 'present' and word[0] in guess_word:
			for evaluation in ['present', 'correct']:
				cur_combination.append(evaluation)
				combinations = self._create_all_combinations(guess_results[1:], word[1:], guess_word[1:], combinations, cur_combination)
				cur_combination.pop()
		# otherwise search all possibilites
		else:
			for evaluation in ['correct', 'present', 'absent']:
				cur_combination.append(evaluation)
				combinations = self._create_all_combinations(guess_results[1:], word[1:], guess_word[1:], combinations, cur_combination)
				cur_combination.pop()
		return combinations

	def _get_entropy(self, entropy_dict, poss_words):
		"""
		This method calculates the entropy for a given word
		Entropy is calculated by the product of two parts
		p: which is the number of words possible with given outcome / total number of possible words
		log2(1/p):	represents how much information is cut out
		You then take the running sum of each outcome of p*log2(1/p)
		
		Parameters
		----------
		entropy_dict:	dict
						dictionary of {possible outcome : [list of words that fit outcome]}
		poss_words:		list
						list of possible words

		Returns
		-------
		entropy:		int
						entropy value 
		"""
		entropy = 0
		for guess in entropy_dict:
			num_words = len(entropy_dict[guess])
			p = num_words / len(poss_words)
			entropy += p * np.log2(1/p)
		return entropy

	def _find_poss_words(self, guess, guess_results, poss_words):
		"""
		This method creates a new list of possible words to pick from
		based on the what the previous guess and evaluations were

		Parameters
		----------
		guess:					str
								previous guess
		guess_results:			list
								list of evaluation results from previous guess

		Returns
		-------
		new_poss_words:			list
								list of possible words
		"""
		new_poss_words = []
		for word in poss_words:
			if word != guess and self._word_matches_guess(word, guess, guess_results):
				new_poss_words.append(word)
		return new_poss_words

	def _word_matches_guess(self, word, guess, guess_results):
		"""
		This method checks if a word matches an evaluation

		Parameters
		----------
		word:			str
						word that is being checked
		guess:			str
						previous guess
		guess_results	list
						list of evaluation results from previous guess

		Returns
		-------
		bool:			true if matches, otherwise false
		"""
		correct = {}
		present = []
		absent = []
		for i, (letter, evaluation) in enumerate(zip(guess, guess_results)):
			if evaluation == 'correct':
				correct[i] = letter
			elif evaluation == 'present':
				present.append(letter)
			elif evaluation == 'absent':
				absent.append(letter)
		for i, char in enumerate(word):
			if char in absent:
				return False
			if char != guess[i] and i in list(correct.keys()):
				return False
		return True

	def _find_next_poss_words(self, combinations, guess, poss_words):
		"""
		This method looks through every combination and finds every word that fits that
		combination. It then stores it into a dictionary of {combination: [list of words]}

		Parameters
		----------
		combinations:	list
						list of all combinations
		guess: 			str
						previous guess
		poss_words:		list
						list of all possible words

		Returns
		-------
		new_poss_words: list
						list of new possible words
		"""
		new_poss_words = {}
		for combination in combinations:
			comb_str = "".join(combination)
			for word in poss_words:
				if word != guess and self._word_matches_guess(word, guess, combination):
					if comb_str in new_poss_words:
						new_poss_words[comb_str].append(word)
					else:
						new_poss_words[comb_str] = [word]
		return new_poss_words

	def _guess(self, guess):
		"""
		This method inputs a guess into the wordle website and returns its evaluation

		Parmeters
		---------
		guess:			str
						guessed word

		Returns
		-------
		guess_results	list
						list of evaluation results
		"""
		query = f"""return document.querySelector('game-app').shadowRoot.querySelector('game-row[letters = "{guess}"]').shadowRoot.querySelectorAll('game-tile[letter]')"""
		guess_results = []
		sends = driver.find_element(By.XPATH, "/html/body")
		sends.click()
		sends.send_keys(guess)
		sends.send_keys(Keys.ENTER)
		inner_texts = [my_elem.get_attribute("outerHTML") for my_elem in driver.execute_script(query)]
		for inner_text in inner_texts:
			guess_results.append(inner_text.split()[2].split('"')[1])  # gets the result of each tile
			time.sleep(1)
		return guess_results



def main():
	bot = Bot()
	bot.run()



if __name__ == '__main__':
	main()