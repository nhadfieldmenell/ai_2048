from __future__ import print_function
import sys, random, heapq, copy
import numpy as np
from collections import defaultdict

allPositions = [(x,y) for x in range(4) for y in range(4)]

scoreEnd = 0

#score when 0 in snaking pattern
score0 = 5

#score when 1 in snaking pattern
score1 = 15
score2 = 16
score3 = 17
score4 = 18
score5 = 19
score6 = 20
score7 = 21
score8 = 22

#directions: 1 is up, 2 is right, 3 is down, 4 is left, 0 is nothing
#corners correspond to quadrant

"""
	 x0  x1  x2  x3
	+---+---+---+---+
 y0	|	|	|	|	|
	+---+---+---+---+
 y1	|	|	|	|	|
	+---+---+---+---+
 y2	|	|	|	|	|
	+---+---+---+---+
 y3	|	|	|	|	|
	+---+---+---+---+
"""

class Board(object):
	def __init__(self,copyBoard = None):
		if (copyBoard == None):
			self.board = np.zeros((4,4),dtype = np.int)
			self.num2pos = defaultdict(list)
			self.num2pos[0] = copy.copy(allPositions)
			self.addRandomTile()
			self.addRandomTile()

		else:
			pass


	def move(self,direction):
		return

	def setVal(self,x,y,val):
		self.num2pos[self.board[x,y]].remove((x,y))
		self.num2pos[val].append((x,y))
		self.board[x,y] = val
		return val

	def testBoard(self):
		#THIS IS BAD DOESNT SET NUM2POS
		self.board = np.zeros((4,4),dtype = np.int)
		self.board[3,3] = 4
		self.board[3,2] = 4
		self.board[2,3] = 4
		self.board[2,0] = 2
		self.newTurn()

	#board is in end state if there is no free tile and no adjacent matching tiles
	#return False if there is no possible move
	#otherwise, return True
	def inEndState(self):
		if len(self.num2pos[0]) != 0:
			return False


		#means all spaces are full
		for (x,y) in allPositions:
			if y != 3:
				if self.board[x,y] == self.board[x,y+1]:
					return False
			if x != 3:
				if self.board[x,y] == self.board[x+1,y]:
					return False
		return True

	#find a random open tile on the board
	#insert a 2 there (90%)
	#insert a 4 there (10%)
	#return 0 if could not add tile
	#return 1 on success
	def addRandomTile(self):
		if len(self.num2pos[0]) == 0:
			return 0

		(x,y) = random.choice(self.num2pos[0])
		self.num2pos[0].remove((x,y))
		twoOrFour = random.randrange(0,10)
		newTileNum = 2
		if twoOrFour == 9:
			newTileNum = 4
		print(self.num2pos)
		self.setVal(x,y,newTileNum)
		#self.board[x,y] = newTileNum
		#self.num2pos[newTileNum].append((x,y))

	#return a list of coordinate spaces that have a 0 tile
	def unfilledSpots(self):
		return num2pos[0]

	def printBoard(self):
		#show board
		for y in range(4):
			print ("+-----+-----+-----+-----+\n|", end = "")
			for x in range(4):
				if self.board[x,y] == 0:
					print ("     |", end = "")
				elif self.board[x,y] < 10:
					print(" ", end = " ")
					print(self.board[x,y], end = "  |")
				elif self.board[x,y] < 100:
					print (" ", end = "")
					print(self.board[x,y], end = "  |")
				elif self.board[x,y] < 1000:
					print (" ", end = "")
					print(self.board[x,y], end = " |")
				elif self.board[x,y] < 10000:
					print (" ", end = "")
					print(self.board[x,y], end = "|")
				elif self.board[x,y] < 100000:
					print(self.board[x,y], end = "|")
			print ("\n", end = "")
		print ("+-----+-----+-----+-----+")

	def newTurn(self):
		print (self.num2pos)
		#show board
		self.printBoard()
		change = 0
		if self.inEndState():
			print("        Game Over")
			return
		#userInput = raw_input('Pick a move (a, w, s, d, g for genius, q for quit): ')
		userInput = raw_input('Pick a move (a, w, s, d, q for quit): ')
		interpCmd = {'a': 'L', 'w': 'U', 'd':'R', 's': 'D'}
		if userInput == "g":
			change = searchEM(self.board)
		elif userInput == "q":
			return
		else:
			change = self.move(interpCmd[userInput])
		if change != 0:
			self.addRandomTile()
		self.newTurn()
		return

	def move(self,direction):
		dir2majorAxis = {'L': (0,1,4,1,-1,0), 'R': (0,2,-1,-1,4,3), 'U': (1,1,4,1,-1,0), 'D': (1,2,-1,-1,4,3)}
		changes = 0
		#XorY: 0 for x is major axis, 1 for y is major axis
		XorY, majorStart, majorEnd, inc, majorOpposite, majorDone = dir2majorAxis[direction]
		
		for minor in range(4):
			#print ("minor: " + str(minor))
			condensed = defaultdict(int)
			for major0 in range(majorStart,majorEnd,inc):
				#print ("major0: " + str(major0))
				currentVal = 0
				if not XorY:
					currentVal = self.setVal(major0,minor,0)
				else:
					currentVal = self.setVal(minor,major0,0)
				#print ("currentVal: " + str(currentVal))
				if currentVal != 0:
					for major1 in range(major0-inc,majorOpposite,-inc):
						#print ("major1: " + str(major1))
						valAtSpot = 0
						if not XorY:
							valAtSpot = self.board[major1,minor]
						else:
							valAtSpot = self.board[minor,major1]
						#print ("valAtSpot: " + str(valAtSpot))
						if valAtSpot != 0:
							if valAtSpot == currentVal and condensed[major1] == 0:
								if not XorY:
									self.setVal(major1,minor,2*valAtSpot)
									#self.board[major1,minor] = 2*valAtSpot
								else:
									self.setVal(minor,major1,2*valAtSpot)
									#self.board[minor,major1] = 2*valAtSpot
								changes += 1
								condensed[major1] = 1
							else:
								if not XorY:
									self.setVal(major1+inc,minor,currentVal)
									#self.board[major1+inc,minor] = currentVal
								else:
									self.setVal(minor,major1+inc,currentVal)
									#self.board[minor,major1+inc] = currentVal
							if major1+inc != major0:
								changes += 1
							break
						elif major1 == majorDone:
							if not XorY:
								print (str(minor) + str(major1))
								self.setVal(majorDone,minor,currentVal)
								#self.board[majorDone,minor] = currentVal
								changes += 1
								break
							else:
								print (str(minor) + str(major1))
								self.setVal(minor,majorDone,currentVal)
								#self.board[minor,majorDone] = currentVal
								changes += 1
								break
		return changes
				
				
			

		
		#for minor_axis 0->3:
		#	for major_axis 2nd to 4th:
		#		for condense_spot major_axis->0th:
		#			move it through any 0s
		#			if the first non-0 is the same value:
		#				if it is not condensed: condense it
		#			else:
		#				leave the number in the last 0
		#








#board is in end state if there is no free tile and no adjacent matching tiles
#return False if there is no possible move
#otherwise, return True
def inEndState(theBoard):
	for x in range(4):
		for y in range(4):
			if theBoard[x,y] == 0:
				return False
	
	#means all spaces are full
	for x in range(4):
		for y in range(4):
			if y != 3:
				if theBoard[x,y] == theBoard[x,y+1]:
					return False
			if x != 3:
				if theBoard[x,y] == theBoard[x+1,y]:
					return False
	return True
		


#find a random open tile on the board
#insert a 2 there (90%)
#insert a 4 there (10%)
#return 0 if could not add tile
#return 1 on success
def addRandomTile(theBoard):
	emptySpots = []
	for x in range(4):
		for y in range(4):
			if theBoard[x,y] == 0:
				emptySpots.append([x,y])
				
	if len(emptySpots) == 0:
		return 0
		
	spotToFill = random.randrange(0,len(emptySpots))
	twoOrFour = random.randrange(0,10)
	newTileNum = 2
	if twoOrFour == 9:
		newTileNum = 4
		
	theBoard[emptySpots[spotToFill][0],emptySpots[spotToFill][1]] = newTileNum

def moveLeft(theBoard):
	changes = 0
	#holds the positions of the tiles that have already been condensed so you dont condense the same space twice
	condensed = []
	for y in range(4):
		#move from leftmost to rightmost
		for x in range(1,4):
			#currentVal is the one we are moving	
			currentVal = theBoard[x,y]		
			theBoard[x,y] = 0
			if currentVal != 0:
				for x2 in range(x-1,-1,-1):
					valAtSpot = theBoard[x2,y]
					if valAtSpot != 0:
						if valAtSpot == currentVal and condensed.count([x2,y]) == 0:
							theBoard[x2,y] = 2*valAtSpot
							changes += 1
							condensed.append([x2,y])
						else:
							theBoard[x2+1,y] = currentVal
							if x2+1 != x:
								changes+= 1
						break
					
					elif x2 == 0:
						theBoard[0,y] = currentVal
						changes += 1
						break
	return changes

def moveUp(theBoard):
	changes = 0
	condensed = []
	for x in range(4):
		for y in range(1,4):
			currentVal = theBoard[x,y]
			theBoard[x,y] = 0
			if currentVal != 0:
				for y2 in range(y-1,-1,-1):
					valAtSpot = theBoard[x,y2]
					if valAtSpot != 0:
						if valAtSpot == currentVal and condensed.count([x,y2]) == 0:
							theBoard[x,y2] = 2*valAtSpot
							changes += 1
							condensed.append([x,y2])
						else:
							theBoard[x,y2+1] = currentVal
							if y2+1 != y:
								changes += 1
						break
						
					elif y2 == 0:
						theBoard[x,0] = currentVal
						changes += 1
						break	
	return changes

def moveRight(theBoard):
	changes = 0
	condensed = []
	for y in range(4):
		for x in range(2,-1,-1):
			currentVal = theBoard[x,y]
			theBoard[x,y] = 0
			if currentVal != 0:
				for x2 in range(x+1,4):
					valAtSpot = theBoard[x2,y]
					if valAtSpot != 0:
						if valAtSpot == currentVal and condensed.count([x2,y]) == 0:
							theBoard[x2,y] = 2*valAtSpot
							changes += 1
							condensed.append([x2,y])
						else:
							theBoard[x2-1,y] = currentVal
							if x2-1 != x:
								changes += 1
						break
					
					elif x2 == 3:
						theBoard[3,y] = currentVal
						changes += 1
						break	
	return changes

def moveDown(theBoard):
	changes = 0
	condensed = []
	for x in range(4):
		for y in range(2,-1,-1):
			currentVal = theBoard[x,y]
			theBoard[x,y] = 0
			if currentVal != 0:
				for y2 in range(y+1,4):
					valAtSpot = theBoard[x,y2]
					if valAtSpot != 0:
						if valAtSpot == currentVal and condensed.count([x,y2]) == 0:
							theBoard[x,y2] = 2*valAtSpot
							changes += 1
							condensed.append([x,y2])
						else:
							theBoard[x,y2-1] = currentVal
							if y2-1 != y:
								changes += 1
						break
						
					elif y2 == 3:
						theBoard[x,3] = currentVal
						changes += 1
						break
	return changes

def moveDir(theBoard,dir):
	#print ("dir: " + dir)
	if dir == 'U':
		return moveUp(theBoard)
	if dir == 'D':
		return moveDown(theBoard)
	if dir == 'L':
		return moveLeft(theBoard)
	if dir == 'R':
		return moveRight(theBoard)
	
#return a list of coordinate spaces that have a 0 tile
def unfilledSpots(board):
	unfilled = []
	for x in range(4):
		for y in range(4):
			if board[x,y] == 0:
				unfilled.append([x,y])
	return unfilled

	
#add a tile of value val to theBoard at (x,y)
def addSpecificTile(theBoard,val,x,y):
	theBoard[x,y] = val


_hcache = {}

#@profile
def trivialHeuristic(board):
	key = tuple(board.flatten())
	if key in _hcache:
		return _hcache[key]

	returnScore = -1

	if inEndState(board):
		returnScore = 0
		_hcache[key] = returnScore
		return returnScore

	maxI = np.argmax(board)

	if maxI in [0,3,12,15]:
		returnScore = 2
	else:
		returnScore = 1

	_hcache[key] = returnScore
	return returnScore


#the heuristic measures how good a state is
#first checks if it is an end state (want to avoid)
#then it sees if the largest is in a corner
#then it sees for how many in a row down one edge are the values descending
#only next-largest is considered so if 3rd largest is next to the largest
#   that only counts for the largest being in the corner
#return the # of biggest->next biggest->next biggest there is starting from one corner and going along some edge
#@profile
def heuristic(board):
	key = tuple(board.flatten())
	if key in _hcache:
		return _hcache[key]

	returnScore = -1

	if inEndState(board):
		_hcache[key] = scoreEnd
		return scoreEnd



	h = []
	for x in range(4):
		for y in range(4):
			if board[x,y] != 0:
				heapq.heappush(h,(0-board[x,y]))

	median = h[len(h)/2]

	biggest = 0-heapq.heappop(h)

	#This is the case where there is a single tile on the board
	if (len(h) == 0):
		return score1

	found = False
	returnScore = 0


	#topLeft is true if the biggest one is in the top left corner, etc.
	topLeft = False
	topRight = False
	botLeft = False
	botRight = False
	#True if the largest is in a top corner
	#False if largest is in bottom corner
	if board[0,0] == biggest:
		topLeft = True
	elif board[3,0] == biggest:
		topRight = True
	elif board[0,3] == biggest:
		botLeft = True
	elif board[3,3] == biggest:
		botRight = True
	else:
		_hcache[key] = score0
		found = True
		returnScore = score0

	#xOrY = {0,1}
	#xOrY = 0: looking for next best along x axis
	#xOrY = 1: looking for next best along y axis
	xOrY = 0

	#1 if moving left->right or up->down, -1 otherwise
	inc = 1

	#now holds the second biggest
	biggest = 0-heapq.heappop(h)

	#holds the position of the previous spot in the snaking pattern
	thisX = 0
	thisY = 0

	if topLeft:
		if board[1,0] == biggest:
			thisX = 1
			thisY = 0
			xOrY = 0
		elif board[0,1] == biggest:
			thisX = 0
			thisY = 1
			xOrY = 1
		else:
			found = True
			returnScore =  score1
	elif topRight:
		if board[2,0] == biggest:
			thisX = 2
			thisY = 0
			xOrY = 0
			inc = -1
		elif board[3,1] == biggest:
			thisX = 3
			thisY = 1
			xOrY = 1
		else:
			_hcache[key] = score1
			found = True
			returnScore = score1
	elif botLeft:
		if board[1,3] == biggest:
			thisX = 1
			thisY = 3
			xOrY = 0
		elif board[0,2] == biggest:
			thisX = 0
			thisY = 2
			xOrY = 1
			inc = -1
		else:
			_hcache[key] = score1
			found = True
			returnScore = score1
	elif botRight:
		if board[2,3] == biggest:
			thisX = 2
			thisY = 3
			xOrY = 0
			inc = -1
		elif board[3,2] == biggest:
			thisX = 3
			thisY = 2
			xOrY = 1
			inc = -1
		else:
			found = True
			returnScore = score1

	for i in range(2):
		if found:
			break
		if (len(h) == 0):
			if i == 0:
				found =  True
				returnScore = score2
			else:
				found = True
				returnScore = score3
		if found:
			break
		biggest = 0-heapq.heappop(h)
		if not xOrY:
			thisX += inc
		else:
			thisY += inc
		if board[thisX,thisY] != biggest:
			if i == 0:
				found = True
				returnScore = score2
			else:
				found = True
				returnScore = score3


	#return score4
	#stuff below here may just make it slower
	inc = -inc

	if not xOrY:
		if topLeft or topRight:
			thisY = 1
		else:
			thisY = 2
	else:
		if topLeft or botLeft:
			thisX = 1
		else:
			thisX = 2


	for i in range(4):
		if found:
			break
		if (len(h) == 0):
			if i == 0:
				found = True
				returnScore = score4
			elif i == 1:
				found = True
				returnScore = score5
			elif i == 2:
				found = True
				returnScore = score6
			else:
				found = True
				returnScore = score7
		if found:
			break
		biggest = 0-heapq.heappop(h)
		if found:
			break
		if board[thisX,thisY] != biggest:
			if i == 0:
				found = True
				returnScore = score4
			elif i == 1:
				found = True
				returnScore = score5
			elif i == 2:
				found = True
				returnScore = score6
			else:
				found = True
				returnScore = score7
		if not xOrY:
			thisX += inc
		else:
			thisY += inc

	if not found:
		found = True
		returnScore = score8
	_hcache[key] = returnScore
	return returnScore


	
	

#pass in a board, a number of remaining maxNode levels to check, 
#whether it is a max node (maxNode==True) or expecti node (maxNode==False)
#return the value of the state given that many steps left
#maxNodes decide between best moves for a board position
#expectiNodes average values of each possible ensuing board position (after placing random tile)
def expectimax(board,maxDepth,maxNode):
	#return the score of the expecti nodes at maxDepth
	if inEndState(board) or (maxDepth == 0 and not maxNode):
		return heuristic(board)
	
	
	
	#handle maxNode
	if maxNode:
		newBoard = np.copy(board)
		moveLeft(newBoard)
		left = expectimax(newBoard,maxDepth-1,False)
		newBoard = np.copy(board)
		moveRight(newBoard)
		right = expectimax(newBoard,maxDepth-1,False)
		newBoard = np.copy(board)
		moveUp(newBoard)
		up = expectimax(newBoard,maxDepth-1,False)
		newBoard = np.copy(board)
		moveDown(newBoard)
		down = expectimax(newBoard,maxDepth-1,False)
		return max(left,right,up,down)
	
	#handle expectiNode
	
	#holds all unfilled board points, stored as x,y pairs
	unfilled = unfilledSpots(board)
	numUnfilled = float(len(unfilled))
	
	#if no new tiles can be added, score of expectiNode is that of identical maxNode
	if numUnfilled == 0:
		return expectimax(board,maxDepth,True)
	
	#weighted average score of expectiNode
	#weighted such that boards where 2's get placed have 9x more weight than boards that placed 4's
	val = 0
	weight = float(1/numUnfilled)
	for coord in unfilled:
		newBoard = np.copy(board)
		addSpecificTile(newBoard,2,coord[0],coord[1])
		val += 0.9*expectimax(newBoard,maxDepth,True)
		newBoard = np.copy(board)
		addSpecificTile(newBoard,4,coord[0],coord[1])
		val += 0.1*expectimax(newBoard,maxDepth,True)
		
	return val*weight


#returns best direction to move the board
#going to change this to use Dynamic Programming, rather than recursive calls
#going to use hash table to hold the score of particular board positions to improve performance
def genius(board):
	unfilled = unfilledSpots(board)
	numUnf = len(unfilled)
	
	#SET MAXDEPTH HERE
	#this needs to be changed
	maxDepth = 3
	if numUnf > 12:
		maxDepth = 1
	elif numUnf > 9:
		maxDepth = 1
	elif numUnf > 5:
		maxDepth = 2
	elif numUnf > 2:
		maxDepth = 2
	
	#don't like this much
	best = -10000
	bestDir = 1
	for moveDir in range(1,5):
		newBoard = np.copy(board)
		if moveDir == 1:
			moveUp(newBoard)
		elif moveDir == 2:
			moveRight(newBoard)
		elif moveDir == 3:
			moveDown(newBoard)
		elif moveDir == 4:
			moveLeft(newBoard)

			
		val = expectimax(newBoard,maxDepth,False)
		if val > best and not(newBoard==board).all():
			best = val
			bestDir = moveDir
			
	if bestDir == 1:
		return moveUp(board)
	elif bestDir == 2:
		return moveRight(board)
	elif bestDir == 3:
		return moveDown(board)
	else:
		return moveLeft(board)

#this method allows you to test the heuristic on an input board
def evaluateHeuristic():
	testboard0 = np.array([[90, 0, 20, 0],
							[80, 0, 0, 0],
							[70, 0, 15, 0],
							[0, 70, 0, 0]])
	testboard1 = np.array([[0, 0, 0, 0],
							[70, 0, 0, 0],
							[80, 80, 0, 0],
							[90, 0, 0, 0]])
	testboard2 = np.array([[0, 0, 40, 50],
							[20, 0, 0, 60],
							[0, 10, 0, 70],
							[0, 0, 20, 90]])
	testboard3 = np.array([[0, 0, 80, 90],
							[0, 0, 0, 0],
							[0, 0, 0, 0],
							[0, 0, 100, 0]])
	for testBoard in [testboard0,testboard1,testboard2,testboard3]:
		print (testBoard)
		print(heuristic(testBoard))




''''
input_var = raw_input("Enter something:")
if input_var == "L":
	print "xxx"
print ("You entered " + input_var)
'''