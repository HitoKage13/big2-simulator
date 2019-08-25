# Started by Jeremy Lim on 13/08/2019

# TO-DO LIST
# - Implement states (most done)
# - Check legal players
# - If passing, will not go back to the player
# - Implement player prompts (most done)
# - Implement point system (most done)

import random

class Card():
    def __init__(self, suit, rank, suitValue, rankValue, totalValue):
        self._suit = suit
        self._rank = rank
        self._suitValue = suitValue
        self._rankValue = rankValue
        self._totalValue = totalValue

    @property
    def suit(self):
        return self._suit

    @property
    def rank(self):
        return self._rank

    @property
    def suitValue(self):
        return self._suitValue

    @property
    def rankValue(self):
        return self._rankValue

    @property
    def totalValue(self):
        return self._totalValue

    def __repr__(self):
       return self._suit + self._rank

class Condition():
    def __init__(self, state, lastCards):
        self._state = state
        self._lastCards = lastCards

    @property
    def state(self):
        return self._state

    @property
    def lastCards(self):
        return self._lastCards

    def set_state(self, state):
        self._state = state

    def set_lastCards(self, lastCards):
        self._lastCards = lastCards

P1 = []
P2 = []
P3 = []
P4 = []
deck = []

P1_Points = 0
P2_Points = 0
P3_Points = 0
P4_Points = 0

currentCondition = Condition(None, None)

# global 'D' ::= 1
# global 'C' ::= 2
# global 'H' ::= 3
# global 'S' ::= 4

# prints the selected player's hand
def printHand(player):
    print("PLAYER " + str(player) + ": " + str(returnPlayer(player)))

# initialises the game and
def initialise_game():
    rankList = ["3","4","5","6","7","8","9","10","J","Q","K","A","2"]
    suitList = ["D","C","H","S"]
    rankValue = 3
    suitValue = 1
    totalValue = 1
    counter = 0

    # sets up the deck
    for rank in rankList:
        suitValue = 1
        for suit in suitList:
            deck.append(Card(suit, rank, suitValue, rankValue, totalValue))
            suitValue += 1
            totalValue += 1
        rankValue += 1

    # debugging for values
    # for card in deck:
    #     print(str(card) + " " + str(card.suitValue) + " " + str(card.rankValue) + " " + str(card.totalValue))

    # randomly gives cards out
    random.shuffle(deck)
    for i in range(0, 13):
        P1.append(deck[counter])
        P2.append(deck[counter+1])
        P3.append(deck[counter+2])
        P4.append(deck[counter+3])
        counter += 4

# provides a prompt for the current player to play cards
def prompt(state, lastCards, player):
    printHand(player)
    if (state == None and lastCards == None):
        state = str(input("What state do you want to play? "))
        currentCondition.set_state(state)
        # WIP for checking state legality
    else:
        print("Current: " + str(state))
        print("Last card: " + str(lastCards))

    print("What action are you doing? Enter `play`, `pass`, `legal`")
    action = input()
    action = action.lower()
    if (action == "play"):
        print("What card are you playing? Enter in [SUIT] [RANK] or `pass` to skip your turn")
    elif (action == "pass"):
        return
    elif (action == "legal"):
        # legalPlays()
        pass

    card1 = input()
    if (state == '1'):
        playedCards = [returnCard(card1, deck)]
    elif (state == '2'):
        card2 = input()
        playedCards = [returnCard(card1, deck), returnCard(card2, deck)]
    elif (state == '3'):
        card2 = input()
        card3 = input()
        playedCards = [returnCard(card1, deck), returnCard(card2, deck), returnCard(card3, deck)]
    elif (state == '5'):
        card2 = input()
        card3 = input()
        card4 = input()
        card5 = input()
        playedCards = [returnCard(card1, deck), returnCard(card2, deck), returnCard(card3, deck), returnCard(card4, deck), returnCard(card5, deck)]
    else:
        pass

    if (checkLegal(state, lastCards, playedCards)):

        # checks if the cards played are in hand
        for card in playedCards:
            if (returnCard(card, returnPlayer(player)) == None):
                print("REKT")

        # plays the cards
        for card in playedCards:
            playCard(card, returnPlayer(player))

        # sets the cards played for next round
        currentCondition.set_lastCards(playedCards)

# returns the selected player's hand
def returnPlayer(player):
    if (player == 1):
        return P1
    elif (player == 2):
        return P2
    elif (player == 3):
        return P3
    elif (player == 4):
        return P4

# returns the selected card as an object
def returnCard(target, deck):
    searched = list(filter(lambda card: str(card) == target, deck))
    if (len(searched) > 0):
        return searched[0]
    else:
        return None

# plays a card from a hand and returns success/error
def playCard(card, hand):
    if card in hand:
        hand.remove(card)
        return "SUCCESS"
    else:
        return "ERROR"

# WIP
def legalPlays():
    return legalList

# checks if the cards played are legal
def checkLegal(state, lastCards, playedCards):
    # checks if cards inputted are legal to be played
    if (len(playedCards) == 2 or len(playedCards) == 3):
        rankCheck = playedCards[0].rankValue
        for card in playedCards:
            if (card.rankValue != rankCheck):
                return False

    # checks if there are previous cards played
    if (lastCards == None):
        return True

    # checks if it beats the previous cards
    if (state == '1'):
        if playedCards[0].totalValue > lastCards[0].totalValue:
            return True
    elif (state == '2' or state == '3'):
        if playedCards[0].rankValue > lastCards[0].rankValue:
            return True
        elif playedCards[0].rankValue == lastCards[0].rankValue:
            # WIP
            pass
    elif (state == '5'):
        # WIP
        pass

    return False

# checks if the game is finished
def checkFinish():
    if (len(P1) == 0):
        return 1
    elif (len(P2) == 0):
        return 2
    elif (len(P3) == 0):
        return 3
    elif (len(P4) == 0):
        return 4
    else:
        return 0

# calculates points after each game for each player
def calcPoints(player):
    if (len(player) < 7):
        return len(player)
    elif (len(player) >= 7 and len(player) < 10):
        return 2*len(player)
    elif (len(player) >= 10 and len(player) < 13):
        return 3*len(player)
    elif (len(player) == 13):
        return 4*len(player)

# initialises, runs and finishes the game
def game():
    initialise_game()
    while (checkFinish() == 0):
        prompt(currentCondition.state, currentCondition.lastCards, 1)
        if (checkFinish() > 0):
            break
        prompt(currentCondition.state, currentCondition.lastCards, 2)
        if (checkFinish() > 0):
            break
        prompt(currentCondition.state, currentCondition.lastCards, 3)
        if (checkFinish() > 0):
            break
        prompt(currentCondition.state, currentCondition.lastCards, 4)

    P1_Points = calcPoints(returnPlayer(1))
    P2_Points = calcPoints(returnPlayer(2))
    P3_Points = calcPoints(returnPlayer(3))
    P4_Points = calcPoints(returnPlayer(4))

game()
