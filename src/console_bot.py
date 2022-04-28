from game import Game
from utils import find_poss_words, new_guess, guessed_word
from words import WORDBANK
from datetime import datetime


class ConsoleWordleBot:
    """
    This method represents a bot that plays on the 
    command line. It is initialized with the first
    guess.
    """
    def __init__(self, first_guess, verbose = False):
        self.data = []
        self.verbose = verbose
        self.first_guess = first_guess

    def play_game(self, game = None):
        """
        This method plays a game of Wordle. It returns
        when it either solves the puzzle or runs out of
        guesses. 

        Parameters
        ----------
        game:       Game()
                    game to play on, otherwise create new one

        Returns
        -------
        bool:       true if won, false if lost
        """
        if not game:
            game = Game()
        guess = self.first_guess
        poss_words = WORDBANK
        guesses = 0
        prev_guesses = []
        prev_guess_results = []
        won = False
        start = datetime.now()
        while guesses < 6:
            guesses += 1
            guess_results = game.check_guess(guess)
            prev_guesses.append(guess)
            if guessed_word(guess_results):
                won = True
                break
            poss_words = find_poss_words(guess, guess_results, poss_words, [])
            guess = new_guess(guess_results, guess, prev_guesses, poss_words, [])

        elapsed = (datetime.now() - start).total_seconds()
        self._update_data(prev_guesses, prev_guess_results, won, game, elapsed)
        if self.verbose:
            self.display_game(idx = -1)
        return won

    def get_data(self):
        """This method returns the bots data"""
        return self.data

    def display_data(self):
        """This method displays the bots data"""
        wins = 0
        losses = 0
        num_guesses = 0
        lost_on = []
        total_elapsed = 0
        distribution = {}
        for game in self.data:
            if game['won']:
                wins += 1
                guesses = game['num_guesses']
                if guesses in distribution:
                    distribution[guesses] += 1
                else:
                    distribution[guesses] = 1
                num_guesses += game['num_guesses']
            else:
                losses += 1
                lost_on.append(game['answer'])
            total_elapsed += game['time_to_solve']
        print(f'Bot data using "{self.first_guess.upper()}" as first word after {len(self.data)} games:\n\nWin rate: {wins/(wins+losses) * 100}%\nAvg Guesses: {num_guesses/wins}\nAvg Time Spent: {round(total_elapsed / wins+losses, 2)} seconds\n')
        
        win_rate_data = list(sorted(list(distribution.items()), key = lambda x: x[1]))[::-1]
        most_bars = win_rate_data[0][1]
        for i in range(1, 7):
            if i not in dict(win_rate_data):
                print(f"{i}  | 0")
            else:
                print(f"{i}  {'|' * round((dict(win_rate_data)[i] / most_bars) * 10 + 1)} {dict(win_rate_data)[i]}")
        
        if lost_on:
            print("Lost on words:")
            for elem in lost_on:
                print(elem)
        print()

    def display_game(self, idx = None, correct_answer = None):
        """
        This method displays a specific game, which can be found
        either by index or by the correct answer for that wordle

        Parameters
        ----------
        idx:            int
                        idx'th game
        correct_answer: str
                        correct answer for the game
        """
        if idx:
            for key, val in list(self.data[idx].items()):
                print(f"{key}: {val}")
        elif correct_answer:
            for i, game in enumerate(self.data):
                if game['correct_answer'] == correct_answer:
                    return self.display_game(idx = i)

    def _update_data(self, prev_guesses, prev_guess_results, won, game, elapsed):
        """
        This method updates the bot data with the current game

        Parameters
        ----------
        prev_guesses:       list
                            list of previous guesses
        won:                bool
                            true if game was won, otherwise false
        game:               Game()
                            game object of game     
        """
        game_data = {}
        game_data['won'] = won 
        for i, (guess, _eval) in enumerate(zip(prev_guesses, prev_guess_results)):
            game_data[f"guess_{i+1}"] = guess
            game_data[f"eval_{i+1}"] = _eval
        game_data['num_guesses'] = len(prev_guesses)
        game_data['answer'] = game.get_answer()
        game_data['time_to_solve'] = round(elapsed, 2)
        self.data.append(game_data)


if __name__ == '__main__':
    bot = ConsoleWordleBot("slate", verbose = True)
    bot.play_game()