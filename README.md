# Solving Wordle Using Information Theory

https://user-images.githubusercontent.com/59450965/164546807-89b46729-2057-44b3-b859-3c9e5f329f0b.mp4

## Motive
This program was mainly inspired by the [video posted by 3Blue1Brown](https://www.youtube.com/watch?v=v68zYyaEmEA), in which he explains how wordle can be solved using information theory. This program incorporates the math from the video and sends requests to the [Wordle website](https://www.nytimes.com/games/wordle/index.html) to solve the daily puzzle.

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
- `python simulate.py <n_simulations> <first_guess1> <first_guess2> ... <first_guessn>
- Ex: `python simulate 100 slate crate crane`
