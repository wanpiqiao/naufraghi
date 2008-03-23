#!/urs/bin/env python
# -*- encoding: utf-8 -*-

pieces_data = """
.#..##
.#####
#####.
.####.
######
##..##

..##..
.#####
#####.
#####.
.#####
.#.#..

##..##
######
.####.
######
.####.
..##..


..#.##
.####.
######
######
.####.
..##..

..##..
.#####
#####.
#####.
.#####
..#.##

##..#.
######
.####.
.####.
######
..##..
"""

def getPerimeter(piece):
    """Convert an ASCII piece in a boolean perimeter

    >>> piece = ["..##..",\
                 ".#####",\
                 "#####.",\
                 "#####.",\
                 ".#####",\
                 "..#.##"]
    >>> getPerimeter(piece)
    [0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0]
    """
    def isUp(p):
        return int(p == "#")
    top = map(isUp, piece[0])
    right = map(isUp, [r[-1] for r in piece[1:-1]])
    bottom = map(isUp, reversed(piece[-1]))
    left = map(isUp, [r[0] for r in piece[-2:0:-1]]) # bottom-up 
    return top + right + bottom + left

def parsePieces(pieces_data):
    r"""Parse a file containing ASCII pieces

    >>> data = "\n".join(["aaa", "", "bbb", "", "", "ccc", "ddd"])
    >>> list(parsePieces(data))
    [['aaa'], ['bbb'], ['ccc', 'ddd']]
    """
    pieces = []
    for line in pieces_data.strip().split("\n"):
        if line.strip() != "":
            pieces.append(line.strip())
        elif pieces:
            yield list(pieces)
            pieces = []
    yield list(pieces)

def getSide(face, side, rotation=0, flip=0):
    """ Get a side from a perimeter considering rotation and flipping

    >>> face = [0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0]
    >>> [getSide(face, i, 0, 0) for i in range(4)]
    [[0, 0, 1, 1, 0, 0], [0, 1, 0, 0, 1, 1], [1, 1, 0, 1, 0, 0], [0, 0, 1, 1, 0, 0]]
    >>> getSide(face, 0, 2, 0)
    [1, 1, 0, 1, 0, 0]
    >>> getSide(face, 0, 0, 1)
    [0, 0, 1, 1, 0, 0]
    """
    _face = face + [face[0]]
    if flip: # diagonal flip
        _face = list(reversed(_face))
    _side = (side + rotation) % 4
    return _face[_side*5: _side*5 + 6]

def getPiece(face):
    """ Reconstrunct a piece given the perimeter

    >>> piece = ["..##..",\
                 ".#####",\
                 "#####.",\
                 "#####.",\
                 ".#####",\
                 "..#.##"]
    >>> getPiece(getPerimeter(piece))
    ['..##..', '.#####', '#####.', '#####.', '.#####', '..#.##']
    >>> piece == getPiece(getPerimeter(piece))
    True
    """
    def toChar(point):
        return point and "#" or "."
    top = getSide(face, 0)
    N = len(top)
    right = getSide(face, 1)
    left = getSide(face, 0, 0, 1)
    assert left == list(reversed(getSide(face, 3)))
    _face = ["".join(map(toChar, top))]
    for i in range(1, N-1):
        row = [left[i]] + ["#"]*(N-2) + [right[i]]
        _face += ["".join(map(toChar, row))]
    bottom = getSide(face, 1, 0, 1)
    assert bottom == list(reversed(getSide(face, 2)))
    return _face + ["".join(map(toChar, bottom))]
    

def isCompatible(side1, side2):
    """Compare 2 sides for compatibility (one must be reversed)

    >>> face = [1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1]
    >>> isCompatible(getSide(face, 0, 0, 0), getSide(face, 0, 0, 0))
    False
    >>> isCompatible(getSide(face, 0, 0, 0), getSide(face, 0, 2, 0))
    True
    """
    N = len(side1)
    for i in range(N):
        if side1[i] + side2[N-i-1] > 1:
            return False
    return True

def canPlace(side1, face1, rot1, flip1, face2, rot2, flip2):
    side2 = (side1 + 2) % 4
    s1 = getSide(face1, side1, rot1, flip1)
    s2 = getSide(face2, side2, rot2, flip2)
    return isCompatible(s1, s2)

""" A valid cube must satisfy 12 edge rules
                ---------
                |       |
                | (0,2) |
                |       |
        -------------------------
        |       /[4]    /       |
        | (4,1) / (4,0) / (4,3) |
        |       /       /       |
-----------------------------------------
|[0]    |[1]    |[2]    |[3]    |       |
| (0,0) | (1,0) | (2,0) | (3,0) | (0,0) |
|       |       |       |       |       |
-----------------------------------------
        |       /[5]    /       |
        | (5,3) / (5,0) / (5,1) |
        |       /       /       |
        -------------------------
                |       |
                | (0,2) |
                |       |
                ---------
"""

def isValid(*args):
    N = len(args)
    def getRot((face, rotation, flip), rot):
        return (face, rotation + rot, flip)
    def isValid1(s0, s1):
        res =  canPlace(1, *(s0 + s1))
        return res
    def isValid2(s0, s1, s2):
        res =  canPlace(1, *(s1 + s2))
        return res
    def isValid3(s0, s1, s2, s3):
        res =  canPlace(1, *(s2 + s3)) and\
               canPlace(1, *(s3 + s0))
        return res
    def isValid4(s0, s1, s2, s3, s4):
        res =  canPlace(0, *(s2 + s4)) and\
               canPlace(0, *(s1 + getRot(s4, 1))) and\
               canPlace(0, *(s4 + getRot(s0, 2))) and\
               canPlace(0, *(s3 + getRot(s4, 3)))
        return res
    def isValid5(s0, s1, s2, s3, s4, s5):
        res =  canPlace(2, *(s2 + s5)) and\
               canPlace(2, *(s1 + getRot(s5, 3))) and\
               canPlace(2, *(s5 + getRot(s0, 2))) and\
               canPlace(2, *(s3 + getRot(s5, 1)))
        return res
    return [isValid1, isValid2, isValid3, isValid4, isValid5][N-2](*args)

# http://www.kuro5hin.org/story/2002/4/1/153/77985 ---------------------
def combinations( L ):
    N = len( L )
    if N == 0:
        return []
    elif N == 1:
        return [
        L[0][i:i+1]
        for i in xrange( 0, len( L[0] ) )
    ]
    else:
        return [
            L[0][i:i+1] + subcomb
            for i in xrange( 0, len( L[0] ) )
            for subcomb in combinations( L[1:] )
        ]
 
def permutations( L ):
    N = len( L )
    if N == 0:
        return []
    elif N == 1:
        return [L]
    else:
        return [
            L[i:i+1] + subperm
            for i in xrange( 0, N )
            for subperm in permutations( L[:i] + L[i+1:] )
        ]
# ----------------------------------------------------------------------

# place = (face, rotation, flip)
# state = [place, place, ...]
# states = [state, state, ...]

def expander(faces, rotations, flips):
    def _expand(state):
        free_faces = [f for f in faces if f not in [s[0] for s in state]]
        new_states = []
        if free_faces:
            for new_place in map(tuple, combinations((free_faces, rotations, flips))):
                test = state + [new_place]
                if isValid(*test):
                    new_states.append(test)
            return new_states
        else:
            return [state,]
    def expand(states):
        expansion = []
        for i, state in enumerate(states):
            expansion.extend(_expand(state))
        return expansion
    return expand
        

def run():
    pieces = parsePieces(pieces_data)
    faces = map(getPerimeter, pieces)
    def name_face(face):
        return "f%s" % faces.index(face)
    def name_place(place):
        return "(%s %s %s)" % (name_face(place[0]), place[1], place[2])
    print "faces = ", map(name_face, faces)
    start_state = [(faces[0], 0, 0),]
    states = [start_state,]
    expand = expander(faces, [0,1,2,3], [0,1])
    print "Starting from state =", name_place(start_state[0])
    while True:
        print "looping...", len(states), "states..."
        _states = expand(states)
        if _states != states:
            states = _states
        else:
            break
    print "states = [", ",\n".join([str(map(name_place, state)) for state in states]), "]"
    print "Done!!"
 
if __name__ == "__main__":
    import sys
    if "solve" in sys.argv:
        run()
    else:
        import doctest
        doctest.testmod()

"""
Test run:

foucault:sandbox matteo$ time python cubetto.py solve
faces =  ['f0', 'f1', 'f2', 'f3', 'f4', 'f5']
Starting from state = (f0 0 0)
looping... 1 states...
looping... 16 states...
looping... 150 states...
looping... 136 states...
looping... 24 states...
looping... 6 states...
states = [ ['(f0 0 0)', '(f1 1 1)', '(f3 3 0)', '(f2 0 0)', '(f4 3 0)', '(f5 0 0)'],
['(f0 0 0)', '(f1 1 1)', '(f3 3 0)', '(f2 3 1)', '(f4 3 0)', '(f5 0 0)'],
['(f0 0 0)', '(f4 1 1)', '(f3 3 0)', '(f2 0 0)', '(f1 3 0)', '(f5 0 0)'],
['(f0 0 0)', '(f4 1 1)', '(f3 3 0)', '(f2 3 1)', '(f1 3 0)', '(f5 0 0)'],
['(f0 0 0)', '(f5 2 1)', '(f2 2 1)', '(f4 1 0)', '(f3 2 0)', '(f1 1 1)'],
['(f0 0 0)', '(f5 2 1)', '(f2 3 0)', '(f4 1 0)', '(f3 2 0)', '(f1 1 1)'] ]
Done!!

real	0m0.221s
user	0m0.204s
sys	0m0.015s
"""
