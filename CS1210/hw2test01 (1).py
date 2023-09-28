# CS1210: HW2
######################################################################
# Complete the signed() function, certifying that:
#  1) the code below is entirely your own work, and
#  2) it has not been shared with anyone outside the intructional team.
#
def signed():
    return(["cjtams"])

######################################################################
# Import randint and shuffle from random module.
from random import randint, shuffle

######################################################################
# createDeck() produces a new, cannonically ordered, 52 card deck
# using a nested comprehension. Providing a value less than 13
# produces a smaller deck, like the semi-standard 40 card 4 suit 1-10
# deck used in many older card games (including tarot cards). Here,
# we'll use it with default values.
#
def createDeck(N=13, S=('spades', 'hearts', 'clubs', 'diamonds')):
    return([ (v, s) for s in S for v in range(1, N+1) ])

######################################################################
# Construct the representation of a given card using special unicode
# characters for hearts, diamonds, clubs, and spades. The input is a
# legal card, c, which is a (v, s) tuple. The output is a 2 or
# 3-character string 'vs' or 'vvs', where 's' here is the unicode
# character corresponding to the four standard suites (spades, hearts,
# diamonds or clubs -- provided), and v is a 1 or 2 digit string
# corresponding to the integers 2-10 and the special symbols 'A', 'K',
# 'Q', and 'J'.
#
# Example:
#    >>> displayCard((1, 'spades'))
#    'A♠'
#    >>> displayCard((12, 'hearts'))
#    'Q♡'
#
'''
Full points
'''
def displayCard(c):
    suits = {'spades':'\u2660', 'hearts':'\u2661', 'diamonds':'\u2662', 'clubs':'\u2663'}
    value = {1:'A',2:2,3:3,4:4,5:5,6:6,7:7,8:8,9:9,10:10,11:'J',12:'Q',13:'K'}
    return ( '{}{}'.format(value[c[0]],suits[c[1]]) )

######################################################################
# Print out an indexed representation of the state of the table:
# foundation piles are numbered 0-3, corner piles 4-7.
#
# Example:
#   >>> showTable(F, C)
#     F0: 9♡...9♡
#     F1: 2♢...2♢
#     F2: 7♡...7♡
#     F3: 8♡...8♡
#     C4:
#     C5:
#     C6:
#     C7:
# Or, mid-game:
#     F0: 8♣...A♢
#     F1: J♣...J♣
#     F2: A♠...A♠
#     F3:
#     C4: K♡...K♡
#     C5:
#     C6:
#     C7:
#
'''
Full points
'''
def showTable(F, C):
    decklistF=['F0','F1','F2','F3']
    decklistC=['C4','C5','C6','C7']
    for i in range(8):
        if i<4:
            if len(F[i])>0:
                print('{}: {}...{}'.format(decklistF[i],displayCard(F[i][0]),displayCard(F[i][len(F[i])-1])))
            else:
                print('{}:'.format(decklistF[i]))
        else:
            if len(C[i-4])>0:
                print('{}: {}...{}'.format(decklistC[i-4],displayCard(C[i-4][0]),displayCard(C[i-4][len(C[i-4])-1])))
            else:
                print('{}:'.format(decklistC[i-4]))

######################################################################
# Print out an indexed list of the cards in input list H, representing
# a hand. Entries are numbered starting at 8 (indexes 0-3 are reserved
# for foundation piles, and 4-7 are reserved for corners). The
# indexing is used to select cards for play.
#
# Example:
#   >>> showHand(H[0])
#   Hand: 8:A♢ 9:4♢ 10:3♡ 11:5♠ 12:6♠ 13:7♠ 14:8♠
#   >>> showHand(H[1])
#   Hand: 8:9♣ 9:5♢ 10:8♢ 11:9♢ 12:10♡ 13:A♠ 14:4♠
#
'''
Full points
'''
def showHand(H):
    print( 'Hand: '+' '.join(['{}:{}'.format(i+8,displayCard(H[i])) for i in range(len(H))]) )

######################################################################
# We'll use deal(N, D) to set up the game. Given a deck (presumably
# produced by createDeck()), shuffle it, then deal 7 cards to each of
# N players, and seed the foundation piles with 4 additional cards.
# Returns D, H, F, where D is what remains of the deck, H is a list of
# N 7-card "hands", and F is a list of lists corresponding to the four
# "seeded" foundation piles.
#
# Example:
#   >>> D, H, F = deal(2, D)
#   >>> len(D)
#   34
#   >>> len(H)
#   2
#   >>> H[0][:3]
#   [(5, 'clubs'), (12, 'clubs'), (3, 'diamonds')]
#   >>> F[2]
#   [(11, 'hearts')]
#
'''
Full points
'''
def deal(N, D):
    shuffle(D)
    #i have to use a list comprehension for some reason or
    #H just makes a list of N identical lists
    H=[[] for x in range(N)] #nested list of correct size
    F=[[],[],[],[]]
    for i in range(N*7):
        H[i%N].append(D.pop())
    F[0].append(D.pop())
    F[1].append(D.pop())
    F[2].append(D.pop())
    F[3].append(D.pop())
    return ( D,H,F )




######################################################################
# Returns True if card c can be appended to stack S. To be legal, c
# must be one less in value than S[-1], and should be of the "other"
# color (red vs black).
#
# Hint: Remember, S might be empty, in which case the answer should
# not be True.
#
# Hint: Use the encapsulated altcolor(c1, c2) helper function to check
# for alternating colors.
#
# Example:
#   >>> legal([(2, 'diamonds')], (1, 'spades'))
#   True
#   >>> legal([(2, 'diamonds')], (1, 'hearts'))
#   False
#
'''
Full points
'''
def legal(S, c):
    def altcolor(c1, c2):
        if (c1[1]=='diamonds' or c1[1]=='hearts') and (c2[1]=='spades' or c2[1]=='clubs'):
            return True
        elif (c1[1]=='spades' or c1[1]=='clubs') and (c2[1]=='diamonds' or c2[1]=='hearts'):
            return True
        else:
            return False
    if S!=[] and altcolor(S[len(S)-1],c) and (S[len(S)-1][0]-1==c[0]):
        return True
    else:
        return False


######################################################################
# Governs game play for N players (2 by default). This function sets
# up the game variables, D, H, F and C, then chooses the first player
# randomly from the N players. By convention, player 0 is the user,
# while all other player numbers are played by the auto player.
#
# Each turn, the current player draws a card from the deck D, if any
# remain, and then is free to make as many moves as he/she chooses.
#
# Hint: fill out the remainder of the function, replacing the pass
# statements and respecting the comments.
#
'''
Full points
'''
def play(N=2):
    # Set up the game.
    D, H, F = deal(N, createDeck())
    C = [ [] for i in range(4) ]   # Corners, initially empty.

    # Randomly choose a player to start the game.
    player=randint(0,N-1)
    print('Player {} moves first.'.format(player))

    # Start the play loop; we'll need to exit explicitly when
    # termination conditions are realized.
    while True:
        # Draw a card if there are any left in the deck.
        if len(D)>0:
            H[player].append(D.pop())
        print('\n\nPlayer {} ({} cards) to move.'.format(player, len(H[player])))
        print('Deck has {} cards left.'.format(len(D)))

        # Now show the table.
        showTable(F, C)

        # Let the current player have a go.
        if player != 0:
            automove(F, C, H[player])
        else:
            usermove(F, C, H[player])

        # Check to see if player is out; if so, end the game.
        if H[player] == []:
            print('\n\nPlayer {} wins!'.format(player))
            showTable(F, C)
            break

        # Otherwise, go on to next player.
        else:
            player = (player+1)%N

######################################################################
# Prompts a user to play their hand.  See transcript for sample
# operation.
#
##########
# I'm not sure what you want to be an Illegal versus Ill-formed
# the valid function I'm assuming has something to do with that
# but I'm not sure what is the use the user feedback is limited already and
# knowing that letters aren't part of the src dst input is still confusing
# I had a few of my friends from highschool try this and it's not exactly
# obvious how the game works. In short, is the Illegal Move feedback supposed
# to be the only one for numeric inputs in the form of src dst?
# if so I'm not sure why the valid function needs to exist
# it's not useful in the moving of cards aroud because you need a way to know
# which pile you are altering and the valid will just be an extra step after
# checking what piles the user is attempting to move to

'''
Full points
'''
def usermove(F, C, hand):
    # valid() is an internal helper function that checks if the index
    # i indicates a valid F, C or hand index.  To be valid, it cannot
    # be an empty pile or an out-of-range hand index. Remember, 0-3
    # are foundation piles, 4-7 are corner piles, and 8 and up index
    # into the hand.
    def valid(i):
        if i in (0,1,2,3) and len(F[i])>0:
            return True
        if i in (4,5,6,7) and len(C[i-4])>0:
            return True
        if i in range(7,7+len(hand)):
            return True
        return False

    # Ensure the hand is sorted, integrating newly drawn card.
    hand.sort()

    # Give some instruction.
    print('Enter your move as "src dst": press "/" to refresh display; "." when done')

    # Manage any number of moves.
    while True:           # Until the user quits with a .
        # Display current hand.
        # not here or else it inly displays only at the beginning of a turn

        # Read inputs and construct a tuple.
        move = []
        while not move or not valid(move[0]) or not valid(move[1]):
            showHand(hand) #this is better in the loop
            move = input("Your move? ").split()
            if len(move) == 1:
                if move[0] == '.':
                    return
                elif move[0] == '/':
                    showTable(F,C)
                    continue

            try:
                move = [int(move[0]), int(move[1])]
                # Execute the command, which looks like [from, to].
                # Remember, 0-3 are foundations, 4-7 are corners, 8+
                # are from your hand.
                #
                # What follows here is an if/elif/else statement for
                # each of the following cases.
                # Playing a card from your hand to a foundation pile.
                if move[0] in range(8,len(hand)+8) and move[1] in range(0,4) and (legal(F[move[1]],hand[move[0]-8]) or F[move[1]]==[]):
                    F[move[1]].append(hand[move[0]-8])
                    print('Moving {} to F{}.'.format(displayCard(hand[move[0]-8]),move[1]))
                    hand[move[0]-8:move[0]-7]=[]

                # Moving a foundation pile to a foundation pile.
                elif move[0] in range(0,4) and move[1] in range(0,4) and F[move[0]]!=[] and legal(F[move[1]],F[move[0]][0]):
                    F[move[1]].extend(F[move[0]])
                    print('Moving F{} to F{}.'.format(move[0],move[1]))
                    F[move[0]].clear()

                # Playing a card from your hand to a corner pile (K only to empty pile).
                elif move[1] in range(4,8) and move[0] in range(8,len(hand)+8) and (C[move[1]-4]==[] and hand[move[0]-8][0]==13 or legal(C[move[1]-4],hand[move[0]-8])):
                    C[move[1]-4].append(hand[move[0]-8])
                    print('Moving {} to C{}.'.format(displayCard(hand[move[0]-8]),move[1]))
                    hand[move[0]-8:move[0]-7]=[]

                # Moving a foundation pile to a corner pile.; one for general case and one for king in foundation pile because rule change
                elif ( move[0] in range(0,4) and move[1] in range(4,8) and ((C[move[1]-4]==[] and F[move[0]][0][0]==13) or legal(C[move[1]-4],F[move[0]][0]))):
                    C[move[1]-4].extend(F[move[0]])
                    print('Moving F{} to C{}.'.format(move[0],move[1]))
                    F[move[0]].clear()


                # Otherwise, print "Illegal move" warning.
                else:
                    print("Illegal move")

            except:
                # Any failure to process ends up here.
                print('Ill-formed move {}'.format(move))

            # If the hand is empty, return. Otherwise, reset move and
            # keep trying.
            if not hand:
                return
            move = []

######################################################################
# Plays a hand automatically using a fixed but not particularly
# brilliant strategy. The strategy involves consolidating the table
# (to collapse foundation and corner piles), then scanning cards in
# your hand from highest to lowest, trying to place each card. The
# process is repeated until no card can be placed. See transcript for
# an example.
#
'''
Full points
'''
def automove(F, C, hand):
    # Keep playing cards while you're able to move something.
    moved = True
    while moved:
        moved = False	# Change back to True if you move a card.

        # Start by consolidating the table.
        consolidate(F, C)

        # Sort the hand (destructively) so that you consider highest
        # value cards first.
        hand.sort()

        # Scan cards in hand from high to low value, which makes removing
        # elements easier.
        for i in range(len(hand)-1, -1, -1):
            # If current card is a king, place in an empty corner
            # location (guaranteed to be one).

            if hand[i][0]==13:
                k=C.index(list())
                C[k].append(hand[i])
                print('Moving {} to open corner C{}.'.format(displayCard(hand[i]),k+4))
                hand[i:i+1]=[]
                moved=True

            # Otherwise, try to place current card on an existing
            # corner or foundation pile.
            for j in range(4):
                # Here, you have an if/elif/else that checks each of
                # the stated conditions.
                if not hand or i>len(hand)-1:
                    continue

                # Place current card on corner pile.
                if legal(C[j],hand[i]):
                    C[j].append(hand[i])
                    print('Moving {} to C{}.'.format(displayCard(hand[i]),j+4))
                    hand[i:i+1]=[]
                    moved=True

                # Place current card on foundation pile.
                elif legal(F[j],hand[i]):
                    F[j].append(hand[i])
                    print('Moving {} to F{}.'.format(displayCard(hand[i]),j))
                    hand[i:i+1]=[]
                    moved=True

                # Start a new foundation pile.
                elif F[j]==[]:
                    F[j].append(hand[i])
                    print('Moving {} to open foundation F{}.'.format(displayCard(hand[i]),j))
                    hand[i:i+1]=[]
                    moved=True

######################################################################
# consolidate(F, C) looks for opportunities to consolidate by moving a
# foundation pile to a corner pile or onto another foundation pile. It
# is used by the auto player to consolidate elements on the table to
# make it more playable.
#
# Example:
#   >>> showTable(F, C)
#     F0: 6♢...6♢
#     F1: 10♣...10♣
#     F2: J♡...J♡
#     F3: Q♠...Q♠
#     C4: K♢...K♢
#     C5:
#     C6:
#     C7:
#   >>> consolidate(F, C)
#   >>> showTable(F, C)
#     F0: 6♢...6♢
#     F1:
#     F2:
#     F3:
#     C4: K♢...10♣
#     C5:
#     C6:
#     C7:
#
'''
Full points
'''
def consolidate(F, C):
    # Consider moving one foundation onto another.
    for i in range(4):
        for j in range(4):
            if F[j]!=[] and legal(F[i],F[j][0]):
                F[i].extend(F[j])
                print('Moving F{} to F{}.'.format(j,i))
                F[j][0:]=[]
    # Consider moving a foundation onto a corner.
    for i in range(4):
        for j in range(4):
            if F[j]!=[] and legal(C[i],F[j][0]):
                C[i].extend(F[j])
                print('Moving F{} to C{}.'.format(j,i))
                F[j][0:]=[]
            elif F[j]!=[] and C[i]==[] and F[j][0][0]==13:
                C[i].extend(F[j])
                print('Moving F{} to C{}.'.format(j,i))
                F[j][0:]=[]


'''
Style

Full points


'''
######################################################################

######################################################################
# AutoGrader Feedback
######################################################################
######################################################################
### Your final score will be posted on ICON. Just FYI, the point	
### breakdown is:	
###    displayCard(): 2 points
###    showHand():    2 points
###    showTable():   3 points
###    deal(): 	      5 points
###    legal():       3 points
###    play(): 	      4 points
###    usermove():    5 points
###    automove():    6 points
###    consolidate(): 4 points
###    style/comments 6 points
### Total            40 points	
######################################################################
######################################################################
'''

**********************************************************************
File "../hw2test.py", line 21, in __main__
Failed example:
    student.showTable(F, C)
Expected:
      F0: 9♡...9♡
      F1: K♣...K♣
      F2: Q♣...Q♣
      F3: 5♡...5♡
      C4:
      C5:
      C6:
      C7:
Got:
    F0: 9♡...9♡
    F1: K♣...K♣
    F2: Q♣...Q♣
    F3: 5♡...5♡
    C4:
    C5:
    C6:
    C7:
**********************************************************************
File "../hw2test.py", line 31, in __main__
Failed example:
    student.showTable(F2, C2)
Expected:
      F0: J♢...J♢
      F1: 7♢...7♢
      F2: 10♠...10♠
      F3: 9♢...9♢
      C4:
      C5:
      C6:
      C7:
Got:
    F0: J♢...J♢
    F1: 7♢...7♢
    F2: 10♠...10♠
    F3: 9♢...9♢
    C4:
    C5:
    C6:
    C7:
**********************************************************************
1 items had failures:
   2 of  19 in __main__
***Test Failed*** 2 failures.
'''

### Hawkid: cjtams
### TestScore: 17
######################################################################
### This concludes the Autograder output. The TestScore shown above
### does not contribute to your final grade, rather only provides
### the TAs who are grading your code with some preliminary guidance.
######################################################################
