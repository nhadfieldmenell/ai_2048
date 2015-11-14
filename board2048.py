import sys
import random
import heapq
sys.setrecursionlimit(100000)

#directions: 1 is up, 2 is right, 3 is down, 4 is left, 0 is nothing
#corners correspond to quadrant

def inEndState(theBoard):
	for i in theBoard:
		if i == 0:
			return False
			
	for i in range(4):
		j = i*4
		if theBoard[j] == 0:
			return False
		if theBoard[j] == theBoard[j+1]:
			return False
		if i != 3:
			for k in range(4):
				if theBoard[j+k] == theBoard[j+k+4]:
					return False
		j = j+2
		if theBoard[j] == theBoard[j-1]:
			return False
		if theBoard[j] == theBoard[j+1]:
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
			if theBoard[4*x+y] == 0:
				emptySpots.append(4*x+y)
				
	if len(emptySpots) == 0:
		return 0
		
	spotToFill = random.randrange(0,len(emptySpots))
	twoOrFour = random.randrange(0,10)
	newTileNum = 2
	if twoOrFour == 9:
		newTileNum = 4
	
	theBoard[emptySpots[spotToFill]] = newTileNum


def moveLeft(theBoard):
	changes = 0
	condensed = []
	for x in range(4):
		for y in range(1,4):	
			currentVal = theBoard[4*x+y]		#currentVal is the one we are moving
			theBoard[4*x+y] = 0
			if currentVal != 0:
				for y2 in range(y-1,-1,-1):
					valAtSpot = theBoard[4*x+y2]
					if valAtSpot != 0:
						if valAtSpot == currentVal and condensed.count(4*x+y2) == 0:
							theBoard[4*x+y2] = 2*valAtSpot
							changes += 1
							condensed.append(4*x+y2)
						else:
							theBoard[4*x+y2+1] = currentVal
							if y2+1 != y:
								changes+= 1
						break
					
					elif y2 == 0:
						theBoard[4*x] = currentVal
						changes += 1
						break		
	return changes


def moveUp(theBoard):
	changes = 0
	condensed = []
	for y in range(4):
		for x in range(1,4):
			currentVal = theBoard[4*x+y]
			theBoard[4*x+y] = 0
			if currentVal != 0:
				for x2 in range(x-1,-1,-1):
					valAtSpot = theBoard[4*x2+y]
					if valAtSpot != 0:
						if valAtSpot == currentVal and condensed.count(4*x2+y) == 0:
							theBoard[4*x2+y] = 2*valAtSpot
							changes += 1
							condensed.append(4*x2+y)
						else:
							theBoard[4*(x2+1)+y] = currentVal
							if x2+1 != x:
								changes += 1
						break
						
					elif x2 == 0:
						theBoard[y] = currentVal
						changes += 1
						break
	return changes


def moveRight(theBoard):
	changes = 0
	condensed = []
	for x in range(4):
		for y in range(2,-1,-1):
			currentVal = theBoard[4*x+y]
			#currentVal = theBoard[x][y]
			#theBoard[x][y] = 0
			theBoard[4*x+y] = 0
			if currentVal != 0:
				for y2 in range(y+1,4):
					#valAtSpot = theBoard[x][y2]
					valAtSpot = theBoard[4*x+y2]
					if valAtSpot != 0:
						if valAtSpot == currentVal and condensed.count(4*x+y2) == 0:
							#theBoard[x][y2] = 2*valAtSpot
							theBoard[4*x+y2] = 2*valAtSpot
							changes += 1
							condensed.append(4*x+y2)
						else:
							#theBoard[x][y2-1] = currentVal
							theBoard[4*x+y2-1] = currentVal
							if y2-1 != y:
								changes += 1
						break
					
					elif y2 == 3:
						#theBoard[x][3] = currentVal
						theBoard[4*x+3] = currentVal
						changes += 1
						break
	return changes


def moveDown(theBoard):
	changes = 0
	condensed = []
	for y in range(4):
		for x in range(2,-1,-1):
			currentVal = theBoard[4*x+y]
			theBoard[4*x+y] = 0
			if currentVal != 0:
				for x2 in range(x+1,4):
					spot = 4*x2+y
					valAtSpot = theBoard[spot]
					if valAtSpot != 0:
						if valAtSpot == currentVal and condensed.count(spot) == 0:
							theBoard[spot] = 2*valAtSpot
							changes += 1
							condensed.append(spot)
						else:
							theBoard[4*(x2-1)+y] = currentVal
							if x2-1 != x:
								changes += 1
						break
						
					elif x2 == 3:
						theBoard[spot] = currentVal
						changes += 1
						break
	return changes


def addSpecificTile(theBoard,val,pos):
	theBoard[pos] = val


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
	'''
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
			loc = 4*x+y
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


def newTurn(theBoard):
	
	#show board
	for x in range(4):
		print ("+-----+-----+-----+-----+\n|", end = "")
		for y in range(4):
			if theBoard[4*x+y] == 0:
				print ("     |", end = "")
			elif theBoard[4*x+y] < 10:
				print(" ", end = " ")
				print(theBoard[4*x+y], end = "  |")
			elif theBoard[4*x+y] < 100:
				print (" ", end = "")
				print(theBoard[4*x+y], end = "  |")
			elif theBoard[4*x+y] < 1000:
				print (" ", end = "")
				print(theBoard[4*x+y], end = " |")
			elif theBoard[4*x+y] < 10000:
				print (" ", end = "")
				print(theBoard[4*x+y], end = "|")
			elif theBoard[4*x+y] < 100000:
				print(theBoard[4*x+y], end = "|")
		print ("\n", end = "")
	print ("+-----+-----+-----+-----+")
		
	change = 0
	if inEndState(theBoard):
		print("        Game Over")
		return
	userInput = input('Pick a move (a, w, s, d, g for genius): ')
	if userInput == "a":
		change = moveLeft(theBoard)
	elif userInput == "d":
		change = moveRight(theBoard)
	elif userInput == "w":
		change = moveUp(theBoard)
	elif userInput == "s":
		change = moveDown(theBoard)
	elif userInput == "g":
		change = genius(theBoard,0,0,0)
	if change != 0:
		addRandomTile(theBoard)
	newTurn(theBoard)
	return


def heuristicTest(board,count):
	print(str(count))
	#show board
	for x in range(4):
		print ("+-----+-----+-----+-----+\n|", end = "")
		for y in range(4):
			if board[4*x+y] == 0:
				print ("     |", end = "")
			elif board[4*x+y] < 10:
				print(" ", end = " ")
				print(board[4*x+y], end = "  |")
			elif board[4*x+y] < 100:
				print (" ", end = "")
				print(board[4*x+y], end = "  |")
			elif board[4*x+y] < 1000:
				print (" ", end = "")
				print(board[4*x+y], end = " |")
			elif board[4*x+y] < 10000:
				print (" ", end = "")
				print(board[4*x+y], end = "|")
			elif board[4*x+y] < 100000:
				print(board[4*x+y], end = "|")
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

	
aBoard = [0 for x in range(16)]
addRandomTile(aBoard)
addRandomTile(aBoard)
#heuristicTest(aBoard,0)
newTurn(aBoard)

''''
input_var = raw_input("Enter something:")
if input_var == "L":
	print "xxx"
print ("You entered " + input_var)
'''