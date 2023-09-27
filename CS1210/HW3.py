def solve(board):
    solns = set()
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
        def readwords(filename='words.dat'):
            infile=open(filename)
            words = []
            lpfxs = set()
            c=0
            for line in infile:
                s=line.lower().strip()
                words.append(s)
                lpfxs.update({s[:i] for i in range(len(line.lower().strip()))})
                c += 1
            print( 'Read {} words'.format(c) )
            infile.close()
            return words,lpfxs
        words,lpfxs=readwords()
        def extract(path):
            word=''
            for coords in path:
                word += board[coords[0]][coords[1]]
            return word        
        if extract(path+[loc]) in words:
            solns.update({extract(path+[loc])})
        if extract(path+[loc]) in self.lpfxs:
            for step in adjacencies(loc,path):
                extend((step[0]+loc[0],step[1]+loc[1]),path+[loc])
    #extend starting from each loc on the board
    for i in range(4):
        for j in range(4):
            extend((i,j))
    return solns
