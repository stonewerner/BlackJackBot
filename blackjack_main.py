#import numpy as np
import random

STARTING_WALLET = 100


###RULES#####
'''
aces are counted as 11
thus, dealer must stand on a "soft" 17
blackjack pays 1.5x the bet
BONUSES:
splitting - when you're dealt 2 cards of equal value, can split and play 2 hands
betting - implement placing a bet and keeping track of your $$$
dynamic value of aces

card counting* - because cards are dealt at random WITH REPLACEMENT, the "count" isn't really accurate

'''

###CLASSES######################################################
'''
the card class
suit: heart, club, spade, diamond
value: 1 - 10
name: int or 'king', 'queen' etc
'''
class Card:
    
    def __init__(self, suit, name, value):
        self.suit = suit
        self.name = str(name)
        self.value = value


    def __repr__(self):
        return str(self.name) + " of " + self.suit



'''
the deck class
deck: an array of 52 card objects
'''
class Deck:

    #initialize deck with empty array
    def __init__(self):
        self.deck = []

    def fill_deck(self):

        #hearts
        for i in range(2, 11):
            self.deck.append(Card('heart', i, i))
        self.deck.append(Card('heart', 'jack', 10))
        self.deck.append(Card('heart', 'queen', 10))
        self.deck.append(Card('heart', 'king', 10))
        self.deck.append(Card('heart', 'ace', 11))

        #spades
        for i in range(2, 11):
            self.deck.append(Card('spade', i, i))
        self.deck.append(Card('spade', 'jack', 10))
        self.deck.append(Card('spade', 'queen', 10))
        self.deck.append(Card('spade', 'king', 10))
        self.deck.append(Card('spade', 'ace', 11))

        #clubs
        for i in range(2, 11):
            self.deck.append(Card('club', i, i))
        self.deck.append(Card('club', 'jack', 10))
        self.deck.append(Card('club', 'queen', 10))
        self.deck.append(Card('club', 'king', 10))
        self.deck.append(Card('club', 'ace', 11))

        #diamonds
        for i in range(2, 11):
            self.deck.append(Card('diamond', i, i))
        self.deck.append(Card('diamond', 'jack', 10))
        self.deck.append(Card('diamond', 'queen', 10))
        self.deck.append(Card('diamond', 'king', 10))
        self.deck.append(Card('diamond', 'ace', 11))

    #requires numpy
    '''def shuffle(self):
        np.random.shuffle(self.deck)
    '''

    def get_rand_card(self):
        return self.deck[random.randint(0, 51)]

'''
the player class
hand: array of cards in hand
count: Running total (int)
'''
class Player:

    def __init__(self):
        self.hand = []
        self.count = 0
        self.wallet = STARTING_WALLET

    def add_card(self, card):
        self.hand.append(card)
        self.count += card.value

    def clear_hand(self):
        self.hand = []
        self.count = 0

    def __repr__(self):
        return "player's hand is: " + str(self.hand) + " with count: " + str(self.count)

###GLOBAL FUNCTIONS############################################


def initialize_deck():
    main_deck = Deck()
    main_deck.fill_deck()
    return main_deck

def get_action():
    x = input("H for Hit and S for Stand \n").upper()
    while x!= "H" and x != "S":
        print("Invalid input")
        x = input("H for Hit and S for Stand \n").upper()
    return x

def get_play():
    x = input("Press S to Start or Q to Quit \n").upper()
    while x!= "S" and x != "Q":
        print("Invalid input")
        x = input("Press S to Start or Q to Quit \n").upper()
    return x

def get_bet(limit):
    x = input("Enter your bet for this hand \n")
    while True:
        try:
            while int(x) > limit or int(x) < 1:
                print("Invalid input: must be a positive number less than " + str(limit))
                x = input("Enter your bet for this hand \n")
            return int(x)
        except KeyboardInterrupt:
            return
        except:
            print("Invalid input: must be a positive number less than " + str(limit))
            x = input("Enter your bet for this hand \n")
        



#take in 2 arrays representing the 2 players hands and returns the winner of the 2
def compare_tie(hand1, hand2):
    #assert that both sum to 21
    #check rules, winner is the one with fewer cards?
    return False





###########################################

#INITIALIZE DECK - a game uses 1 - 8 decks per game
main_deck = initialize_deck()


#DEAL CARDS - dealers gives cards out left to right, then house's card face down, then everyone again and house face up
player1 = Player()
dealer = Player()

player1.add_card(main_deck.get_rand_card())
dealer.add_card(main_deck.get_rand_card())   #this one is face down
player1.add_card(main_deck.get_rand_card())
dealer.add_card(main_deck.get_rand_card())



#PLAY THE GAME
play = get_play()
while play == "S":
    print("You have " + str(player1.wallet) + " dollars in your wallet")
    if player1.wallet <= 0:
        print("Better luck next time!")
        quit()
    bet = get_bet(player1.wallet)
    while player1.count < 21:
        print("Your hand is " + str(player1.hand) + " that sums to " + str(player1.count))
        print("The dealer is showing " + str(dealer.hand[1]))

        action = get_action()

        if action == "H":
            print("You chose to Hit")
            c = main_deck.get_rand_card()
            player1.add_card(c)
            print("You were dealt " + str(c))
            
        else:
            print("You chose to Stand")
            break

    print("Your hand is " + str(player1.hand) + " that sums to " + str(player1.count))

    if (player1.count > 21):
        print("YOU BUST")
        player1.wallet -= bet
        #GAME OVER YOU LOSE
    elif player1.count == 21 and len(player1.hand) == 2:
        print("BLACKJACK!")
    elif player1.count == 21:
        print("YOU HAVE 21!")

    #now the dealer plays
    if player1.count <= 21:
        print("It is the dealer's turn")
        while dealer.count < 21:
            if dealer.count < 17:
                #hit
                print("The dealer hits")
                c = main_deck.get_rand_card()
                dealer.add_card(c)
                print("The dealer was dealt " + str(c))
                #print("The dealer has " + str(dealer.hand) + " that sums to " + str(dealer.count))
            else:
                print("The dealer stands at " + str(dealer.count))
                break

        print("The dealer has " + str(dealer.hand) + " that sums to " + str(dealer.count))

        if (dealer.count == 21 and len(dealer.hand)==2) and (player1.count == 21 and len(player1.hand)==2):
            #push
            print("push")
            print("THE DEALER ALSO HAS BLACKJACK - PUSH")
        elif (player1.count == 21 and len(player1.hand)==2):
            #player wins
            print("YOU WIN!")
            player1.wallet += bet
        elif (dealer.count == 21 and len(dealer.hand)==2):
            #dealer wins
            print("THE DEALER HAS BLACKJACK")
            print("YOU LOSE")
            player1.wallet -= bet
        elif dealer.count > 21:
            print("YOU WIN - DEALER BUSTS")
            player1.wallet += bet
        elif player1.count > dealer.count and player1.count <= 21:
            print("YOU WIN")
            player1.wallet += bet
        elif dealer.count > player1.count and dealer.count <= 21:
            print("DEALER WINS")
            player1.wallet -= bet
        else:
            #push
            print("PUSH")
        


    print("You now have " + str(player1.wallet) + " dollars")
    play = get_play()
    if play == "S":
        player1.clear_hand()
        dealer.clear_hand()
        player1.add_card(main_deck.get_rand_card())
        dealer.add_card(main_deck.get_rand_card())   #this one is face down
        player1.add_card(main_deck.get_rand_card())
        dealer.add_card(main_deck.get_rand_card())

 
    