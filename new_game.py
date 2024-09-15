import random
import tkinter as tk
from tkinter import messagebox, simpledialog

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
    

class BlackjackGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Blackjack")
        self.master.geometry("600x500")  # Increased height for new section

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

        # New section for Coach's Hints
        self.hint_frame = tk.Frame(self.master)
        self.hint_frame.pack(pady=10)

        self.hint_label = tk.Label(self.hint_frame, text="Coach's Hint: ")
        self.hint_label.pack(side=tk.LEFT)

        self.hint_text = tk.StringVar()
        self.hint_display = tk.Label(self.hint_frame, textvariable=self.hint_text)
        self.hint_display.pack(side=tk.LEFT)

        self.hint_button = tk.Button(self.hint_frame, text="Show Hint", command=self.toggle_hint)
        self.hint_button.pack(side=tk.LEFT, padx=10)

        self.hint_visible = False

    def toggle_hint(self):
        self.hint_visible = not self.hint_visible
        if self.hint_visible:
            self.hint_button.config(text="Hide Hint")
            self.update_hint()
        else:
            self.hint_button.config(text="Show Hint")
            self.hint_text.set("")

    def update_hint(self):
        if self.hint_visible:
            player_value = self.player.get_hand_value()
            dealer_up_card = self.dealer.hand[0].value
            hint = self.get_optimal_move(player_value, dealer_up_card)
            self.hint_text.set(hint)
        else:
            self.hint_text.set("")

    def get_optimal_move(self, player_value, dealer_up_card):
        # Basic strategy for when to hit or stand
        if player_value <= 11:
            return "Hit"
        elif player_value == 12:
            return "Hit" if dealer_up_card in [2, 3, 7, 8, 9, 10, 11] else "Stand"
        elif 13 <= player_value <= 16:
            return "Hit" if dealer_up_card in [7, 8, 9, 10, 11] else "Stand"
        else:  # player_value >= 17
            return "Stand"


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

        self.update_hint()
        self.update_display()


    def hit(self):
        self.player.add_card(self.deck.draw())
        self.update_display()
        self.update_hint()

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
        self.update_hint()

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