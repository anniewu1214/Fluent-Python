import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])


class FrenchDeck:
    """
    Test of sequence properties:

        >>> beer_card = Card('7', 'diamonds')
        >>> beer_card
        Card(rank='7', suit='diamonds')
        >>> deck = FrenchDeck()
        >>> len(deck)
        52
        >>> deck[0]
        Card(rank='2', suit='spades')
        >>> deck[-1]
        Card(rank='A', suit='hearts')
        >>> from random import choice
        >>> choice(deck)  # doctest: +ELLIPSIS
        Card(rank=..., suit=...)
        >>> deck[:3]  # doctest: +NORMALIZE_WHITESPACE
        [Card(rank='2', suit='spades'), Card(rank='3', suit='spades'),
        Card(rank='4', suit='spades')]
        >>> deck[12::13]  # doctest: +NORMALIZE_WHITESPACE
        [Card(rank='A', suit='spades'), Card(rank='A', suit='diamonds'),
        Card(rank='A', suit='clubs'), Card(rank='A', suit='hearts')]
        >>> for card in deck:  # doctest: +ELLIPSIS
        ...     print(card)
        Card(rank='2', suit='spades')
        Card(rank='3', suit='spades')
        ...
        >>> for card in reversed(deck):  # doctest: +ELLIPSIS
        ...     print(card)
        Card(rank='A', suit='hearts')
        Card(rank='K', suit='hearts')
        ...
        >>> Card('Q', 'hearts') in deck
        True
        >>> Card('7', 'beasts') in deck
        False
        >>> suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)
        >>> def spades_high(card):
        ...     rank_value = FrenchDeck.ranks.index(card.rank)
        ...     return rank_value * len(suit_values) + suit_values[card.suit]
        >>> for card in sorted(deck, key=spades_high):  # doctest: +ELLIPSIS
        ...     print(card)
        Card(rank='2', suit='clubs')
        Card(rank='2', suit='diamonds')
        ...

    Test of monkey patching:
    - def: change a class or module at runtime, without touching the source code
    - the code is often tightly coupled with the program, often handling private
      and undocumented parts
    - use monkey patching to make it mutable and compatible with random.shuffle

        >>> def set_card(deck, position, card):
        ...     deck._cards[position] = card
        ...
        >>> FrenchDeck.__setitem__ = set_card
        >>> from random import shuffle
        >>> shuffle(deck)
        >>> deck[:5]  # doctest: +ELLIPSIS
        [Card(rank=...
    """
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        """Line breaks are ignored inside pairs of [], {}, or (). so you can build
        multiline lists, listcomps, genexprs, dicts without using \ line continuation escape"""
        self._cards = [Card(rank, suit) for suit in self.suits
                       for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]


class FrenchDeck2(collections.MutableSequence):
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                       for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __setitem__(self, index, value):
        # required, enables shuffling
        self._cards[index] = value

    def insert(self, index, value):
        # required
        self._cards.insert(index, value)

    def __delitem__(self, index):
        # subclassing MutableSequence forces us to implement __delitem__
        del self._cards[index]

    def __getitem__(self, index):
        return self._cards[index]
