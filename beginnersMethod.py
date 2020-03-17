from Cube import UP, FRONT, DOWN, RIGHT, LEFT, BACK, EDGETOP, EDGERIGHT, EDGEDOWN, EDGELEFT, CORNERTOPLEFT, CORNERTOPRIGHT, CORNERDOWNRIGHT, CORNERDOWNLEFT
from Cube import Cube

MAXITER = 1000 #if a loop exceeds this number, then the cube is definetely wrong

class BeginnersCube(Cube):

    def solve(self):
        """
        Solve cube using beginners method, returns True if cube is solved succeesfully
        and False if it can't be solved
        """
        self.changePerspective()
        
        try:
            self.solveUpperCross()
            self.solveUpperCorners()
            self.solveSecondLayer()
            self.orientLowerCross()
            self.solveLowerCross()
            self.solveLowerCornersPosition()
            self.solveLowerCornersOrientation()

            self.shortenSolution()
            return True
        except:
            return False


    def shortenSolution(self):
        """
        Removes redundant steps from solution
        """
        if len(self.movesDone) == 0: return
        
        strSolution = " ".join(self.movesDone) + " "

        for color in [UP, DOWN, RIGHT, LEFT, FRONT, BACK]:

            strSolution = strSolution.replace(color + "p ", color + " " + color + " " + color + " ")
            strSolution = strSolution.replace(color + "2 ", color + " " + color + " ")

            strSolution = strSolution.replace(color + " "  + color + " " + color + " " + color + " ", " ") 
            strSolution = strSolution.replace(color + " "  + color + " " + color + " ", color + "p ")

            strSolution = strSolution.replace(color + " "  + color + " ", color + "2 ")

        newMoves = strSolution.split(" ")
        newMoves = list(filter(lambda a: a != "", newMoves))


        self.movesDone = newMoves
        

    def correctEdges(self, faceColor):
        """
        Returns number of correct edges for specified face
        """
        counter = 0
        for index in [EDGEDOWN, EDGELEFT, EDGERIGHT, EDGETOP]:
            if self.cubeDict[faceColor]['colors'][index] == faceColor and self.getEdgeOther(faceColor, index) == self.getAdjFaceColor(faceColor, index):
                counter += 1
        return counter

    def correctCorners(self, faceColor):
        """
        Returns number of correct corners for specified face
        """
        counter = 0
        for index in [CORNERDOWNLEFT, CORNERDOWNRIGHT, CORNERTOPLEFT, CORNERTOPRIGHT]:
            if self.isPieceCorrect(faceColor, index):
                counter += 1
        return counter  

    def cornersCorrectPosition(self, faceColor):
        """
        Returns number of correct corners with correct position (no orientation necessarily) specified face
        """
        counter = 0
        for index in [CORNERDOWNLEFT, CORNERDOWNRIGHT, CORNERTOPLEFT, CORNERTOPRIGHT]:
            if self.isPositionCorrect(faceColor, index):
                counter += 1
        return counter  

    def isFaceCorrect(self, faceColor):
        """
        Returns True if specified face is correct
        """
        return self.correctCorners(faceColor) == self.correctEdges(faceColor) == 4

    def isF2L(self):
        """
        Returns True if first 2 layers are solved
        """
        if not self.isFaceCorrect(UP): return False
        for colorPair in [(FRONT, RIGHT), (RIGHT, BACK), (BACK, LEFT), (LEFT, FRONT)]:
            if not self.isEdgePieceCorrect(*colorPair): return False
        return True

    def isCrossOriented(self, faceColor):
        """
        Return True if cross is oriented properly (edges dont have to be in right positions necessarily)
        """
        for index in [EDGEDOWN, EDGELEFT, EDGERIGHT, EDGETOP]:
            if not self.isOrientationCorrect(faceColor, index): return False
        return True

    def solveUpperCross(self):  
        """
        Solve cross for UP color
        """

    
        for indexDesired in [EDGEDOWN, EDGELEFT, EDGERIGHT, EDGETOP]:
            correctEdges = self.correctEdges(UP)
            if correctEdges == 4: break

            color2 = self.getAdjFaceColor(UP, indexDesired) #Other color of piece
        
            counter = 0
            while not self.isPieceCorrect(UP, indexDesired):
                counter += 1
                if counter >= MAXITER: raise Exception('Wrong cube input')

                faceColor, indexCur = self.findEdge(UP, color2) #face color and index where piece is currently
                faceColor2 = self.getAdjFaceColor(faceColor, indexCur) #The color of the other face where cur piece is

                if faceColor == UP:
                    if correctEdges == 0: self.u() #Make this more efficient
                    else: self.rotate(faceColor2, '2')
                elif faceColor == DOWN:
                    if faceColor2 == color2: self.rotate(faceColor2, '2')
                    else: self.d()
                else:
                    if indexCur == EDGELEFT:
                        self.rotate(faceColor2)
                        self.d('2')
                        self.rotate(faceColor2, 'p')
                    elif indexCur == EDGERIGHT:
                        self.rotate(faceColor2, 'p')
                        self.d('2')
                        self.rotate(faceColor2)
                    elif indexCur == EDGETOP:
                        self.rotate(faceColor)
                    elif indexCur == EDGEDOWN:
                        self.rotate(faceColor)
                        faceColor, indexCur = self.findEdge(UP, color2) #face color and index where piece is currently
                        faceColor2 = self.getAdjFaceColor(faceColor, indexCur) #The color of the other face where cur piece is
                        self.rotate(faceColor2)
                        self.d()
                        self.rotate(faceColor2, 'p')
                        self.rotate(faceColor, 'p')
                    
    def solveUpperCorners(self):
        """
        Solve corners for upper face
        """
        for indexDesired in [CORNERDOWNLEFT, CORNERDOWNRIGHT, CORNERTOPLEFT, CORNERTOPRIGHT]:
            correctCorners = self.correctCorners(UP)
            if correctCorners == 4: break

            color2, color3 = self.getAdjFaceColor(UP, indexDesired)

            counter = 0
            while not self.isPieceCorrect(UP, indexDesired):
                counter += 1
                if counter >= MAXITER: raise Exception('Wrong cube input')

                curFaceColor, curIndex = self.findCorner(UP, color2, color3) #current face and index of white face of piece 
                adjColor1, adjColor2 = self.getAdjFaceColor(curFaceColor, curIndex) #current adjacent faces of piece

                if curFaceColor == UP:
                    self.rotate(adjColor1)
                    self.d('2')
                    self.rotate(adjColor1, 'p')
                elif curFaceColor == DOWN:
                    if self.isCornerPieceCorrect(UP, adjColor1, adjColor2):
                        self.d()
                    else: 
                        self.rotate(adjColor1, 'p')
                        self.d()
                        self.rotate(adjColor1)
                else:
                    if curIndex == CORNERTOPLEFT: 
                        self.rotate(curFaceColor, 'p')
                        self.d('p')
                        self.rotate(curFaceColor)
                    elif curIndex == CORNERTOPRIGHT:
                        self.rotate(curFaceColor)
                        self.d()
                        self.rotate(curFaceColor, 'p')
                    elif curIndex == CORNERDOWNRIGHT:
                        if color2 == curFaceColor and color3 == adjColor2:
                            self.d('p')
                            self.rotate(adjColor2, 'p')
                            self.d()
                            self.rotate(adjColor2)
                        else:
                            self.d()
                    elif curIndex == CORNERDOWNLEFT:
                        if color2 == adjColor1 and color3 == curFaceColor:
                            self.d()
                            self.rotate(adjColor1)
                            self.d('p')
                            self.rotate(adjColor1, 'p')
                        else: 
                            self.d()

    def solveSecondLayer(self):
        """
        Solve second layer (after first layer is solved)
        """
        if not self.isFaceCorrect(UP): raise Exception
        for colorPair in [(FRONT, RIGHT), (RIGHT, BACK), (BACK, LEFT), (LEFT, FRONT)]:

            counter = 0
            while not self.isEdgePieceCorrect(*colorPair):

                counter += 1
                if counter >= MAXITER: raise Exception('Wrong cube input')
            
                curFaceColor, curIndex = self.findEdge(*colorPair)
                if curFaceColor == DOWN: curFaceColor, curIndex = self.findEdge(*colorPair[::-1])
                self.changePerspective(UP, DOWN, self.cubeDict[curFaceColor]['left'], self.cubeDict[curFaceColor]['right'], curFaceColor, self.cubeDict[self.cubeDict[curFaceColor]['right']]['right'])

                if curIndex == EDGELEFT:
                    self.l()
                    self.d('p')
                    self.l('p')
                    self.d('p')
                    self.f('p')
                    self.d()
                    self.f()
                elif curIndex == EDGERIGHT:
                    self.r('p')
                    self.d()
                    self.r()
                    self.d()
                    self.f()
                    self.d('p')
                    self.f('p')
                else:
                    if not self.cubeDict[curFaceColor]['colors'][EDGEDOWN] == curFaceColor: self.d()
                    else:
                        if self.getAdjFaceColor(curFaceColor, EDGELEFT) == self.getEdgeOther(curFaceColor, EDGEDOWN):
                            self.d()
                            self.l()
                            self.d('p')
                            self.l('p')
                            self.d('p')
                            self.f('p')
                            self.d()
                            self.f()
                        else:
                            self.d('p')
                            self.r('p')
                            self.d()
                            self.r()
                            self.d()
                            self.f()
                            self.d('p')
                            self.f('p')                        


        self.changePerspective()

    def orientLowerCross(self):
        """
        Orient lower cross
        """
        if not self.isF2L(): raise Exception

        lowerFaceColors = self.cubeDict[DOWN]['colors']
        
        counter = 0
        while not self.isCrossOriented(DOWN):
            counter += 1
            if counter >= MAXITER: raise Exception('Wrong cube input')

            while self.getEdgeOther(FRONT, EDGEDOWN) == DOWN or (self.getEdgeOther(LEFT, EDGEDOWN) == DOWN and self.getEdgeOther(BACK, EDGEDOWN) == DOWN):
                counter += 1
                if counter >= MAXITER: raise Exception('Wrong cube input')
                self.d()
            self.f()
            self.d()
            self.l()
            self.d('p')
            self.l('p')
            self.f('p')

    def solveLowerCross(self):
        """
        Solve lower cross
        """

        self.changePerspective(up=DOWN, down=UP, right=LEFT, left=RIGHT) #perspective yellow is up, and white is down

        counter = 0
        while True:

            counter += 1
            if counter >= MAXITER: raise Exception('Wrong cube input')
            
            right, back, left, front = self.cubeDict[RIGHT]['colors'][EDGEDOWN], self.cubeDict[BACK]['colors'][EDGEDOWN], self.cubeDict[LEFT]['colors'][EDGEDOWN], self.cubeDict[FRONT]['colors'][EDGEDOWN]
            if (back, left) in [(FRONT, RIGHT), (RIGHT, BACK), (BACK, LEFT), (LEFT, FRONT)]:

                if (front, back) in [(FRONT, BACK), (BACK, FRONT), (RIGHT, LEFT), (LEFT, RIGHT)]:
                    break
                self.r()
                self.u()
                self.r('p')
                self.u()
                self.r()
                self.u()
                self.u()
                self.r('p')
                break

            elif (front, back) in [(FRONT, BACK), (BACK, FRONT), (RIGHT, LEFT), (LEFT, RIGHT)]:
                self.r()
                self.u()
                self.r('p')
                self.u()
                self.r()
                self.u()
                self.u()
                self.r('p')  
                continue        
            
            self.u()
        
        #Put cross in right position
        while self.correctEdges(DOWN) != 4: 
            counter += 1
            if counter >= MAXITER: raise Exception('Wrong cube input')
            self.u()
        self.changePerspective() #siwtch perspective back to normal
    
    def solveLowerCornersPosition(self):
        """
        Put corners on last layer in correct positions (not orientation)
        """

        if self.cornersCorrectPosition(DOWN) == 0:
            self.d()
            self.l()
            self.d('p')
            self.r('p')
            self.d()
            self.l('p')
            self.d('p')
            self.r()
        
        if self.cornersCorrectPosition(DOWN) == 1:
            if self.isPositionCorrect(FRONT, CORNERDOWNLEFT): pass
            elif self.isPositionCorrect(RIGHT, CORNERDOWNLEFT):
                self.changePerspective(front=RIGHT, left=FRONT, back=LEFT, right=BACK)
            elif self.isPositionCorrect(BACK, CORNERDOWNLEFT):
                self.changePerspective(front=BACK, back=FRONT, left=RIGHT, right=LEFT)
            elif self.isPositionCorrect(LEFT, CORNERDOWNLEFT):
                self.changePerspective(front=LEFT, left=BACK, back=RIGHT, right=FRONT)
            self.d()
            self.l()
            self.d('p')
            self.r('p')
            self.d()
            self.l('p')
            self.d('p')
            self.r()
            if self.cornersCorrectPosition(DOWN) != 4:
                self.d()
                self.l()
                self.d('p')
                self.r('p')
                self.d()
                self.l('p')
                self.d('p')
                self.r()

        if self.cornersCorrectPosition(DOWN) != 4:
            raise Exception('Invalid Cube')
        
        self.changePerspective()

    def solveLowerCornersOrientation(self):
        
        self.changePerspective(up=DOWN, down=UP, right=LEFT, left=RIGHT) #perspective yellow is up, and white is down

        counter = 0
        while not self.isSolved():
            counter += 1
            if counter >= MAXITER: raise Exception('Invalid Cube')

            
            if self.getCornerOther(FRONT, CORNERDOWNRIGHT)[0] == DOWN:
                self.u()
                continue

            for i in range(2):
                self.d()
                self.l()
                self.d('p')
                self.l('p')

            
        self.changePerspective()






