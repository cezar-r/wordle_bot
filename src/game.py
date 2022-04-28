import random

from words import WORDBANK


class Game:
	"""
	This class represents a Wordle game interface. I creates 
	a random answer when initialized and has a method
	that evaluates each guess.
	"""
	def __init__(self, answer = None):
		if not answer:
			self.answer = random.choice(list(WORDBANK))
		else:
			self.answer = answer
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

		def remove_correct(evaluation, word):
			new_word = ""
			for i, char in enumerate(word):
				if i in evaluation and evaluation[i] != "correct":
					new_word += char
				elif i not in evaluation:
					new_word += char
			return new_word 

		freq_dict = {}
		idx_dict = {}
		for i, keys in enumerate(self.answer):
			freq_dict[keys] = freq_dict.get(keys, 0) + 1
			idx_dict[i] = keys

		evaluation = {}
		for i, (cur_letter, corr_letter) in enumerate(list(zip(guess, self.answer))):
			if cur_letter == corr_letter:
				evaluation[i] = "correct"
			elif cur_letter not in self.answer:
				evaluation[i] = "absent"

		for i, (cur_letter, corr_letter) in enumerate(list(zip(guess, self.answer))):
			if i not in evaluation:
				if cur_letter in remove_correct(evaluation, self.answer) and freq_dict[cur_letter] > 0:
					evaluation[i] = "present"
					freq_dict[cur_letter] -= 1
				else:
					evaluation[i] = "absent"

		sorted_eval = dict(sorted(list(evaluation.items()), key = lambda x: x[0]))
		return list(sorted_eval.values())


	def get_answer(self):
		"""This method returns the correct answer"""
		return self.answer