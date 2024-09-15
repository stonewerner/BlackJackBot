# Blackjack Game with GUI

This project is a Python implementation of the classic casino game Blackjack, featuring a graphical user interface built with Tkinter.

## Table of Contents

1. [Features](#features)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [How to Play](#how-to-play)
5. [Game Rules](#game-rules)
6. [Project Structure](#project-structure)
7. [Future Improvements](#future-improvements)


## Features

- Graphical User Interface using Tkinter
- Support for multiple decks (1-8)
- Player wallet and betting system
- Basic Blackjack gameplay (Hit, Stand)
- Dealer AI following standard casino rules

## Requirements

- Python 3.6 or higher
- Tkinter (usually comes pre-installed with Python)

## Installation

1. Ensure you have Python installed on your system. If not, download and install it from [python.org](https://www.python.org/downloads/).

2. Clone this repository or download the source code.

   ```
   git clone https://github.com/stonewerner/BlackJackBot.git
   cd BlackJackBot
   ```

3. No additional libraries need to be installed as the game uses only built-in Python modules.

## How to Play

1. Run the game by executing the following command in your terminal:

   ```
   python new_game.py
   ```

2. When prompted, enter the number of decks you want to play with (1-8).

3. Place your bet for each round when prompted.

4. Use the "Hit" button to request another card, or "Stand" to keep your current hand.

5. Try to get as close to 21 as possible without going over.

6. The dealer will play their hand after you stand, and the winner will be determined.

7. Click "New Game" to start a new round.

## Game Rules

- The goal is to beat the dealer's hand without going over 21.
- Face cards (Jack, Queen, King) are worth 10. Aces are worth 1 or 11, whichever makes a better hand.
- Each player starts with two cards, one of the dealer's cards is hidden until the end.
- To 'Hit' is to ask for another card. To 'Stand' is to hold your total and end your turn.
- If you go over 21 you bust, and the dealer wins regardless of the dealer's hand.
- Dealer will hit until their cards total 17 or higher.

## Project Structure

- `new_game.py`: Main game file containing all classes and GUI implementation
- `README.md`: This file, containing project information and instructions

## Future Improvements

- Add card images for a more visual experience
- Implement additional game features like splitting and doubling down
- Add sound effects for a more immersive gameplay
- Create a high score system
- Implement more advanced betting strategies
- Implement game theory optimal coaching


Enjoy playing Blackjack and feel free to contribute to the project!