import random
import copy


#conventions
UP = 'w'
FRONT = 'b'
DOWN = 'y'
RIGHT = 'o'
LEFT = 'r'
BACK = 'g'

#Indexes for edges
EDGETOP, EDGERIGHT, EDGEDOWN, EDGELEFT = 1, 5, 7, 3

#Indexes for corners
CORNERTOPLEFT, CORNERTOPRIGHT, CORNERDOWNRIGHT, CORNERDOWNLEFT = 0, 2, 8, 6

#Solved cube dict
SOLVEDCUBEDICT = {'w': {'up': 'g', 'right': 'o', 'down': 'b', 'left': 'r', 'colors': ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w', 'w']}, 'y': {'up': 'b', 'right': 'o', 'down': 'g', 'left': 'r', 'colors': ['y', 'y', 'y', 'y', 'y', 'y', 'y', 'y', 'y']}, 'b': {'up': 'w', 'right': 'o', 'down': 'y', 'left': 'r', 'colors': ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b']}, 'g': {'up': 'w', 'right': 'r', 'down': 'y', 'left': 'o', 'colors': ['g', 'g', 'g', 'g', 'g', 'g', 'g', 'g', 'g']}, 'o': {'up': 'w', 'right': 'g', 'down': 'y', 'left': 'b', 'colors': ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o', 'o']}, 'r': {'up': 'w', 'right': 'b', 'down': 'y', 'left': 'g', 'colors': ['r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r']}}

class Cube:

    def __init__(self, cubeDict=SOLVEDCUBEDICT):
        """
        Constructor
        Parameter: cubeDict (solved cube by default)
        cubeDict should be in the following format
        {'color of face 1': {'up': 'color up', 'right': 'color right', 'down': 'color down', 
        'left': 'color left', 'colors': ['color0', 'color2', ..., 'color8']}, ...}

        The folors in the 'colors field are in the following order'\n
                up \n
                012 \n
        left    345     right \n
                678 \n
                down \n

        All faces adjacent to UP, must have UP at its up direction
        """
        self.cubeDict = copy.deepcopy(cubeDict) #dict representing cube
        self.movesDone = []      #moves done to this cube

        self.up, self.down, self.right, self.left, self.front, self.back = UP, DOWN, RIGHT, LEFT, FRONT, BACK

    def rotate(self, faceColor, mode=""):
        """
            Rotate specified face clock wise (mode = ""), counter clockwise (mode = p) or twice (mode=2) 

            Example (clockwise)\n
             u            l  \n
            012          630 \n
          l 345 r  ->  d 741 u\n
            678          852 \n
             d            r  \n
        """
        face = self.cubeDict[faceColor]
        curColors = face['colors']

        #Rotate faces
        newColors = [None]*9
        if mode == "": 
            newColors[0] = curColors[6]
            newColors[1] = curColors[3]
            newColors[2] = curColors[0]
            newColors[3] = curColors[7]
            newColors[4] = curColors[4]
            newColors[5] = curColors[1]
            newColors[6] = curColors[8]
            newColors[7] = curColors[5]
            newColors[8] = curColors[2]
        elif mode == "p":
            newColors[0]= curColors[2]
            newColors[1] = curColors[5]
            newColors[2] = curColors[8]
            newColors[3] = curColors[1]
            newColors[4] = curColors[4]
            newColors[5] = curColors[7]
            newColors[6] = curColors[0]
            newColors[7] = curColors[3]
            newColors[8] = curColors[6]
        elif mode == "2":
            newColors[0]= curColors[8]
            newColors[1] = curColors[7]
            newColors[2] = curColors[6]
            newColors[3] = curColors[5]
            newColors[4] = curColors[4]
            newColors[5] = curColors[3]
            newColors[6] = curColors[2]
            newColors[7] = curColors[1]
            newColors[8] = curColors[0]

        face['colors'] = newColors


        #rotate pieces in adjacent faces
        #indexes of pieces that need to be rotated, in clockwise order (from rotating face's perspective)
        adjIndexes = {}
        #colors of adj pieces
        adjPieces = {}
        for direction in ['up', 'right', 'down', 'left']:
            adjColor = face[direction]
            adjFace = self.cubeDict[adjColor]

            if adjFace['up'] == faceColor: adjIndexes[direction] = [2, 1, 0]
            elif adjFace['right'] == faceColor: adjIndexes[direction] = [8, 5, 2]
            elif adjFace['down'] == faceColor: adjIndexes[direction] = [6, 7, 8]
            elif adjFace['left'] == faceColor: adjIndexes[direction] = [0, 3, 6]

            adjPieces[direction] = [adjFace['colors'][adjIndexes[direction][0]], adjFace['colors'][adjIndexes[direction][1]], adjFace['colors'][adjIndexes[direction][2]]]

        if mode == "":
            adjPieces['up'], adjPieces['right'], adjPieces['down'], adjPieces['left'] = adjPieces['left'], adjPieces['up'], adjPieces['right'], adjPieces['down']
        elif mode == "p":
            adjPieces['up'], adjPieces['right'], adjPieces['down'], adjPieces['left'] = adjPieces['right'], adjPieces['down'], adjPieces['left'], adjPieces['up']
        elif mode == "2":
            adjPieces['up'], adjPieces['right'], adjPieces['down'], adjPieces['left'] = adjPieces['down'], adjPieces['left'], adjPieces['up'], adjPieces['right']

        for direction in ['up', 'right', 'down', 'left']:
            adjColor = face[direction]
            adjFaceColors = self.cubeDict[adjColor]['colors']
            indexes = adjIndexes[direction]

            adjFaceColors[indexes[0]], adjFaceColors[indexes[1]], adjFaceColors[indexes[2]] = adjPieces[direction][0], adjPieces[direction][1], adjPieces[direction][2] 

        self.movesDone.append(faceColor+mode) #add cur move to moves done

    def __str__(self):
        """
        String representation of the cube
        """
        s = ""
        for face in ['w', 'y', 'b', 'g', 'r', 'o']:
            leftSpacing = 10 
            left = self.cubeDict[face]['left']
            right = self.cubeDict[face]['right']
            s += face + "--------\n"
            s += "                     " + self.cubeDict[face]['up'] + "\n"
            s += " "*leftSpacing + str(self.cubeDict[face]['colors'][0:3]) + "\n"
            s += left + " "*(leftSpacing - len(left))+ str(self.cubeDict[face]['colors'][3:6]) + "    " + right +"\n"
            s += " "*leftSpacing + str(self.cubeDict[face]['colors'][6:9]) + "\n"
            s += "                     " + self.cubeDict[face]['down'] + "\n"*2
        return s


    def getState(self):
        """
        Short way for representing cube state
        """
        s = "".join(self.cubeDict["w"]["colors"]) 
        s += "".join(self.cubeDict["y"]["colors"]) 
        s += "".join(self.cubeDict["b"]["colors"]) 
        s += "".join(self.cubeDict["g"]["colors"]) 
        s += "".join(self.cubeDict["r"]["colors"]) 
        s += "".join(self.cubeDict["o"]["colors"]) 
        return s

    def changePerspective(self, up=UP, down= DOWN, left= LEFT, right=RIGHT, front = FRONT, back= BACK):
        """
        Change perspective from which cube is seen
        """
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.front = front
        self.back = back

    def f(self, mode=""):
        """
        Rotate front face 
        mode="" (default): clockwise, mode="2": twice, mode="p": counterclockwise
        """
        self.rotate(self.front, mode=mode)

    def u(self, mode=""):
        self.rotate(self.up, mode=mode)

    def r(self, mode=""):
        self.rotate(self.right, mode=mode)

    def d(self, mode=""):
        self.rotate(self.down, mode=mode)
    
    def l(self, mode=""):
        self.rotate(self.left, mode=mode)

    def b(self, mode=""):
        self.rotate(self.back, mode=mode)

    def clearMoves(self):
        """
        Reset array with moves
        """
        self.movesDone = []

    def undoMoves(self, n):
        """
        undo the last n moves
        if n > moves done, it will simply stop
        """
        counter = 0
        while len(self.movesDone) > 0 and counter < n:
            move = self.movesDone.pop()
            face, mode = move[0], ""
            if move[-1] == '2': mode = '2'
            elif move[-1] == 'p': pass
            else: mode = 'p'

            self.rotate(face, mode)
            self.movesDone.pop()
            counter += 1

    def isSolved(self):
        """
        Returns True if cube is solved
        """
        return self.getState() == "wwwwwwwwwyyyyyyyyybbbbbbbbbgggggggggrrrrrrrrrooooooooo"

    def scramble(self, moves='random', clear=True, seed=None):
        """
        Scramble cube.
        moves = number of moves to use, if it is 'random', then it chooses a random nuumber
        between 100 and 200
        clear = Boolean, whether you want to clear all moves done to cube from movesDone list
        """
        if seed != None: random.seed(seed)
        if moves == 'random': moves = random.randint(100, 200)
        for i in range(moves):
            face = random.choice(['w', 'y', 'b', 'g', 'r', 'o'])
            mode = random.choice(["", "p", "2"])
            self.rotate(face, mode)

        if clear: self.movesDone = []

    def getAdjFaceColor(self, faceColor, index):
        
        """
        Return color(s) of adjacent face to given face and index at counter clockwise order
        """

        if index == EDGERIGHT: return self.cubeDict[faceColor]['right']
        elif index == EDGETOP: return self.cubeDict[faceColor]['up']
        elif index == EDGELEFT: return self.cubeDict[faceColor]['left']
        elif index == EDGEDOWN: return self.cubeDict[faceColor]['down']
        elif index == CORNERTOPLEFT: return self.cubeDict[faceColor]['up'], self.cubeDict[faceColor]['left']
        elif index == CORNERDOWNLEFT: return self.cubeDict[faceColor]['left'], self.cubeDict[faceColor]['down']
        elif index == CORNERDOWNRIGHT: return self.cubeDict[faceColor]['down'], self.cubeDict[faceColor]['right']
        elif index == CORNERTOPRIGHT : return self.cubeDict[faceColor]['right'], self.cubeDict[faceColor]['up']
        else: raise Exception

    def getEdgeOther(self, faceColor, index):
        """
        Gets the other color of the small edge cube with seleceted face index
        """
        if index > 7 or index < 1 or index % 2 == 0: raise Exception

        adjFaceColor = None
        if index == EDGERIGHT: adjFaceColor = self.cubeDict[faceColor]['right']
        elif index == EDGEDOWN: adjFaceColor = self.cubeDict[faceColor]['down']
        elif index == EDGELEFT: adjFaceColor = self.cubeDict[faceColor]['left']
        elif index == EDGETOP: adjFaceColor = self.cubeDict[faceColor]['up']
        else: raise Exception

        adjFace = self.cubeDict[adjFaceColor]
        if adjFace['right'] == faceColor: return adjFace['colors'][EDGERIGHT]
        elif adjFace['up'] == faceColor: return adjFace['colors'][EDGETOP]
        elif adjFace['left'] == faceColor: return adjFace['colors'][EDGELEFT]
        elif adjFace['down'] == faceColor: return adjFace['colors'][EDGEDOWN]
        else: raise Exception

    def getCornerOther(self, faceColor, index):
        """
        Gets the other colors of small corner cube with selected index.
        Returns colors in counter clockwise direction from face perspective
        """
        if index > 8 or index < 0 or index % 2 == 1: raise Exception
        
        adjFaceColor1, adjFaceColor2 = None, None
        if index == CORNERTOPLEFT: adjFaceColor1, adjFaceColor2 = self.cubeDict[faceColor]['up'], self.cubeDict[faceColor]['left']
        elif index == CORNERDOWNLEFT: adjFaceColor1, adjFaceColor2 = self.cubeDict[faceColor]['left'], self.cubeDict[faceColor]['down']
        elif index == CORNERDOWNRIGHT: adjFaceColor1, adjFaceColor2 = self.cubeDict[faceColor]['down'], self.cubeDict[faceColor]['right']
        elif index == CORNERTOPRIGHT: adjFaceColor1, adjFaceColor2 = self.cubeDict[faceColor]['right'], self.cubeDict[faceColor]['up']
        else: raise Exception

        ###
        color1, color2 = None, None
        adjFace1, adjFace2 = self.cubeDict[adjFaceColor1], self.cubeDict[adjFaceColor2]
        if adjFace1['left'] == faceColor: color1 = adjFace1['colors'][CORNERTOPLEFT]
        elif adjFace1['up'] == faceColor: color1 = adjFace1['colors'][CORNERTOPRIGHT]
        elif adjFace1['right'] == faceColor: color1 = adjFace1['colors'][CORNERDOWNRIGHT]
        elif adjFace1['down'] == faceColor: color1 = adjFace1['colors'][CORNERDOWNLEFT]
        else: raise Exception

        if adjFace2['left'] == faceColor: color2 = adjFace2['colors'][CORNERDOWNLEFT]
        elif adjFace2['up'] == faceColor: color2 = adjFace2['colors'][CORNERTOPLEFT]
        elif adjFace2['right'] == faceColor: color2 = adjFace2['colors'][CORNERTOPRIGHT]
        elif adjFace2['down'] == faceColor: color2 = adjFace2['colors'][CORNERDOWNRIGHT]
        else: raise Exception

        return color1, color2

    def isLayerCorrect(self, faceColor, index):
        """
        Returns True if piece is in the correct layer
        """
        if index in [EDGETOP, EDGERIGHT, EDGEDOWN, EDGELEFT]:
            return self.cubeDict[faceColor]['colors'][index] == faceColor or self.getEdgeOther(faceColor, index) == faceColor
        elif index in [CORNERTOPLEFT, CORNERTOPRIGHT, CORNERDOWNRIGHT, CORNERDOWNLEFT]:
            otherColor1, otherColor2 = self.getCornerOther(faceColor, index)
            return faceColor in [self.cubeDict[faceColor]['colors'][index], otherColor1, otherColor2]
        else: return False


    def isPositionCorrect(self, faceColor, index):
        """
        Returns True if position of piece is correct
        """
        if not self.isLayerCorrect(faceColor, index): return False

        ####
        if index in [EDGETOP, EDGERIGHT, EDGEDOWN, EDGELEFT]: 
            otherColor = self.getAdjFaceColor(faceColor, index)
            return self.cubeDict[faceColor]['colors'][index] == otherColor or self.getEdgeOther(faceColor, index) == otherColor
        
        elif index in [CORNERTOPLEFT, CORNERTOPRIGHT, CORNERDOWNRIGHT, CORNERDOWNLEFT]:
            color1, color2 = self.getCornerOther(faceColor, index)
            adjColor1, adjColor2 = self.getAdjFaceColor(faceColor, index)
            return color1 in [faceColor, adjColor1, adjColor2] and color2 in [faceColor, adjColor1, adjColor2] and self.cubeDict[faceColor]['colors'][index] in [faceColor, adjColor1, adjColor2]
        else: raise Exception

    def isPieceCorrect(self, faceColor, index):
        """
        Returns True if the piece corresponding to given color and index is in the correct position and orientation
        """
        return self.isPositionCorrect(faceColor, index) and self.isOrientationCorrect(faceColor, index)

    def isCornerPieceCorrect(self, color1, color2, color3):
        """
        Returns True if corner piece with given colors is correct
        """
        faceColor, index = self.findCorner(color1, color2, color3)
        return self.isPieceCorrect(faceColor, index)

    def isEdgePieceCorrect(self, color1, color2):
        """
        Returns True if edge with specified colors is in correct postion and orientation
        """
        faceColor, index = self.findEdge(color1, color2)
        return self.isPieceCorrect(faceColor, index)

    def isOrientationCorrect(self, faceColor, index):
        """
        Returns True if orientation of piece is correct
        """
        return self.cubeDict[faceColor]['colors'][index] == faceColor

    def findEdge(self, color1, color2):
        """
        Returns face color and index of color 1 of edge piece with color1 and color2
        """
        for color in [UP, DOWN, FRONT, BACK, RIGHT, LEFT]:
            for  index in [EDGEDOWN, EDGETOP, EDGELEFT, EDGERIGHT]:
                if self.cubeDict[color]['colors'][index] == color1:
                    if self.getEdgeOther(color, index) == color2:
                        return color, index
        raise Exception

    def findCorner(self, color1, color2, color3):
        """
        Returns face color and index of color 1 of corner piece with color1, color2 and color3
        """
        for color in [UP, DOWN, FRONT, BACK, RIGHT, LEFT]:
            for  index in [CORNERDOWNLEFT, CORNERDOWNRIGHT, CORNERTOPLEFT, CORNERTOPRIGHT]:
                if self.cubeDict[color]['colors'][index] == color1:
                    otherColor1, otherColor2 = self.getCornerOther(color, index)
                    if color2 in [otherColor1, otherColor2] and color3 in [otherColor1, otherColor2]:
                        return color, index
        raise Exception


