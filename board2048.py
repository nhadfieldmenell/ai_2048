from __future__ import print_function
import sys
import random
import heapq
import numpy as np
sys.setrecursionlimit(100000)

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
#only next-largest is considered so if 3rd largest is nex to the largest
#   that only counts for the largest being in the corner
#return the # of biggest->next biggest->next biggest there is starting from one corner and going along some edge
def heuristic(board):
	if inEndState(board):
		return -2
	
	#push negative values to maintain 
	#stores 3 tuples [-value,x,y]
	h = []
	for x in range(4):
		for y in range(4):
			if board[x,y] != 0:
				heapq.heappush(h,(0-board[x,y],x,y))
				
	biggest = heapq.heappop(h)
	#True if the largest is in a top corner
	#False if largest is in bottom corner
	top = False
	if biggest[1] == 0:
		top = True
	elif biggest[1] != 3:
		return 0
		
	#true if largest is in a left corner
	#false if largest is in a right corner
	left = False
	if biggest[2] == 0:
		left = True
	elif biggest[2] != 3:
		return 0
	
	#xOrY = {0,1}
	#xOrY = 0: looking for next best along x axis
	#xOrY = 1: looking for next best along y axis
	xOrY = 0
	#now holds the next biggest
	biggest = heapq.heappop(h)
	if top and left:
		if biggest[1] == 1 and biggest[2] == 0:
			xOrY = 0
		elif biggest[1] == 0 and biggest[2] == 1:
			xOrY = 1
		#return 1 since there is still the biggest in a corner
		else:
			return 1
	elif top and not left:
		if biggest[1] == 2 and biggest[2] == 0:
			xOrY = 0
		elif biggest[1] == 3 and biggest[2] == 1:
			xOrY = 1
		#return 1 since there is still the biggest in a corner
		else:
			return 1
	elif left:
		if biggest[1] == 1 and biggest[2] == 3:
			xOrY = 0
		elif biggest[1] == 0 and biggest[2] == 2:
			xOrY = 1
		#return 1 since there is still the biggest in a corner
		else:
			return 1
	else:
		if biggest[1] == 2 and biggest[2] == 3:
			xOrY = 0
		elif biggest[1] == 3 and biggest[2] == 2:
			xOrY = 1
		#return 1 since there is still the biggest in a corner
		else:
			return 1
	
	return 2
	
	nextPos = [0,0]
	for i in range(1,4):
		#now holds the next biggest
		biggest = heapq.heappop(h)
		
			
	
	return 1

#pass in a board, a number of remaining maxNode levels to check 
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
		return expectimax(board,maxDepth,maxNode)
	
	#weighted average score of expectiNode
	#weighted such that boards where 2's get placed have 9x more weight than boards that placed 4's
	val = 0
	weight = 1/numUnfilled
	for coord in unfilled:
		newBoard = np.copy(board)
		addSpecificTile(newBoard,2,coord[0],coord[1])
		val += 0.9*expectimax(newBoard,maxDepth,True)
		newBoard = np.copy(board)
		addSpecificTile(newBoard,4,coord[0],coord[1])
		val += 0.1*expectimax(newBoard,maxDepth,True)
		
	return val


#returns best direction to move the board
def genius(board):
	unfilled = unfilledSpots(board)
	numUnf = len(unfilled)
	
	#SET MAXDEPTH HERE
	#this needs to be changed
	maxDepth = 1
	if numUnf > 12:
		maxDepth = 1
	elif numUnf > 9:
		maxDepth = 1
	elif numUnf > 6:
		maxDepth = 1
	elif numUnf > 2:
		maxDepth = 1
	
	best = 0
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

"""

def maxTile(board):
	max = 0
	for i in range(16):
		if board[i] > max:
			max = board[i]
	return max
def snakeFavor(board,listHeap,corner,dir):
	print("ding")
	favor = 0
	if corner == 1:
		if dir == 4:
			for y in range(2,-1,-1): 
				if board[y] == listHeap.pop():
					favor += 10
				else:
					 return favor
			for y in range(4):
				if board[4+y] == listHeap.pop():
					favor += 10
				else:
					 return favor
			for y in range(3,-1,-1):
				if board(8+y) == listHeap.pop():
					favor += 10
				else:
					 return favor
			for y in range(4):
				if board(12+y) == listHeap.pop():
					favor += 10
				else:
					 return favor
			return favor
		elif dir == 3:
			for x in range(1,4):
				if board[4*x+3] == listHeap.pop():
					favor += 10
				else:
					 return favor
			for x in range(3,-1,-1):
				if board[4*x+2] == listHeap.pop():
					favor += 10
				else:
					 return favor
			for x in range(4):
				if board[4*x+1] == listHeap.pop():
					favor += 10
				else:
					 return favor
			for x in range(3,-1,-1):
				if board[4*x] == listHeap.pop():
					favor += 10
				else:
					 return favor
			return favor
			
	elif corner == 2:
		if dir == 2:
			for y in range(1,4): 
				if board[y] == listHeap.pop():
					favor += 10
				else:
					 return favor
			for y in range(3,-1,-1):
				if board[4+y] == listHeap.pop():
					favor += 10
				else:
					 return favor
			for y in range(4):
				if board(8+y) == listHeap.pop():
					favor += 10
				else:
					 return favor
			for y in range(3,-1,-1):
				if board(12+y) == listHeap.pop():
					favor += 10
				else:
					 return favor
			return favor
		elif dir == 3:
			for x in range(1,4):
				if board[4*x] == listHeap.pop():
					favor += 10
				else:
					 return favor
			for x in range(3,-1,-1):
				if board[4*x+1] == listHeap.pop():
					favor += 10
				else:
					 return favor
			for x in range(4):
				if board[4*x+2] == listHeap.pop():
					favor += 10
				else:
					 return favor
			for x in range(3,-1,-1):
				if board[4*x+3] == listHeap.pop():
					favor += 10
				else:
					 return favor
			return favor
			
	elif corner == 3:
		if dir == 2:
			for y in range(1,4): 
				if board[12+y] == listHeap.pop():
					favor += 10
				else:
					 return favor
			for y in range(3,-1,-1):
				if board[8+y] == listHeap.pop():
					favor += 10
				else:
					 return favor
			for y in range(4):
				if board(4+y) == listHeap.pop():
					favor += 10
				else:
					 return favor
			for y in range(3,-1,-1):
				if board(y) == listHeap.pop():
					favor += 10
				else:
					return favor
			return favor
		elif dir == 1:
			for x in range(2,-1,-1):
				if board[4*x] == listHeap.pop():
					favor += 10
				else:
					 return favor
			for x in range(4):
				if board[4*x+1] == listHeap.pop():
					favor += 10
				else:
					 return favor
			for x in range(3,-1,-1):
				if board[4*x+2] == listHeap.pop():
					favor += 10
				else:
					 return favor
			for x in range(4):
				if board[4*x+3] == listHeap.pop():
					favor += 10
				else:
					 return favor
			return favor
			
	elif corner == 4:
		if dir == 4:
			for y in range(2,-1,-1): 
				if board[y+12] == listHeap.pop():
					favor += 10
				else:
					 return favor
			for y in range(4):
				if board[8+y] == listHeap.pop():
					favor += 10
				else:
					 return favor
			for y in range(3,-1,-1):
				if board(4+y) == listHeap.pop():
					favor += 10
				else:
					 return favor
			for y in range(4):
				if board(y) == listHeap.pop():
					favor += 10
				else:
					 return favor
			return favor
		elif dir == 1:
			for x in range(2,-1,-1):
				if board[4*x+3] == listHeap.pop():
					favor += 10
				else:
					 return favor
			for x in range(4):
				if board[4*x+2] == listHeap.pop():
					favor += 10
				else:
					 return favor
			for x in range(3,-1,-1):
				if board[4*x+1] == listHeap.pop():
					favor += 10
				else:
					 return favor
			for x in range(4):
				if board[4*x] == listHeap.pop():
					favor += 10
				else:
					 return favor
			return favor
	return favor

def heuristic(board):
	favorability = 0
	highest = max(board)
	highestIndexes = []
	for i in range(16):
		if board[i] == highest:
			highestIndexes.append(i)
	corner = 0
	if highestIndexes.count(3):
		corner = 1
	elif highestIndexes.count(0):
		corner = 2
	elif highestIndexes.count(12):
		corner = 3
	elif highestIndexes.count(15):
		corner = 4
		
	if corner != 0:
		favorability += 10
		
	minHeap = []
	for x in range(16):
		heapq.heappush(minHeap,board[x])
		
	listHeap = []
	
	for x in range(16):
		listHeap.append(heapq.heappop(minHeap))
	
	listHeap.pop()
	
	if corner == 1:
		favorability += max(snakeFavor(board,listHeap,1,4),snakeFavor(board,listHeap,1,3))
		
	elif corner == 2:
		favorability += max(snakeFavor(board,listHeap,2,2),snakeFavor(board,listHeap,2,3))
		
	elif corner == 3:
		favorability += max(snakeFavor(board,listHeap,3,1),snakeFavor(board,listHeap,3,2))
		
	elif corner == 4:
		favorability += max(snakeFavor(board,listHeap,4,1),snakeFavor(board,listHeap,4,4))
		
		
		'''
	nextHighest = listHeap.pop()
	
			
	if corner == 1:
		if board[2] == nextHighest:
			corner = 14
			if board[7] == nextHighest:
				corner = 143
		elif board[7] == nextHighest:
			corner = 13
			
	elif corner == 2:
		if board[1] == nextHighest:
			corner = 22
			if board[4] == nextHighest:
				corner = 223
		elif board[4] == nextHighest:
			corner = 23
			
	elif corner == 3:
		if board[8] == nextHighest:
			corner = 31
			if board[13] == nextHighest:
				corner = 312
		elif board[13] == nextHighest:
			corner = 32
			
	elif corner == 4:
		if board[1] == nextHighest:
			corner = 41
			if board[14] == nextHighest:
				corner = 414
		elif board[14] == nextHighest:
			corner = 44
			
	if corner > 10:
		favorability += 20
		
	wouldAdd = 40
	
	return favorability

def genius(theBoard,turn,dir,maxWhenCalled):
	if turn != 0:
		if maxWhenCalled < 50 and turn == 3:
			return 0
		elif maxWhenCalled < 150 and turn == 3:
			return 0
		elif maxWhenCalled < 550 and turn == 4:
			return 0
		elif maxWhenCalled < 2500 and turn == 4:
			return 0
		elif maxWhenCalled >= 2500 and turn == 4:
			return 0
		
	favorability = 0
	
	#optimization because first 2 turns don't matter
	if turn != 0 and turn != 1:
		favorability += heuristic(theBoard)	
		
	newBoard = []
	
	#duplicate the old board
	for i in range(16):
		newBoard.append(theBoard[i])
		
	if dir == 1:
		moveUp(newBoard)
	elif dir == 2:
		moveRight(newBoard)
	elif dir == 3:
		moveDown(newBoard)
	elif dir == 4:
		moveLeft(newBoard)
		
	emptyCount = 0
	emptySpots = []
	for x in range(4):
		for y in range(4):
			loc = [x,y]
			if newBoard[loc] == 0:
				emptySpots.append(loc)
	
	nextFavorability = 0	
	threadCount = 1
	newBoard4 = []
	for i in range(16):
		newBoard4.append(newBoard[i])
	
	if turn != 0:		
		turn += 1		
		for i in emptySpots:
			for x in range(1,5):
				threadCount += 1
				addSpecificTile(newBoard,2,i)
				addSpecificTile(newBoard4,4,i)
				nextFavorability += .1*genius(newBoard4, turn, x,maxWhenCalled)
				nextFavorability += .9*genius(newBoard, turn, x,maxWhenCalled)
			
	nextFavorability = nextFavorability / threadCount
	
	change = 0
	
	if turn == 0:
		theMax = max(theBoard)
		up = genius(theBoard,1,1,theMax)
		right = genius(theBoard,1,2,theMax)
		down = genius(theBoard,1,3,theMax)
		left = genius(theBoard,1,4,theMax)
		if max(up,right,down,left) == up:
			change = moveUp(theBoard)
		if max(right,down,left) == right and change == 0:
			change = moveRight(theBoard)
		if max(down,left) == down and change == 0:
			change = moveDown(theBoard)
		if change == 0:
			change = moveLeft(theBoard)
			if change == 0 and max(up,right,down) == up:
				change = moveUp(theBoard)
			if change == 0 and max(right,down) == right:
				change = moveRight(theBoard)
			if change == 0:
				moveDown(theBoard)
				if change == 0 and max(up,right) == up:
					change = moveUp(theBoard)
				if change == 0:
					change = moveRight(theBoard)
					if change == 0:
						moveUp(theBoard)
		
	if turn == 0:
		return change
	
	return favorability + nextFavorability




def heuristicTest(board,count):
	print(str(count))
	#show board
	for x in range(4):
		print ("+-----+-----+-----+-----+\n|", end = "")
		for y in range(4):
			if board[x,y] == 0:
				print ("     |", end = "")
			elif board[x,y] < 10:
				print(" ", end = " ")
				print(board[x,y], end = "  |")
			elif board[x,y] < 100:
				print (" ", end = "")
				print(board[x,y], end = "  |")
			elif board[x,y] < 1000:
				print (" ", end = "")
				print(board[x,y], end = " |")
			elif board[x,y] < 10000:
				print (" ", end = "")
				print(board[x,y], end = "|")
			elif board[x,y] < 100000:
				print(board[x,y], end = "|")
		print ("\n", end = "")
	print ("+-----+-----+-----+-----+")
	if inEndState(board):
		print ("Highest: " + str(max(board)))
		return
		
	change = genius(board,0,0,0)	
	if change != 0:
		addRandomTile(board)
	heuristicTest(board,count+1)
	return

"""	

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
#heuristicTest(theBoard,0)
newTurn(theBoard)

''''
input_var = raw_input("Enter something:")
if input_var == "L":
	print "xxx"
print ("You entered " + input_var)
'''