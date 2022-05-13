from words import PREV_ANSWERS, WORDBANK
from datetime import datetime
from datetime import timedelta
import numpy as np

color_dict = {'present' : "🟨",
                'correct' : "🟩",
                'absent' : "🏴󠁵󠁳󠁴󠁸󠁿"}


def time_until_end_of_today():
    """This method returns the number of seconds until midnight"""
    time_delta = datetime.combine(datetime.now().date() + timedelta(days=1), datetime.strptime("0000", "%H%M").time()) - datetime.now()
    return time_delta


def new_guess(corpus, poss_words, prev_guesses, prev_answers = PREV_ANSWERS):
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
    corpus:                 list
                            list of words to look over
    poss_words:             list
                            list of possible words
    prev_guesses:           list
                            list of previous guesses
    prev_answers:           list 
                            list of previous answers

    Returns
    -------
    sorted_entropy[0][0]:   str
                            word with highest entropy
    """
    word_entropy = {}
    for word in corpus:
        if word not in prev_guesses and word not in prev_answers:
            poss_answers = {}
            for poss_answer in poss_words:
                result = check_guess(word, poss_answer)
                result_str = "".join(result)
                if result_str in poss_answers:
                    poss_answers[result_str].append(word)
                else:
                    poss_answers[result_str] = [word]
            entropy = get_entropy(poss_answers, poss_words)
            word_entropy[word] = entropy 
    sorted_entropy = sorted(list(word_entropy.items()), key = lambda x: x[1])[::-1]
    return sorted_entropy[0][0]


def check_guess(guess, answer):
    """
    This method evaluates a guess relative to the correct 
    answer similar to how the Wordle game does it

    Parameters
    ----------
    guess:      str
                guessed word

    Returns
    -------
    evaluation: list
                list of all evaluations
    """
    def remove_correct(evaluation, word):
        """This method removes all the correct letters from the answer"""
        new_word = ""
        for i, char in enumerate(word):
            if i in evaluation and evaluation[i] != "correct":
                new_word += char
            elif i not in evaluation:
                new_word += char
        return new_word 

    freq_dict = {}
    idx_dict = {}
    for i, keys in enumerate(answer):
        freq_dict[keys] = freq_dict.get(keys, 0) + 1
        idx_dict[i] = keys

    evaluation = {}
    for i, (cur_letter, corr_letter) in enumerate(list(zip(guess, answer))):
        if cur_letter == corr_letter:
            evaluation[i] = "correct"
            freq_dict[cur_letter] -= 1
        elif cur_letter not in answer:
            evaluation[i] = "absent"

    for i, (cur_letter, corr_letter) in enumerate(list(zip(guess, answer))):
        if i not in evaluation:
            if cur_letter in remove_correct(evaluation, answer) and freq_dict[cur_letter] > 0:
                evaluation[i] = "present"
                freq_dict[cur_letter] -= 1
            else:
                evaluation[i] = "absent"

    sorted_eval = dict(sorted(list(evaluation.items()), key = lambda x: x[0]))
    return list(sorted_eval.values())


def find_poss_words(guess, guess_results, poss_words, prev_answers = PREV_ANSWERS):
    """
    This method creates a new list of possible words to pick from
    based on the what the previous guess and evaluations were

    Parameters
    ----------
    guess:                  str
                            previous guess
    guess_results:          list
                            list of evaluation results from previous guess

    Returns
    -------
    new_poss_words:         list
                            list of possible words
    """
    new_poss_words = []
    for word in poss_words:
        if word != guess and word_matches_guess(word, guess, guess_results) and word not in prev_answers:
            new_poss_words.append(word)
    return sorted(new_poss_words)


def word_matches_guess(word, guess, guess_results):
    """
    This method checks if a word matches an evaluation

    Parameters
    ----------
    word:           str
                    word that is being checked
    guess:          str
                    previous guess
    guess_results   list
                    list of evaluation results from previous guess

    Returns
    -------
    bool:           true if matches, otherwise false
    """
    def word_has_n_present_p(word, char, count, correct):
        found = 0 
        for i, _char in enumerate(word):
            if _char == char:
                if i in correct and correct[i] != _char:
                    found += 1
                elif i not in correct:
                    found += 1
        return found >= count

    correct = {}
    present = {}
    absent = []
    for i, (letter, evaluation) in enumerate(zip(guess, guess_results)):
        if evaluation == 'correct':
            correct[i] = letter
        elif evaluation == 'present':
            if letter in present:
                present[letter] += 1
            else:
                present[letter] = 1
        elif evaluation == 'absent':
            absent.append(letter)

    for i, (char1, char2) in enumerate(list(zip(word, guess))):
        if char2 in present and char1 == char2 and i not in correct:
            return False 

    for i, (char1, char2) in enumerate(list(zip(word, guess))):
        if char1 == char2 and char1 in absent and i not in correct:
            return False    

    for idx in correct:
        if guess[idx] != word[idx]:
            return False

    for char, count in list(present.items()):
        if not word_has_n_present_p(word, char, count, correct):
            return False

    for char in absent:
        if char in word and char not in list(correct.values()) + list(present.keys()):
            return False
    return True



def get_entropy(entropy_dict, poss_words):
        """
        This method calculates the entropy for a given word
        Entropy is calculated by the product of two parts
        p: which is the number of words possible with given outcome / total number of possible words
        log2(1/p):  represents how much information is cut out
        You then take the running sum of each outcome of p*log2(1/p)
        
        Parameters
        ----------
        entropy_dict:   dict
                        dictionary of {possible outcome : [list of words that fit outcome]}
        poss_words:     list
                        list of possible words

        Returns
        -------
        entropy:        int
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