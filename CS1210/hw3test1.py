# CS1210: HW3 version 1
######################################################################
# Complete the signed() function, certifying that:
#  1) the code below is entirely your own work, and
#  2) it has not been shared with anyone outside the intructional team.
#
def signed():
    return(["hawkid"])

######################################################################
# In this homework, you will build the internals for Boggle, a popular
# word game played with 16 6-sided dice. At the same time, in class we
# will develop the interactive user interface for Boggle, so that your
# solution, augmented with what we do in class, will give you a
# playable Boggle game. This assignment will also give us a chance to
# work on a system using the object-oriented paradigm.
#
# This is version 1 of the template file, which does not include the
# user interface.  I will periodically release updated versions, which
# you can then merge into your own code: still, be sure to follow the
# instructions carefully, so as to ensure your code will work with the
# new template versions that contain the GUI we develop in class.
#
# The rules of Boggle are available online. Basically, you will roll
# the dice and arrange them into a 4x4 grid. The top faces of the die
# will display letters, and your job is to find words starting
# anywhere in the grid using only adjacent letters (where "adjacent"
# means vertically, horizontally, and diagonally adjacent). In our
# version of Boggle, there are no word length constraints beyond those
# implicitly contained in the master word list.
#
# Although other dice configurations are possible, the original Boggle
# dice are (in no particular order):
D = ["aaeegn","abbjoo","achops","affkps","aoottw","cimotu","deilrx","delrvy",
     "distty","eeghnw","eeinsu","ehrtvw","eiosst","elrtty","himnqu","hlnnrz"]

# You will need sample() from the random module to roll the die.
from random import sample

######################################################################
# Boggle is the base class for our system; it is analogous to the
# Othello class in our implementation of that game.  It contains all
# the important data elements for the current puzzle, including:
#    Boggle.board = the current puzzle board
#    Boggle.words = the master word list
#    Boggle.solns = the words found in the current puzzle board
#    Boggle.lpfxs = the legal prefixes found in the current puzzle board
# Additional data elements are used for the GUI and scoring, which
# will be added in subsequent versions of the template file.
#
# Note: we will opt to use Knuth's 5,757 element 5-letter word list
# ('words.dat') from the Wordnet puzzle, but the 113,809 element list
# of words from HW1 ('words.txt') should also work just as easily.
#
class Boggle ():
    # This is the class constructor. It should read in the specified
    # file containing the dictionary of legal words and then invoke
    # the play() method, which manages the game.
    def __init__(self, input='words.dat'):
        self.readwords(input)
        self.play()
        

    # Printed representation of the Boggle object is used to provide a
    # view of the board in a 4x4 row/column arrangement.
    def __repr__(self):
        return '\n'.join([' '.join([self.board[i][j].upper() for j in range(4)]) for i in range(4)])

    # The readwords() method opens the file specified by filename,
    # reads in the word list converting words to lower case and
    # stripping any excess whitespace, and stores them in the
    # Boggle.words list.
    def readwords(self, filename):
        infile=open(filename)
        self.words = []
        self.lpfxs = set()
        c=0
        for line in infile:
            s=line.lower().strip()
            self.words.append(s)
            self.lpfxs.update({s[:i] for i in range(len(line.lower().strip()))})
            c += 1
        print( 'Read {} words'.format(c) )
        infile.close()

    # The newgame() method creates a new Boggle puzzle by rolling the
    # dice and assorting them to the 4x4 game board. After the puzzle
    # is stashed in Boggle.board, the method also computes the set of
    # legal feasible word prefixes and stores this in Boggle.lpfxs.
    def newgame(self):
        L=sample(D,16)
        self.board = [[sample(L[j+i*4],1)[0] for j in range(4)] for i in range(4) ]
        
    # The solve() method constructs the list of words that are legally
    # embedded in the given Boggle puzzle. The general idea is search
    # recursively starting from each of the 16 puzzle positions,
    # accumulating solutions found into a list which is then stored on
    # Boggle.solns.
    #
    # The method makes use of two internal "helper" functions,
    # adjacencies() and extend(), which perform much of the work.
    def solve(self):
        self.solns = set()
        self.solnsdict = dict()
        # Helper function adjacencies() returns all legal adjacent
        # board locations for a given location loc. A board location
        # is considered legal and adjacent if (i) it meets board size
        # constraints (ii) is not contained in the path so far, and
        # (iii) is adjacent to the specified location loc.
        def adjacencies(loc, path):
            options=[]
            #for loop sequence ensures the possible options are all adjacent to loc
            for move in ((0,1),(0,-1),(1,1),(1,0),(1,-1),(-1,1),(-1,0),(-1,-1)):
                #check for coords outside board
                if ( move[0]+loc[0] not in range(0,4) or move[1]+loc[1] not in range(0,4) ):
                    continue
                #checks for repeat coords
                if  path!=[] and (move[0]+loc[0] in [path[i][0] for i in range(len(path))]) and (move[1]+loc[1] in [path[i][1] for i in range(len(path))]):
                    continue
                options.append(move)
            return options

        # Helper function extend() is a recursive function that takes
        # a location loc and a path traversed so far (exclusive of the
        # current location loc). Together, path and loc specify a word
        # or word prefix. If the word is in Boggle.words, add it to
        # Boggle.solns, because it can be constructed within the
        # current puzzle. Otherwise, if the curren prefix is still in
        # Boggle.lpfxs, attempt to extend the current path to all
        # adjacencies of location loc. To do this efficiently, a
        # particular path extension is abandoned if the current prefix
        # is no longer contained in self.lpfxs, because that means
        # there is no feasible solution to this puzzle reachable via
        # this extension to the current path/prefix.
        def extend(loc, path=[]):
            if self.extract(path+[loc]) in self.words:
                self.solns.update({self.extract(path+[loc])})
                if self.extract(path+[loc]) not in self.solnsdict:
                    self.solnsdict[self.extract(path+[loc])]=[' '.join(['{} {}'.format(x[0],x[1]) for x in path+[loc]])]
                else:
                    self.solnsdict[self.extract(path+[loc])].append(' '.join(['{} {}'.format(x[0],x[1]) for x in path+[loc]]))
            if self.extract(path+[loc]) in self.lpfxs:
                for step in adjacencies(loc,path):
                    extend((step[0]+loc[0],step[1]+loc[1]),path+[loc])
                

        for i in range(4):
            for j in range(4):
                extend((i,j),[]) 

    # The extract() method takes a path and returns the underlying
    # word from the puzzle board.
    def extract(self, path):
        word=''
        for coords in path:
            word += self.board[coords[0]][coords[1]]
        return word
    # The checkpath() method takes a path and returns the word it
    # represents if the path is legal (i.e., formed of distinct and
    # sequentially adjacent locations) and realizes a legal word,
    # False otherwise.
    def checkpath(self, path):
        #check each step in path
        for i in range(len(path)):
            #check for coords outside board
            if ( path[i][0] not in range(0,4) or path[i][1] not in range(0,4) ):
                return False
            #check for nonadjacent coords
            if i!=0 and ( (path[i][0]-path[i-1][0]) not in (-1,0,1) or (path[i][1]-path[i-1][1]) not in (-1,0,1) ):
                return False
            #checks for repeat coords
            if path[i] in path[:i]:
                return False
        return ( (self.extract(path) in self.words) and self.extract(path) )
    # The round() method plays a round (i.e., a single puzzle) of
    # Boggle. It should return True as long as the player is willing
    # to continue playing additional rounds of Boggle; when it returns
    # False, the Boggle game is over.
    #
    # Hint: Look to HW1's round() function for inspiration.
    #
    # This method will be replaced by an interactive version.
    def rounds(self):
        # The recover() helper function converts a list of integers
        # into a path. Thus '3 2 2 1 1 2 2 3' becomes [(3, 2), (2, 1),
        # (1, 2), (2, 3)].
        self.newgame()
        print('Welcome to Boggle!')        
        self.solve()
        print('This puzzle contains {} legal solutions'.format(len(self.solns)))
        print('Cheat***: {}'.format((len(self.solns)==0 and '{}') or self.solns))
        print('{}'.format(self.solnsdict))        
        print( "Input 'r1 c1 r2 c2...'; '/'=display, ':'=show, '+'=new puzzle; ','=quit\n   where 'r1 c1 r2 c2...' specifies a path as series of row,col coordinates." )
        print(self)
        gset=set()
        def recover(path):
            L=path.split() #for cleanliness 
            return [(int(L[i-1]),int(L[i])) for i in range(1,len(L),2)]

        while True:
            user=input('Boggle>').strip()
            if user=='/':
                print(self)
            elif user==':':
                print('{} words found so far:\n  '.format(len(gset))+'\n  '.join(gset))
            elif user=='+':
                print('You found {} of {} possible words.'.format(len(gset),len(self.solns)))
                return True
            elif user=='.':
                print('You found {} of {} possible words.'.format(len(gset),len(self.solns)))
                print('Thanks for playing')
                return False
            elif not all([x.isdigit() for x in user.split()]):
                print('Use numeric coordinates')
            elif not all([( (i%2==0 and isinstance(user[i],str)) or (i%2==1 and user[i]==' ') ) for i in range(len(user))]) or (len(user)%2)!=1:
                print('Ill-formed coordinates')
            elif not self.checkpath(recover(user)) and (self.extract(path) in self.words) :
                print('Illegal path')
            elif not self.extract(recover(user)):
                print("Unrecognized word '{}'".format(self.extract(recover(user))))
            elif self.extract(recover(user)) in gset:
                print('Word already found')
            else:
                print("'{}' added to list".format(self.extract(recover(user))))
                gset.add(self.extract(recover(user)))
    # The play() method when invoked initiates a sequence of
    # individual Boggle rounds by repeatedly invoking the rounds()
    # method as long as the user indicates they are interested in
    # playing additional puzzles.
    #
    # Hint: Look to HW1's play() function for inspiration.
    #
    # This method will be replaced by an interactive version.
    def play(self):
        while self.rounds():
            pass

######################################################################
if __name__ == '__main__':
    Boggle()
