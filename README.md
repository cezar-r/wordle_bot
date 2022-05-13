# Solving Wordle Using Information Theory

https://user-images.githubusercontent.com/59450965/167795616-217c5307-0860-4376-8c39-3c2fbe1ca1ae.mp4


## Motive
This program was mainly inspired by the [video posted by 3Blue1Brown](https://www.youtube.com/watch?v=v68zYyaEmEA), in which he explains how wordle can be solved using information theory. This program incorporates the math from the video and sends requests to the [Wordle website](https://www.nytimes.com/games/wordle/index.html) to solve the daily puzzle. Follow the bot on [Twitter](https://twitter.com/WordleMachine) to keep up to date on its results.

## Installing and Running

### Chromedriver
- Be sure to install your Chrome's current version of [chromedriver](https://chromedriver.chromium.org/downloads) to your `C:\Program Files (x86)` folder. This is used to launch the browser and communicate with the Wordle website.
- You can find your Chrome version by typing `chrome://settings/help` into your search bar.

### Installation
- ```git clone https://github.com/cezar-r/wordle_bot```
- `cd wordle_bot/src`
- `pip install -r requirements.txt`

### Running Browser Bot
- `python main.py`

### Running Simulations
- `python simulate.py <n_simulations> <first_guess1> <first_guess2> ... <first_guessn>`
- Ex: `python simulate.py 100 slate crate crane`

## Performance
- Below is a screenshot of the Wordle bot after playing 2000 games using `slate` `dealt` `crane` and `soare` as its first guesses. The bot itself has no knowledge of possible answers, its corpus is the 12,000 word file of allowed guesses. It also has no knowledge of word commonality at the moment. Lastly, the bot plays Wordle on hard mode.
<img src = "https://github.com/cezar-r/wordle_bot/blob/main/src/simulation_results_2.png">
