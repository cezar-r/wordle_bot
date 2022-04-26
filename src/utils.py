from words import PREV_ANSWERS
import numpy as np


def new_guess(guess_results, guess, prev_guesses, poss_words, prev_answers = PREV_ANSWERS):
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
			if word not in prev_guesses or word not in prev_answers:
				combinations = create_all_combinations(guess_results, word, guess, [], []) 
				entropy_dict = find_next_poss_words(combinations, word, poss_words) #
				entropy = get_entropy(entropy_dict, poss_words) #
				word_entropy_dict[word] = entropy
		sorted_entropy = list(sorted(word_entropy_dict.items(), key = lambda x: x[1]))[::-1]
		return sorted_entropy[0][0]


def create_all_combinations(guess_results, word, guess_word, combinations, cur_combination):
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
		evaluation = guess_results[0]
		# if the current letter matches the other words letter at the same location, it must have the same evaluation
		if word[0] == guess_word[0]:
			cur_combination.append(evaluation)
			combinations = create_all_combinations(guess_results[1:], word[1:], guess_word[1:], combinations, cur_combination)
			cur_combination.pop()
		# if the evaluation of the current letter is green, and the current letter is not the same as the previous letter, it cannot be correct
		elif evaluation == 'correct' and word[0] != guess_word[0]:
			for evaluation in ['present', 'absent']:
				cur_combination.append(evaluation)
				combinations = create_all_combinations(guess_results[1:], word[1:], guess_word[1:], combinations, cur_combination)
				cur_combination.pop()
		# if the evaluation of the current letter is present and the current words letter is in the previous guess, it must cannot be absent
		elif evaluation == 'present' and word[0] in guess_word:
			for evaluation in ['present', 'correct']:
				cur_combination.append(evaluation)
				combinations = create_all_combinations(guess_results[1:], word[1:], guess_word[1:], combinations, cur_combination)
				cur_combination.pop()
		# otherwise search all possibilites
		else:
			for evaluation in ['correct', 'present', 'absent']:
				cur_combination.append(evaluation)
				combinations = create_all_combinations(guess_results[1:], word[1:], guess_word[1:], combinations, cur_combination)
				cur_combination.pop()
		return combinations


def find_poss_words(guess, guess_results, poss_words, prev_answers = PREV_ANSWERS):
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
		if word != guess and word_matches_guess(word, guess, guess_results) and word not in prev_answers:
			new_poss_words.append(word)
	return new_poss_words


def find_next_poss_words(combinations, guess, poss_words):
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
			words_for_comb = find_poss_words(guess, combination, poss_words)
			if words_for_comb:
				new_poss_words[comb_str] = words_for_comb
		return new_poss_words


def word_matches_guess(word, guess, guess_results):
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
		if char in absent and char not in list(correct.values()) + present:
			return False
		if char != guess[i] and i in list(correct.keys()):
			return False
		if char == guess[i] and i not in correct:
			return False
	for char in present:
		if char not in word:
			return False
	for char in list(correct.values()):
		if char not in word:
			return False
	return True


def get_entropy(entropy_dict, poss_words):
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


def guessed_word(guess_results):
        """
        This method checks if a word has been guessed
        It looks through a list of evaluation tiles and
        if they are all green, it returns true

        Parameters
        ----------
        guess_results:  list
                        list of evalution tiles ("correct", "present", or "absent")

        Returns
        -------
        bool:           true if tiles are correct, otherwise false
        """
        for evaluation in guess_results:
            if evaluation != "correct":
                return False
        return True