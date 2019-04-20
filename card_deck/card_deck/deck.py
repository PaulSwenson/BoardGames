#!/usr/bin/env python

""" standard_card_game.py
Framework for a deck to simulate card games with a standard deck.
"""

# standard includes
import random
import types


# TODO: move these variables to a types.SimpleNamespace to ensure they are private
# variables for local use
suits = ['heart', 'spade', 'club', 'diamond']
suit_value_dict = {'heart'  : 3,
                   'diamond': 2,
                   'spade'  : 1,
                   'club'   : 0}


# TODO: move the error classes to a different file.
class CardError(Exception):
    """ CardError
    Parent class for card errors
    """
    pass


class CardValueError(CardError):
   """ CardValueError
   Exception for card values not in valid range
   """
   pass


class CardSuitError(CardError):
   """ CardSuitError
   Exception for card suits not in valid range
   """
   pass


class DeckError(Exception):
    """ DeckError
    Parent class for deck errors
    """
    pass


class DeckOutOfCardsError(DeckError):
    """ DeckOutOfCardsError
    The deck does not contain any more cards
    """
    pass


class Card:
    """ Card
    Class for cards in a standard deck
    """

    def __init__(self, value, suit):
        """ Constructor
        Purpose:
            Creates a card with specified numeric value (usually 1-14)
            and suit if not joker.
        Parameters:
            value   - the value of the card
            suit    - the suit of the card
        """
        if value not in suits:
            raise CardValueError

        if suit not in suits:
            raise CardSuitError

        self.value = value
        self.suit = suit

    def compare(self, card):
        """ Compare
        Purpose:
            Compares the value and suit of this card with another card
        Parameters:
            card    - the card we are comparing this card to
        Returns:
            -1  - if this card is lower than the parameter card
             0  - if this card is identical to the parameter card
             1  - if this card is a higher value than the parameter card
        """
        if self.value == card.value:
            return self.suitCompare(card)

        elif self.value > card.value:
            return 1

        elif self.value < card.value:
            return -1

    def suitCompare(self, card):
        """ suitCompare
        Purpose:
            Compares the suits of two cards.
        Parameters:
            card    - the card we are comparing this card to
        Returns:
            -1  - if this card's suit is lower than the parameter card's suit
             0  - if this card's suit is identical to the parameter card's suit
             1  - if this card's suit is a higher value than the parameter card's suit
        """
        if suit_value_dict[self.suit] == suit_value_dict[card.suit]:
            return 0

        elif suit_value_dict[self.suit] > suit_value_dict[card.suit]:
            return 1

        elif suit_value_dict[self.suit] < suit_value_dict[card.suit]:
            return -1


class Deck:
    """ Deck
    Deck of cards for a standard deck
    """
    def __init__(self, number_of_decks=1, using_jokers=False):
        """ constructor
        Purpose:
            Builds a deck of cards based on a standard card deck
        Parameters:
            number_of_decks - the number of decks to use
            using_jokers    - set to True to add jokers to the deck
        Returns:
            returns an array of cards in sorted order
        """
        self.deck = []
        self.discard = []
        suits = ['heart', 'spade', 'club', 'diamond']
        card_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

        for deck_count in range(number_of_decks):
            for suit in suits:
                for card_value in card_values:
                    self.deck.append(Card(card_value, suit))
            if using_jokers:
                self.deck.append(Card(14), Card(14))

    def shuffle(self):
        """ shuffle
        Purpose:
            Adds the discard pile back into the deck and shuffles it.
        Parameters:
            N/A
        Returns:
            N/A
        Notes:
            Deck and discard modified in place.
        """
        self.deck += self.discard
        self.discard = []
        random.shuffle(self.deck)

    def draw(self):
        """ draw
        Purpose:
            Draw one card from the deck
        Parameters:
            N/A
        Returns:
            Returns a card drawn from the top of the deck
        Exceptions:
            DeckOutOfCardsError - if the deck's draw pile is empty
        Notes:
            Deck will be modified
        """
        try:
            card_drawn = self.deck.pop(0)
        except IndexError:
            raise DeckOutOfCardsError

        return card_drawn

    def addToDiscard(self, card):
        """ addToDiscard
        Purpose:
            Places a card into the deck's discard pile
        Parameters:
            card    - the card being placed in the discard pile
        Returns:
            N/A
        Notes:
            Discard list will be modified
        """
        self.discard.append(card)


class Hand:
    """ Hand
    Used to represent the cards held by a player
    """

    def __init__(self):
        """ constructor
        Purpose:
            Creates a hand to represent a player's cards
        Parameters:
            N/A
        Returns:
            returns a hand object
        """
        self.hand = []

    def draw(self, deck):
        """ draw
        Purpose:
            Draws a card from the deck
        Parameters:
            deck - the deck of cards that we are drawing from
        Returns:
            N/A
        Notes:
            The player's hand and the deck are modified
        """
        try:
            self.hand.append(deck.draw())
        except DeckOutOfCardsError:
            raise DeckOutOfCardsError

    def discard(self, deck, card_index):
        """ discard
        Purpose:
            Discards a card into the deck's discard pile
        Parameters:
            deck        - the deck we are discarding into
            card_index  - the index of the card we are discarding from our hand
        Returns:
            N/A
        Exceptions:
            IndexError  - if the card_index does not exist in our hand
        Notes:
            The deck's discard pile and hand are modified
        """
        try:
            deck.addToDiscard(self.hand.pop(card_index))
        except IndexError:
            raise IndexError

    # TODO: implement searchHandForCard

    # def searchHandForCard(self, card_to_find=None, card_value=None, card_suit=None):
    #     """ searchHandForCard
    #     Purpose:
    #         Searches this hand for a specific card or set of cards by value, suit, or both
    #     Parameters:
    #         card_to_find    - the card to search for
    #         card_value=None - the card value to search for
    #         card_suit=None  - the card suit to search for
    #     Returns:
    #         Returns a list of tuples containing the card and the index.
    #         i.e.
    #             [ (card1, index1), (card2, index2), ... , (cardN, indexN) ]
    #     Notes:
    #         -If the card is not found, this will return an empty list
    #     """
    #     card_value_match_list = []
    #     card_suit_match_list = []
    #     card_match_list = []
    #
    #     index = 0
    #     for card in self.hand:
    #         if card_to_find and card.compare(card_to_find) == 0:
    #             card_match_list.append((card, index))
    #
    #         if not card_to_find and card.value == card_value:
    #             card_value_match_list.append((card, index))
    #
    #         if not card_to_find and card.suit == card_suit:
    #             card_suit_match_list.append((card, index))
    #
    #         index += 1
    #
    #     # TODO: either create separate functions for searching for a card by value/suit
    #     #       or add additional logic here to handle those cases as well.
    #
    #     if not card_to_find:
    #         for card_value_tup in card_value_match_list:
    #             for card_suit_tup in card_suit_match_list:



# TODO: add regression/unit tests for all of these functions.
