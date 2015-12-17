from __future__ import print_function
import sys
import random
import heapq
import numpy as np
sys.setrecursionlimit(100000)

scoreEnd = 0

#score when 0 in snaking pattern
score0 = 3

#score when 1 in snaking pattern
score1 = 6
score2 = 7
score3 = 8
score4 = 9
score5 = 10
score6 = 11
score7 = 12
score8 = 13

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


#the heuristic measures how good a state is
#first checks if it is an end state (want to avoid)
#then it sees if the largest is in a corner
#then it sees for how many in a row down one edge are the values descending
#only next-largest is considered so if 3rd largest is next to the largest
#   that only counts for the largest being in the corner
#return the # of biggest->next biggest->next biggest there is starting from one corner and going along some edge
def heuristic(board):
	if inEndState(board):
		return scoreEnd
	
	h = []
	for x in range(4):
		for y in range(4):
			if board[x,y] != 0:
				heapq.heappush(h,(0-board[x,y]))

	biggest = 0-heapq.heappop(h)

	#This is the case where there is a single tile on the board
	if (len(h) == 0):
		return score1


	#topLeft is true if the biggest one is in the top left corner, etc.
	topLeft = False
	topRight = False
	botLeft = False
	botRight = False
	#True if the largest is in a top corner
	#False if largest is in bottom corner
	top = False
	if board[0,0] == biggest:
		topLeft = True
	elif board[3,0] == biggest:
		topRight = True
	elif board[0,3] == biggest:
		botLeft = True
	elif board[3,3] == biggest:
		botRight = True
	else:
		return score0

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
			return score1
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
			return score1
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
			return score1
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
			return score1

	for i in range(2):
		if (len(h) == 0):
			if i == 0:
				return score2
			else:
				return score3
		biggest = 0-heapq.heappop(h)
		if not xOrY:
			thisX += inc
		else:
			thisY += inc
		if board[thisX,thisY] != biggest:
			if i == 0:
				return score2
			else:
				return score3

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
		if (len(h) == 0):
			if i == 0:
				return score4
			elif i == 1:
				return score5
			elif i == 2:
				return score6
			else:
				return score7
		biggest = 0-heapq.heappop(h)
		if board[thisX,thisY] != biggest:
			if i == 0:
				return score4
			elif i == 1:
				return score5
			elif i == 2:
				return score6
			else:
				return score7
		if not xOrY:
			thisX += inc
		else:
			thisY += inc

	return score8


	
	

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
		for i in range(4):
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
	maxDepth = 2
	if numUnf > 12:
		maxDepth = 1
	elif numUnf > 9:
		maxDepth = 1
	elif numUnf > 5:
		maxDepth = 1
	elif numUnf > 2:
		maxDepth = 1
	
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
	testBoard = [[0 for x in range(4)] for x in range(4)]
	testBoard = np.array(testBoard)
	testBoard[0,0] = 11
	testBoard[0,1] = 11
	testBoard[0,2] = 116
	testBoard[0,3] = 117
	testBoard[1,0] = 11
	testBoard[1,1] = 11
	testBoard[1,2] = 115
	testBoard[1,3] = 118
	testBoard[2,0] = 10
	testBoard[2,1] = 0
	testBoard[2,2] = 0
	testBoard[2,3] = 119
	testBoard[3,0] = 6
	testBoard[3,1] = 0
	testBoard[3,2] = 0
	testBoard[3,3] = 200
	print(heuristic(testBoard))


def heuristicTest(theBoard,count):
	#show board
	for y in range(4):
		print ("+-----+-----+-----+-----+\n|", end = "")
		for x in range(4):
			if theBoard[x,y] == 0:
				print ("     |", end = "")
			elif theBoard[x,y] < 10:
				print(" ", end = " ")
				print(theBoard[x,y], end = "  |")
			elif theBoard[x,y] < 100:
				print (" ", end = "")
				print(theBoard[x,y], end = "  |")
			elif theBoard[x,y] < 1000:
				print (" ", end = "")
				print(theBoard[x,y], end = " |")
			elif theBoard[x,y] < 10000:
				print (" ", end = "")
				print(theBoard[x,y], end = "|")
			elif theBoard[x,y] < 100000:
				print(theBoard[x,y], end = "|")
		print ("\n", end = "")
	print ("+-----+-----+-----+-----+")
	
	if inEndState(theBoard):
		print("        Game Over")
		return
		
	change = genius(theBoard)
	if change != 0:
		addRandomTile(theBoard)
	heuristicTest(theBoard,count+1)
	return

def newTurn(theBoard):
	
	#show board
	for y in range(4):
		print ("+-----+-----+-----+-----+\n|", end = "")
		for x in range(4):
			if theBoard[x,y] == 0:
				print ("     |", end = "")
			elif theBoard[x,y] < 10:
				print(" ", end = " ")
				print(theBoard[x,y], end = "  |")
			elif theBoard[x,y] < 100:
				print (" ", end = "")
				print(theBoard[x,y], end = "  |")
			elif theBoard[x,y] < 1000:
				print (" ", end = "")
				print(theBoard[x,y], end = " |")
			elif theBoard[x,y] < 10000:
				print (" ", end = "")
				print(theBoard[x,y], end = "|")
			elif theBoard[x,y] < 100000:
				print(theBoard[x,y], end = "|")
		print ("\n", end = "")
	print ("+-----+-----+-----+-----+")
		
	change = 0
	if inEndState(theBoard):
		print("        Game Over")
		return
	#userInput = raw_input('Pick a move (a, w, s, d, g for genius, q for quit): ')
	userInput = raw_input('Pick a move (a, w, s, d, q for quit): ')
	if userInput == "a":
		change = moveLeft(theBoard)
	elif userInput == "d":
		change = moveRight(theBoard)
	elif userInput == "w":
		change = moveUp(theBoard)
	elif userInput == "s":
		change = moveDown(theBoard)
	elif userInput == "g":
		change = genius(theBoard)
	elif userInput == "q":
		return
	if change != 0:
		addRandomTile(theBoard)
	newTurn(theBoard)
	return


aBoard = [[0 for x in range(4)] for x in range(4)]
theBoard = np.array(aBoard)
addRandomTile(theBoard)
addRandomTile(theBoard)

evaluateHeuristic()
#heuristicTest(theBoard,0)
#newTurn(theBoard)

''''
input_var = raw_input("Enter something:")
if input_var == "L":
	print "xxx"
print ("You entered " + input_var)
'''