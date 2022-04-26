import random

from words import WORDBANK


class Game:
	"""
	This class represents a Wordle game interface. I creates 
	a random answer when initialized and has a method
	that evaluates each guess.
	"""
	def __init__(self):
		self.answer = random.choice(list(WORDBANK))

	def check_guess(self, guess):
		"""
		This method evaluates a guess relative to the correct 
		answer similar to how the Wordle game does it

		Parameters
		----------
		guess:		str
					guessed word

		Returns
		-------
		evaluation:	list
					list of all evaluations
		"""
		freq_dict = {}
		for i, keys in enumerate(self.answer):
			freq_dict[keys] = freq_dict.get(keys, 0) + 1

		evaluation = []
		for i, (cur_letter, corr_letter) in enumerate(list(zip(guess, self.answer))):
			if cur_letter == corr_letter:
				evaluation.append('correct')
				freq_dict[cur_letter] -= 1
			elif cur_letter not in self.answer:
				evaluation.append('absent')
			elif cur_letter in self.answer:
				if freq_dict[cur_letter] == 0 or cur_letter == self.answer[i]:
					evaluation.append('absent')
				else:
					evaluation.append('present')
					freq_dict[cur_letter] -= 1
		return evaluation

	def get_answer(self):
		"""This method returns the correct answer"""
		return self.answer