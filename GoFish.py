
import random

class Card:
    def __init__(self, rank):
        self.rank = rank

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def draw_card(self, card):
        self.hand.append(card)

    def has_rank(self, rank):
        return any(card.rank == rank for card in self.hand)

    def remove_cards(self, rank):
        cards = [card for card in self.hand if card.rank == rank]
        self.hand = [card for card in self.hand if card.rank != rank]
        return cards

class Deck:
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self):
        self.cards = [Card(rank) for rank in self.ranks * 4]
        random.shuffle(self.cards)

    def deal_cards(self, num_players):
        num_cards = 7 if num_players == 2 else 5
        hands = [[] for _ in range(num_players)]
        for _ in range(num_cards):
            for i in range(num_players):
                hands[i].append(self.cards.pop(0))
        return hands

class GoFishGame:
    def __init__(self, num_players):
        self.num_players = num_players
        self.deck = Deck()
        self.players = [Player(f'Player {i+1}') for i in range(num_players)]
        self.current_player = 0

    def select_opponent(self):
        print("Select an opponent to ask for cards:")
        for i, player in enumerate(self.players):
            if i != self.current_player:
                print(f"{i+1}. {player.name}")
        choice = input().strip()
        while True:
            if choice.isdigit():
                choice = int(choice) - 1
                if choice != self.current_player and choice >= 0 and choice < len(self.players):
                    return choice
            elif choice.startswith("Player ") and choice[7:].isdigit():
                num = int(choice[7:]) - 1
                if num != self.current_player and num >= 0 and num < len(self.players):
                    return num
            print("Invalid choice. Select a valid opponent:")
            choice = input().strip()

    def play(self):
        hands = self.deck.deal_cards(self.num_players)

        # Distribute cards to players
        for i in range(self.num_players):
            self.players[i].hand = hands[i]

        print("Welcome Player 1!")  # Print welcome message for Player 1

        # Main game loop
        while True:
            # Only reveal Player 1's hand
            if self.current_player == 0:
                print(f"\nYour hand:")
                self.display_hand(self.players[self.current_player].hand)
            else:
                print("\nYour hand: (Not visible)")
                
            print(f"\n{self.players[self.current_player].name}'s turn:")
            
            # Ask opponent for a rank
            opponent_index = self.select_opponent()
            opponent = self.players[opponent_index]
            rank = input("Ask an opponent for a rank (2-10, J, Q, K, A): ").upper()
            while rank not in Deck.ranks:
                rank = input("Invalid input. Ask for a rank (2-10, J, Q, K, A): ").upper()

            if opponent.has_rank(rank):
                print(f"{opponent.name} has {rank}s!")
                cards_given = opponent.remove_cards(rank)
                self.players[self.current_player].hand.extend(cards_given)
                if self.check_for_books(self.players[self.current_player], rank):
                    self.display_books(self.players[self.current_player], rank)
            else:
                print(f"{opponent.name} says 'Go Fish!'")
                if len(self.deck.cards) > 0:
                    drawn_card = self.deck.cards.pop(0)
                    print(f"You drew a {drawn_card.rank}")
                    self.players[self.current_player].draw_card(drawn_card)
                    if self.check_for_books(self.players[self.current_player], drawn_card.rank):
                        self.display_books(self.players[self.current_player], drawn_card.rank)
                else:
                    print("The stock is empty. No cards to draw.")

            # Check if the game is over
            if self.is_game_over():
                self.display_winner()
                break

            # Switch to the next player
            self.current_player = (self.current_player + 1) % self.num_players

    def display_hand(self, hand):
        for card in hand:
            print(card.rank, end=' ')
        print()

    def check_for_books(self, player, rank):
        count = sum(1 for card in player.hand if card.rank == rank)
        if count == 4:
            return True
        return False

    def display_books(self, player, rank):
        print(f"{player.name} completed a book of {rank}s!")

    def is_game_over(self):
        for player in self.players:
            if len(player.hand) == 0:
                return True
        return False

    def display_winner(self):
        max_books = 0
        winner = None
        for player in self.players:
            books = sum(1 for rank in Deck.ranks if self.check_for_books(player, rank))
            if books > max_books:
                max_books = books
                winner = player
        print(f"\n{winner.name} wins with {max_books} books!")

if __name__ == "__main__":
    num_players = int(input("Enter the number of players (2-4): "))
    while num_players < 2 or num_players > 4:
        num_players = int(input("Invalid number of players. Enter 2-4: "))
    
    game = GoFishGame(num_players)
    game.play()
