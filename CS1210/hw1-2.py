# CS1210: HW1
######################################################################
# Complete the signed() function, certifying that:
#  1) the code below is entirely your own work, and
#  2) it has not been shared with anyone outside the intructional team.
#
def signed():
    return(["cjtams"])

######################################################################
# In this homework, you will be implementing a spelling bee game,
# inspired by the that appears in the New York Times. The purpose of
# the game is to find as many possible words from a display of 7
# letters, where each word must meet the following criteria:
#   1. it must consist of four or more letters; and
#   2. it must contain the central letter of the display.
# So, for example, if the display looks like:
#    T Y
#   B I L
#    M A
# where I is the "central letter," the words "limit" and "tail" are
# legal, but "balmy," "bit," and "iltbma" are not.
#
# We'll approach the construction of our system is a step-by-step
# fashion; for this homework, I'll provide specs and function
# signatures to help you get started. If you stick to these specs and
# signatures, you should soon have a working system.
#
# First, we'll need a few functions from the random module. Read up on
# these at docs.python.org.
from random import choice, randint, sample

######################################################################
# fingerprint(W) takes a word, W, and returns a fingerprint of W
# consisting of an ordered set of the unique character constituents of
# the word. You have already encountered fingerprint(W) so I will
# provide the reference solution here for you to use elsewhere.
def fingerprint(W):
    return(''.join(sorted(set(W))))

######################################################################
# score(W) takes a word, W, and returns how many points the word is
# worth. The scoring rules here are straightforward:
#   1. four letter words are worth 1 point;
#   2. each additional letter adds 1 point up to a max of 9; and
#   3. pangrams (use all 7 letters in display) are worth 10 points.
# So, for example:
#      A L
#     O B Y
#      N E
#   >>> score('ball')
#   1
#   >>> score('balloon')
#   4
#   >>> score('baloney')
#   10     # Pangram!
#
'''
Full points
'''
def score(W):
    if len(set(W))==7 and len(W)>=7:
        return 10
    elif len(W)>12:
        return 9
    else:
        return len(W)-3

######################################################################
# jumble(S, i) takes a string, S, having exactly 7 characters and an
# integer index i where 0<=i<len(S). The string describes a puzzle,
# while i represents the index of S corresponding to the "central"
# character in the puzzle. This function doesn't return anything, but
# rather prints out a randomized representation of the puzzle, with
# S[i] at the center and the remaining characters randomly arrayed
# around S[i]. So, for example:
#    >>> jumble('abelnoy', 1)
#     A L
#    O B Y
#     N E
#    >>> jumble('abelnoy', 1)
#     N Y
#    L B A
#     E O
#
'''
Full points
'''
def jumble(S, i):
    L=sample(list(S[0:i])+list(S[i+1:]),6)
    print( ' '+L[0].upper()+' '+L[1].upper()+'\n'+L[2].upper()+' '+S[i].upper()+' '+L[3].upper()+'\n'+' '+L[4].upper()+' '+L[5].upper())

######################################################################
# readwords(filename) takes the name of a file containing a dictionary
# of English words and returns two values, a dictionary of legal words
# (those having 4 or more characters and fingerprints of 7 of fewer
# characters), with fingerprints as keys and values consisting of sets
# of words with that fingerprint, as well as a list, consisting of all
# of the unique keys of the dictionary having exactly 7 characters (in
# no particular order).
#
# Your function should provide some user feedback. So, for example:
#    >>> D,S=readwords('words.txt')
#    113809 words read: 82625 usable; 33830 unique fingerprints.
#    >>> len(S)
#    13333
#    >>> S[0]
#    'abemort'
#    >>> D[S[0]]
#    {'barometer', 'bromate'}
#
### finp(s)=fingerprint(s)
'''
Full points
'''
def readwords(filename):
    infile=open(filename)
    S=[]  ##initialize storage and counts
    D={}
    usable=0 #we will increment whenever a word is added to a set in D
    wordsread=0
    for line in infile:
        word=line.strip() # for cleanliness
        if len(word)>=4 and ( fingerprint(word) not in D ) and ( len(fingerprint(word))<=7 ): #for words with finps not in D
            D.update({fingerprint(word):{word}}) #add new key and value to the dictionary
            usable += 1
            if (len(fingerprint(word))==7): #build seed list
                S.append(fingerprint(word))
        elif len(word)>=4 and ( fingerprint(word) in D ) and ( len(fingerprint(word))<=7 ):#for words with finps in D already
            D[fingerprint(word)] = D[fingerprint(word)]|{word} #union of its corresponding set and new word
            usable += 1
        wordsread += 1 #increment for every line so it counts how many words were looked at
    print('{} words read: {} usable; {} unique fingerprints.'.format(wordsread, usable, len(D))) #user feedback
    infile.close() #clean up
    return (D,S)
######################################################################
# round(D, S) takes two arguments, corresponding to the values
# returned by readwords(), randomly selects a puzzle seed from the
# list S and a central letter from within S. It then shows the puzzle
# and enters a loop where the user can:
#    1. enter a new word for scoring;
#    2. enter / to rescramble and reprint the puzzle;
#    3. enter + for a new puzzle; or
#    4. enter . to end the game.
# When a word is entered, it is checked for length (must be longer
# than 4 characters and its fingerprint must be contained within the
# puzzle seed). The word is then checked against D, and if found, is
# scored and added to the list of words.
#
# Here is a sample interactive transcript of round() in action:
#    >>> D,S = readwords('words.txt')
#    >>> round(D,S)
#     E H
#    R P U
#     O S
#    Input words, or: '/'=scramble; ':'=show; '+'=new puzzle; '.'=quit
#    sb> pose
#    Bravo! +1
#    sb> repose
#    Bravo! +3
#    sb> house
#    Word must include 'p'
#    sb> :
#    2 words found so far:
#      pose
#      repose
#    sb> /
#     H R
#    O P E
#     S U
#    sb> prose
#    Bravo! +2
#    sb> +
#    You found 3 of 415 possible words: you scored 6 points.
#    True
#
### My plan going into theis is to intitialize the values that will change as the game progresses then enter a loop where the rest of the
### game occurs until the user enters '.' to quit
### I am not sure why the play() function has to "repeatedly" invoke rounds you can make the game work completely by just calling rounds
### because they are all print statements besides '.'. There is also no reason a new puzzle must return True I think, because
### without a while loop in play() the function does not need any boolean to regulate it which saves memory(In my interpretation of the intended spec). The play() function will hide
### rounds() and readwords() already and it gives you a new >>> command line when you quit with only the False return I have. I added the print of intructions for each new puzzle
### as well to match the original description in the HW 1 ICON page. play() will not repeatedly invoke rounds for these reasons.

'''
Full Points
'''
def rounds(D, S):
    scorenum=0
    wordlist=[] #for guessed words
    centerindex=randint(0,6) #stores center part of puzzle
    seednum=randint(0,len(S)-1) #stores puzzle seed
    jumble(S[seednum],centerindex) #first puzzle display
    print("Input words, or: '/'=scramble; ':'=show; '+'=new puzzle; '.'=quit")
    while True:
        ###can I change the input prompt
        ### the .lower() takes care of caps
        user=input("sb>").lower()
        #########################################################
        ### just 'rejumbles' the puzzle retaining the same center
        if user=='/':
            jumble(S[seednum],centerindex)
        #########################################################
        ### quit will return to stop eval
        ### in both rounds and when its called in play()
        ### print satement meant to match the original description in the HW 1 ICON page
        elif user=='.':
            print('You found {} of {} possible words: you scored {} points.'.format(len(wordlist),sum([ len(D[x]) for x in D if (set(x)<=set(S[seednum]) and S[seednum][centerindex] in x) ]),scorenum))
            return False
        #########################################################
        elif user==':':
            print('{} words found so far:\n  '.format(len(wordlist))+'\n  '.join(wordlist))
        #########################################################
        ### new puzzle: uses comprehesion to find possible words by check if the key fingerprint is part of the puzzle
        ### and if the center element is in the fingerprint(spaces are for reading). Then repeats steps for generating a new
        ### puzzle like at the beginning, so it will not a have a recursive call and reprint
        ### "Input words, or: '/'=scramble; ':'=show; '+'=new puzzle; '.'=quit"
        ### reset score
        elif user=='+':
            print('You found {} of {} possible words: you scored {} points.'.format(len(wordlist),sum([ len(D[x]) for x in D if (set(x)<=set(S[seednum]) and S[seednum][centerindex] in x) ]),scorenum))
            scorenum=0
            wordlist=[]
            centerindex=randint(0,6)
            seednum=randint(0,len(S)-1)
            jumble(S[seednum],centerindex)
            print("Input words, or: '/'=scramble; ':'=show; '+'=new puzzle; '.'=quit")
        ###############################################
        ### when the user doesn't enter a game modifier
        elif isinstance(user,str):
            ###check for len, center letter, existance (both users finp and user in the set that is paired with the finp in D)
            ### !!! make sure no repeats
            if S[seednum][centerindex] in user and set(S[seednum])>=set(user) and len(user)>=4 and ( fingerprint(user) in D ) and ( user in D[fingerprint(user)] ) and (user not in wordlist):
                scorenum += score(user)
                wordlist.append(user)
                print('Bravo! +{}'.format(score(user)))
            elif user in wordlist:
                print('You already entered that one.')# extra bit for user feddback
            elif S[seednum][centerindex] not in user and set(S[seednum])>=set(user) and len(user)>=4:
                ### I only wnat words that just dont have center letter to give this feedback
                ### not considering exsitance yet
                print("Word must include '{}'".format(S[seednum][centerindex]))
            elif len(user)<4 and set(S[seednum])>=set(user):
                ### here I just left it at len and whether or not it looks valid because if the word is less
                ### than four letters and has the right letters then I don't need to differentiate
                ### between "real" words
                print("Word must be four letters long.")
            else:
                print('Not a valid word.')# extra bit for user feddback

######################################################################
# play(filename='words.txt') takes a single optional argument filename
# (defaults to 'words.txt') that gives the name of the file containing
# the dictionary of legal words. After invoking readwords(), it
# repeatedly invokes rounds() until it obtains a False, indicating the
# game is over.
# sad
### see above rounds() signature for deviation from spec

'''
-1 fails to repeatedly call round() until returns False

NOTE: To your note about returning True/False seeming pointless, consider the following reference solution:

    D,S = readwords(filename)
    print("Welcome to Spelling Bee!")
    while round(D, S):
        pass

The benefit of this approach comes from simplifying the case where a new puzzle is requested: 

"+" would break the infinite loop of round by returning True. 
This breaks out of the round loop, but the loop in play will continue and start a new round, as the while condition is still true. 
This allows the first few lines of round to reset the game for you, instead of having to manually do it yourself

Regardless, I need to take away the point here since it did deviate from specs.
'''
def play(filename='words.txt'):
    print('Spell for your life :)')
    D,S=readwords(filename)
    rounds(D,S)


'''
STYLE AND FORMAT

Full points
'''

######################################################################
# AutoGrader Feedback
######################################################################
######################################################################
### Your final score will be posted on ICON. Just FYI, the point	
### breakdown is:	
###    score()      4 points	
###    jumble()     3 points	
###    readwords() 12 points	
###    round()     11 points	
###    play()       4 points	
###    style        6 points	
### Total          40 points	
######################################################################
######################################################################
# 76 words read: 74 usable; 12 unique fingerprints.
'''

**********************************************************************
File "../hw1test.py", line 28, in __main__
Failed example:
    score('cinnamiciac')
Expected:
    9
Got:
    8
**********************************************************************
1 items had failures:
   1 of  11 in __main__
***Test Failed*** 1 failures.
'''

### Hawkid: cjtams
### TestScore: 10
######################################################################
### This concludes the Autograder output. The TestScore shown above
### does not contribute to your final grade, rather only provides
### the TAs who are grading your code with some preliminary guidance.
######################################################################
