import os
import time
import json
import warnings
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from words import WORDBANK, PREV_ANSWERS
from utils import find_poss_words, new_guess, guessed_word

warnings.filterwarnings("ignore")
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path = "C:\Program Files (x86)\chromedriver.exe", service_log_path='NUL', options = options)
url = "https://www.nytimes.com/games/wordle/"
driver.get(url)
time.sleep(1)


class WordleBot:
    """
    This class represents the bot that plays wordle
    Its data is stored in a json file and its first guess is
    given by the mathematically optimal first word; soare
    The current wordle should be set to whatever wordle the 
    previous days wordle was
    """
    def __init__(self, filename = "data.json", first_guess = "slate", cur_wordle = 307):
        self.filename = filename
        self.first_guess = first_guess
        self.cur_wordle = cur_wordle
        self.data = json.load(open(self.filename, encoding="utf-8"))

    def run(self):
        """
        This method runs the bot. It checks if there is
        a new wordle to played, and if there is, it attempts
        to complete the puzzle. Otherwise, it continuously 
        checks for a new wordle every 5 seconds
        """
        i = 1
        while not self._new_wordle():
            dots_str = "." * ((i % 3) + 1)
            print("Waiting for new wordle" + dots_str, end = "\r")
            i += 1
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
        bool:   true if new wordle, otherwise false
        """
        driver.refresh() 
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
        prev_guess_results = []
        poss_words = WORDBANK
        while guesses < 6:
            guesses += 1
            guess_results = self._guess(guess)
            prev_guesses.append(guess)
            prev_guess_results.append(guess_results)
            if guessed_word(guess_results):
                PREV_ANSWERS.add(guess)
                self._update_prev_answers_file(guess)
                self._write_out(prev_guesses, prev_guess_results, True)
                return
            poss_words = find_poss_words(guess, guess_results, poss_words, PREV_ANSWERS)
            guess = new_guess(guess_results, guess, prev_guesses, poss_words, PREV_ANSWERS)
            

        self._write_out(prev_guesses, prev_guess_results, False)

    def _update_prev_answers_file(self, guess):
        prev_answers = open("prev_answers.txt", "a")
        prev_answers.write(f"{guess}\n")
        prev_answers.close()

    def _write_out(self, prev_guesses, prev_guess_results, won):
        """
        This method writes out the game data to a file

        Parameters
        ----------
        prev_guesses:   list
                        list of guesses used
        won:            bool
                        true if game was won
        """
        color_dict = {'present' : "🟨",
                'correct' : "🟩",
                'absent' : "🏴󠁵󠁳󠁴󠁸󠁿"}

        key = "wordle_" + str(self.cur_wordle)
        data = self.data['data']
        game_data = {}
        game_data['won'] = won
        for i, (guess, _eval) in enumerate(zip(prev_guesses, prev_guess_results)):
            game_data[f'guess_{i+1}'] = guess
            game_data[f'eval_{i+1}'] = "".join([color_dict[evaluation] for evaluation in _eval])
        data['game_history'][key] = game_data
        data['games_played'] = len(data['game_history'])
        if won:
            data['cur_streak'] = self._calc_cur_streak(data)
        else:
            data['cur_streak'] = 0
        data['max_streak'] = max(data['max_streak'], data['cur_streak'])
        data['win_rate'] = self._calc_win_rate(data)

        json_string = json.dumps({"data" : data}, indent = 4, ensure_ascii=False)
        with open(self.filename, 'w', encoding="utf-8") as outfile:
            outfile.write(json_string)
        self._display_stats()

    def _display_stats(self):
        """
        This method displays the bots data to the console
        """
        self.data = json.load(open(self.filename, encoding="utf-8"))
        data = self.data['data']
        games_played = data['games_played']
        win_rate = data['win_rate']
        cur_streak = data['cur_streak']
        max_streak = data['max_streak']

        print(f'\nGames played: {games_played}\nWin rate: {win_rate}%\nCurrent streak: {cur_streak}\nMax streak: {max_streak}\n')
        win_rate_data = {}
        wins = 0
        for game in list(data['game_history'].values()):
            if game['won']:
                guesses = len(game) // 2
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

    def _calc_cur_streak(self, data):
        """
        This method calculates the current streak of the bot

        Parameters
        ----------
        data:       dict
                    bots overall game data
        """
        cur_streak = 0
        for game in list(data['game_history'].values())[::-1]:
            if game['won']:
                cur_streak += 1
            else:
                return cur_streak
        return cur_streak

    def _calc_win_rate(self, data):
        """
        This method calculates the win rate of the bot

        Parameters
        ----------
        data:       dict
                    bots overall game data
        """
        if data['games_played'] == 0:
            return 0
        wins = 0
        for game in list(data['game_history'].values()):
            if game['won']:
                wins += 1
        return round(wins / data['games_played'] * 100)

    def _guess(self, guess):
        """
        This method inputs a guess into the wordle website and returns its evaluation

        Parmeters
        ---------
        guess:          str
                        guessed word

        Returns
        -------
        guess_results   list
                        list of evaluation results
        """
        query = f"""return document.querySelector('game-app').shadowRoot.querySelector('game-row[letters = "{guess}"]').shadowRoot.querySelectorAll('game-tile[letter]')"""
        guess_results = []
        sends = driver.find_element(By.XPATH, "/html/body")
        sends.click()
        for char in guess:
            sends.send_keys(char)
            time.sleep(.2)
        sends.send_keys(Keys.ENTER)
        inner_texts = [my_elem.get_attribute("outerHTML") for my_elem in driver.execute_script(query)]
        for inner_text in inner_texts:
            guess_results.append(inner_text.split()[2].split('"')[1])  # gets the result of each tile
            time.sleep(1)
        return guess_results