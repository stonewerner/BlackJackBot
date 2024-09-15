import random

STARTING_WALLET = 100
SUITS = ['heart', 'spade', 'club', 'diamond']
RANKS = list(range(2, 11)) + ['jack', 'queen', 'king', 'ace']
MIN_DECKS = 1
MAX_DECKS = 8

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = str(rank)
        self.value = 10 if rank in ['jack', 'queen', 'king'] else 11 if rank == 'ace' else int(rank)

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

class Deck:
    def __init__(self, num_decks):
        self.num_decks = num_decks
        self.reset()

    def reset(self):
        self.cards = [Card(suit, rank) for _ in range(self.num_decks) for suit in SUITS for rank in RANKS]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop() if self.cards else None

    def __len__(self):
        return len(self.cards)

class Player:
    def __init__(self, is_dealer=False):
        self.hand = []
        self.is_dealer = is_dealer
        self.wallet = STARTING_WALLET if not is_dealer else None

    def add_card(self, card):
        self.hand.append(card)

    def get_hand_value(self):
        value = sum(card.value for card in self.hand)
        num_aces = sum(1 for card in self.hand if card.rank == 'ace')
        while value > 21 and num_aces:
            value -= 10
            num_aces -= 1
        return value

    def clear_hand(self):
        self.hand.clear()

    def __repr__(self):
        return f"{'Dealer' if self.is_dealer else 'Player'}'s hand: {self.hand}, Value: {self.get_hand_value()}"
    
"""

def get_action(prompt, valid_inputs):
    while True:
        action = input(prompt).upper()
        if action in valid_inputs:
            return action
        print("Invalid input")

def get_bet(wallet):
    while True:
        try:
            bet = int(input(f"Enter your bet (1-{wallet}): "))
            if 1 <= bet <= wallet:
                return bet
            print(f"Invalid bet. Must be between 1 and {wallet}")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_num_decks():
    while True:
        try:
            num_decks = int(input(f"Enter the number of decks to play with ({MIN_DECKS}-{MAX_DECKS}): "))
            if MIN_DECKS <= num_decks <= MAX_DECKS:
                return num_decks
            print(f"Invalid number. Must be between {MIN_DECKS} and {MAX_DECKS}")
        except ValueError:
            print("Invalid input. Please enter a number.")

def play_round(deck, player, dealer):
    player.clear_hand()
    dealer.clear_hand()
    
    bet = get_bet(player.wallet)
    
    for _ in range(2):
        player.add_card(deck.draw())
        dealer.add_card(deck.draw())

    print(f"Your hand: {player.hand}")
    print(f"Dealer's face-up card: {dealer.hand[1]}")

    # Player's turn
    while player.get_hand_value() < 21:
        action = get_action("H for Hit, S for Stand: ", ['H', 'S'])
        if action == 'S':
            break
        player.add_card(deck.draw())
        print(f"Your hand: {player.hand}")
        if player.get_hand_value() > 21:
            print("You bust!")
            player.wallet -= bet
            return

    player_value = player.get_hand_value()
    
    # Dealer's turn
    print(f"Dealer's hand: {dealer.hand}")
    while dealer.get_hand_value() < 17:
        dealer.add_card(deck.draw())
        print(f"Dealer draws: {dealer.hand[-1]}")
    
    dealer_value = dealer.get_hand_value()

    # Determine winner
    if dealer_value > 21:
        print("Dealer busts! You win!")
        player.wallet += bet
    elif player_value > dealer_value:
        print("You win!")
        player.wallet += bet
    elif player_value < dealer_value:
        print("Dealer wins.")
        player.wallet -= bet
    else:
        print("It's a tie!")

    print(f"Your wallet: ${player.wallet}")

def main():
    num_decks = get_num_decks()
    deck = Deck(num_decks)
    player = Player()
    dealer = Player(is_dealer=True)

    print(f"Starting game with {num_decks} deck{'s' if num_decks > 1 else ''}.")

    while player.wallet > 0:
        play = get_action("S to Start a new round, Q to Quit: ", ['S', 'Q'])
        if play == 'Q':
            break
        play_round(deck, player, dealer)
        if len(deck) < 20 * num_decks:  # Reshuffle when deck is low
            print("Reshuffling the deck...")
            deck.reset()

    print("Thanks for playing!")

if __name__ == "__main__":
    main()

    """

import tkinter as tk
from tkinter import messagebox, simpledialog
import random

# ... [Previous Card, Deck, and Player classes remain the same] ...

class BlackjackGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Blackjack")
        self.master.geometry("600x400")

        self.num_decks = self.get_num_decks()
        self.deck = Deck(self.num_decks)
        self.player = Player()
        self.dealer = Player(is_dealer=True)

        self.create_widgets()
        self.new_game()

    def get_num_decks(self):
        return simpledialog.askinteger("Number of Decks", 
                                       f"Enter the number of decks to play with ({MIN_DECKS}-{MAX_DECKS}):",
                                       minvalue=MIN_DECKS, maxvalue=MAX_DECKS)

    def create_widgets(self):
        self.dealer_frame = tk.Frame(self.master)
        self.dealer_frame.pack(pady=10)

        self.player_frame = tk.Frame(self.master)
        self.player_frame.pack(pady=10)

        self.dealer_label = tk.Label(self.dealer_frame, text="Dealer's Hand:")
        self.dealer_label.pack()

        self.dealer_cards = tk.Label(self.dealer_frame, text="")
        self.dealer_cards.pack()

        self.player_label = tk.Label(self.player_frame, text="Your Hand:")
        self.player_label.pack()

        self.player_cards = tk.Label(self.player_frame, text="")
        self.player_cards.pack()

        self.hit_button = tk.Button(self.master, text="Hit", command=self.hit)
        self.hit_button.pack(side=tk.LEFT, padx=10)

        self.stand_button = tk.Button(self.master, text="Stand", command=self.stand)
        self.stand_button.pack(side=tk.LEFT, padx=10)

        self.new_game_button = tk.Button(self.master, text="New Game", command=self.new_game)
        self.new_game_button.pack(side=tk.LEFT, padx=10)

        self.wallet_label = tk.Label(self.master, text=f"Wallet: ${self.player.wallet}")
        self.wallet_label.pack(side=tk.RIGHT, padx=10)

    def new_game(self):
        self.player.clear_hand()
        self.dealer.clear_hand()
        
        if len(self.deck) < 20 * self.num_decks:
            self.deck.reset()

        bet = simpledialog.askinteger("Place Your Bet", f"Enter your bet (1-{self.player.wallet}):",
                                      minvalue=1, maxvalue=self.player.wallet)
        if bet is None:
            return

        self.current_bet = bet

        for _ in range(2):
            self.player.add_card(self.deck.draw())
            self.dealer.add_card(self.deck.draw())

        self.update_display()

    def hit(self):
        self.player.add_card(self.deck.draw())
        self.update_display()

        if self.player.get_hand_value() > 21:
            self.end_game("You bust! Dealer wins.")

    def stand(self):
        while self.dealer.get_hand_value() < 17:
            self.dealer.add_card(self.deck.draw())

        self.update_display(show_all=True)
        self.end_game(self.determine_winner())

    def update_display(self, show_all=False):
        self.player_cards.config(text=", ".join(str(card) for card in self.player.hand))
        if show_all:
            self.dealer_cards.config(text=", ".join(str(card) for card in self.dealer.hand))
        else:
            self.dealer_cards.config(text=f"{self.dealer.hand[0]}, Hidden Card")

        self.wallet_label.config(text=f"Wallet: ${self.player.wallet}")

    def determine_winner(self):
        player_value = self.player.get_hand_value()
        dealer_value = self.dealer.get_hand_value()

        if dealer_value > 21:
            self.player.wallet += self.current_bet
            return "Dealer busts! You win!"
        elif player_value > dealer_value:
            self.player.wallet += self.current_bet
            return "You win!"
        elif player_value < dealer_value:
            self.player.wallet -= self.current_bet
            return "Dealer wins."
        else:
            return "It's a tie!"

    def end_game(self, message):
        self.update_display(show_all=True)
        messagebox.showinfo("Game Over", message)
        if self.player.wallet <= 0:
            messagebox.showinfo("Game Over", "You're out of money! Game over.")
            self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = BlackjackGUI(root)
    root.mainloop()