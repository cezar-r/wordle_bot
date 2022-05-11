import random

from words import POSS_ANSWERS
from utils import check_guess, color_dict


class Game:
    """
    This class represents a Wordle game interface. I creates 
    a random answer when initialized and has a method
    that evaluates each guess.
    """
    def __init__(self, answer = None, verbose = False):
        if not answer:
            self.answer = random.choice(list(POSS_ANSWERS ))
        else:
            self.answer = answer
        self.guess_results = []
        self.verbose = verbose


    def check_guess(self, guess):
        """
        This method evaluates a guess relative to the correct 
        answer similar to how the Wordle game does it

        Parameters
        ----------
        guess:      str
                    guessed word

        Returns
        -------
        results:    list
                    list of all evaluations
        """ 
        results = check_guess(guess, self.answer)
        result_str = "".join([color_dict[evaluation] for evaluation in results])
        self.guess_results.append(result_str)
        if self.verbose:
            print(f'{guess}\n{result_str}')
        return results


    def guess_results_as_string(self):
        """This method returns the entire results into a str
        Similar to what is seen when copying your wordle results"""
        string = ""
        for result in self.guess_results:
            string  += result + "\n"
        return string


    def get_answer(self):
        """This method returns the correct answer"""
        return self.answer