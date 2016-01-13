from __future__ import print_function
import sys, random, heapq, copy
import numpy as np
from collections import defaultdict

allPositions = [(x,y) for x in range(4) for y in range(4)]

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

_hcache = {}

class Board(object):
	def __init__(self,copyBoard = None):
		if (copyBoard == None):
			self.board = np.zeros((4,4),dtype = np.int)
			self.key = tuple(self.board.flatten())
			self.num2pos = defaultdict(list)
			self.num2pos[0] = copy.copy(allPositions)
			tile0 = self.addRandomTile()
			tile1 = self.addRandomTile()
			self.largest = max(tile0,tile1)


		else:
			self.largest = copyBoard.largest
			self.board = copyBoard.board.copy()
			self.key = copyBoard.key
			self.num2pos = defaultdict(list)
			for pos in allPositions:
				self.num2pos[self.board[pos]].append(pos)


	def setVal(self,x,y,val):
		currentVal = self.board[x,y]
		self.num2pos[currentVal].remove((x,y))
		self.num2pos[val].append((x,y))
		self.board[x,y] = val
		self.key = tuple(self.board.flatten())
		return currentVal
	
	#return list of (child board, probability of that boards)
	def getChildren(self,direction):
		movedBoard = Board(self)
		if not movedBoard.move(direction):
			return []
		childList = []
		weight = 1/float(len(movedBoard.num2pos[0]))
		for x,y in movedBoard.num2pos[0]:
			newBoard = Board(movedBoard)
			newBoard.setVal(x,y,2)
			childList.append((newBoard,0.9*weight))
			newBoard = Board(movedBoard)
			newBoard.setVal(x,y,4)
			childList.append((newBoard,0.1*weight))
		return childList
			

	def testSnake(self):
		self.board = np.zeros((4,4),dtype = np.int)
		self.num2pos[0] = copy.copy(allPositions)
		self.num2pos[2] = []
		self.num2pos[4] = []
		self.setVal(0,3,128)
		print (self.board)
		print (self.heuristic())
		snake,secondary,biggest = self.getSnake()
		print (str(snake) + "," + str(secondary) + "," + str(biggest))
		print (self.scoreOutsideSnake(snake,secondary))
		self.setVal(0,2,64)
		print (self.board)
		print (self.heuristic())
		snake,secondary,biggest = self.getSnake()
		print (str(snake) + "," + str(secondary) + "," + str(biggest))
		print (self.scoreOutsideSnake(snake,secondary))
		self.setVal(0,1,16)
		print (self.board)
		print (self.heuristic())
		snake,secondary,biggest = self.getSnake()
		print (str(snake) + "," + str(secondary) + "," + str(biggest))
		print (self.scoreOutsideSnake(snake,secondary))
		self.setVal(0,0,8)
		print (self.board)
		print (self.heuristic())
		snake,secondary,biggest = self.getSnake()
		print (str(snake) + "," + str(secondary) + "," + str(biggest))
		print (self.scoreOutsideSnake(snake,secondary))
		self.setVal(1,3,32)
		print (self.board)
		print (self.heuristic())
		snake,secondary,biggest = self.getSnake()
		print (str(snake) + "," + str(secondary) + "," + str(biggest))
		print (self.scoreOutsideSnake(snake,secondary))
		self.setVal(1,3,2)
		print (self.board)
		print (self.heuristic())
		snake,secondary,biggest = self.getSnake()
		print (str(snake) + "," + str(secondary) + "," + str(biggest))
		print (self.scoreOutsideSnake(snake,secondary))
		self.setVal(1,1,4)
		print (self.board)
		print (self.heuristic())
		snake,secondary,biggest = self.getSnake()
		print (str(snake) + "," + str(secondary) + "," + str(biggest))
		print (self.scoreOutsideSnake(snake,secondary))
		self.setVal(1,0,4)
		print (self.board)
		print (self.heuristic())
		snake,secondary,biggest = self.getSnake()
		print (str(snake) + "," + str(secondary) + "," + str(biggest))
		print (self.scoreOutsideSnake(snake,secondary))
		self.setVal(2,0,64)
		print (self.board)
		print (self.getSnake())
		snake,secondary,biggest = self.getSnake()
		print (str(snake) + "," + str(secondary) + "," + str(biggest))
		print (self.scoreOutsideSnake(snake,secondary))
		"""
		newBoard = Board(self)
		print (self.board)
		print (self.num2pos)
		print (newBoard.board)
		print (newBoard.num2pos)
		newBoard.setVal(3,3,2048)
		print (self.board)
		print (self.num2pos)
		print (newBoard.board)
		print (newBoard.num2pos)
		"""



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
		twoOrFour = random.randrange(0,10)
		newTileNum = 2
		if twoOrFour == 9:
			newTileNum = 4
		#print(self.num2pos)
		self.setVal(x,y,newTileNum)
		return newTileNum

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
		#print (self.num2pos)
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
				#print ("(" + str() + str(currentVal))
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
								else:
									self.setVal(minor,major1,2*valAtSpot)
								self.largest = max(self.largest,2*valAtSpot)
								changes += 1
								condensed[major1] = 1
							else:
								if not XorY:
									self.setVal(major1+inc,minor,currentVal)
								else:
									self.setVal(minor,major1+inc,currentVal)
							if major1+inc != major0:
								changes += 1
							break
						elif major1 == majorDone:
							if not XorY:
								#print (str(minor) + str(major1))
								self.setVal(majorDone,minor,currentVal)
								changes += 1
								break
							else:
								#print (str(minor) + str(major1))
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

	def __hash__(self):
		return hash(self.key)

	def theBiggest(self):
		biggest = 65536

	
	def getSnake(self):
		biggest = 65536
		biggest,biggestCount = self.findNextBiggest(biggest,0)

		snakeList = []
		secondarySnake = []

		#topLeft is true if the biggest one is in the top left corner, etc.
		topLeft = False
		topRight = False
		botLeft = False
		botRight = False
		if self.board[0,0] == biggest:
			snakeList.append((0,0))
			topLeft = True
		elif self.board[3,0] == biggest:
			snakeList.append((3,0))
			topRight = True
		elif self.board[0,3] == biggest:
			snakeList.append((0,3))
			botLeft = True
		elif self.board[3,3] == biggest:
			snakeList.append((3,3))
			botRight = True
		else:
			return snakeList,secondarySnake,biggest

		#xOrY = {0,1}
		#xOrY = 0: looking for next best along x axis
		#xOrY = 1: looking for next best along y axis
		xOrY = 0

		#1 if moving left->right or up->down, -1 otherwise
		inc = 1

		biggest,biggestCount = self.findNextBiggest(biggest,biggestCount)

		#holds the position of the previous spot in the snaking pattern
		thisX = 0
		thisY = 0

		snakeBroken = False
		lastTile = 0

		if topLeft:
			if self.board[1,0] == biggest:
				thisX,thisY,xOrY = 1,0,0
				snakeList.append((1,0))
			elif self.board[0,1] == biggest:
				snakeList.append((0,1))
				thisX,thisY,xOrY = 0,1,1
			elif self.board[1,0] > self.board[0,1]:
				thisX,thisY,xOrY = 1,0,0
				snakeBroken = True
				secondarySnake.append((1,0))
				lastTile = self.board[1,0]
			else:
				secondarySnake.append((0,1))
				thisX,thisY,xOrY = 0,1,1
				snakeBroken = True
				lastTile = self.board[1,1]
		elif topRight:
			if self.board[2,0] == biggest:
				snakeList.append((2,0))
				thisX,thisY,xOrY,inc = 2,0,0,-1
			elif self.board[3,1] == biggest:
				snakeList.append((3,1))
				thisX,thisY,xOrY = 3,1,1
			elif self.board[2,0] > self.board[3,1]:
				secondarySnake.append((2,0))
				thisX,thisY,xOrY,inc = 2,0,0,-1
				snakeBroken = True
				lastTile = self.board[2,0]
			else:
				secondarySnake.append((3,1))
				thisX,thisY,xOrY = 3,1,1
				snakeBroken = True
				lastTile = self.board[3,1]
		elif botLeft:
			if self.board[1,3] == biggest:
				thisX,thisY,xOrY = 1,3,0
				snakeList.append((1,3))
			elif self.board[0,2] == biggest:
				snakeList.append((0,2))
				thisX,thisY,xOrY,inc = 0,2,1,-1
			elif self.board[1,3] > self.board[0,2]:
				snakeBroken = True
				thisX,thisY,xOrY = 1,3,0
				secondarySnake.append((1,3))
				lastTile = self.board[1,3]
			else:
				snakeBroken = True
				secondarySnake.append((0,2))
				thisX,thisY,xOrY,inc = 0,2,1,-1
				lastTile = self.board[0,2]
		elif botRight:
			if self.board[2,3] == biggest:
				snakeList.append((2,3))
				thisX,thisY,xOrY,inc = 2,3,0,-1
			elif self.board[3,2] == biggest:
				snakeList.append((3,2))
				thisX,thisY,xOrY,inc = 3,2,1,-1
			elif self.board[2,3] > self.board[3,2]:
				snakeBroken = True
				secondarySnake.append((2,3))
				thisX,thisY,xOrY,inc = 2,3,0,-1
				lastTile = self.board[2,3]
			else:
				snakeBroken = True
				snakeList.append((3,2))
				thisX,thisY,xOrY,inc = 3,2,1,-1
				lastTile = self.board[3,2]
		else:
			return snakeList,secondarySnake,biggest
		
		for i in range(2):
			if not snakeBroken:
				if self.findNextBiggest(biggest,biggestCount)[0] == 0:
					return snakeList,secondarySnake,biggest
				biggest,biggestCount = self.findNextBiggest(biggest,biggestCount)
				if not xOrY:
					thisX += inc
				else:
					thisY += inc
				if self.board[thisX,thisY] != biggest:
					snakeBroken = True
					lastTile = self.board[thisX,thisY]
					secondarySnake.append((thisX,thisY))
				else:
					snakeList.append((thisX,thisY))
			else:
				if not xOrY:
					thisX += inc
				else:
					thisY += inc
				if self.board[thisX,thisY] == 0:
					return snakeList,secondarySnake,biggest
				if self.board[thisX,thisY] <= lastTile:
					lastTile = self.board[thisX,thisY]
					secondarySnake.append((thisX,thisY))
				else:
					return snakeList,secondarySnake,biggest

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

			if not snakeBroken:
				biggest,biggestCount = self.findNextBiggest(biggest,biggestCount)
				if biggest == 0:
					return snakeList,secondarySnake,biggest

				if self.board[thisX,thisY] != biggest:
					snakeBroken = True
					secondarySnake.append((thisX,thisY))
				else:
					snakeList.append((thisX,thisY))
				if not xOrY:
					thisX += inc
				else:
					thisY += inc
			else:
				if self.board[thisX,thisY] == 0:
					return snakeList,secondarySnake,biggest
				if self.board[thisX,thisY] <= lastTile:
					lastTile = self.board[thisX,thisY]
					secondarySnake.append((thisX,thisY))
				else:
					return snakeList,secondarySnake,biggest
				if not xOrY:
					thisX += inc
				else:
					thisY += inc

		biggest,biggestCount = self.findNextBiggest(biggest,biggestCount)
		return snakeList,secondarySnake,biggest

	def scoreOutsideSnake(self,snake,secondary):
		nodes = copy.copy(allPositions)
		for i in snake: nodes.remove(i)
		for i in secondary: nodes.remove(i)
		scoreOut = 0
		for i in nodes: scoreOut += self.board[i]
		return scoreOut

	#@profile
	def heuristic(self):
		#if self.key in _hcache:
		#	return _hcache[self.key]

		biggest = 65536
		biggest,biggestCount = self.findNextBiggest(biggest,0)

		if self.inEndState():
		#	_hcache[self.key] = -biggest
			return -biggest*2
		
		
		if self.findNextBiggest(biggest,biggestCount)[0] == 0:
		#	_hcache[self.key] = score1
			return biggest

		snake,secondarySnake,biggestOut = self.getSnake()
		snakeScore = 0
		for point in snake:
			snakeScore += self.board[point]

		secondaryScore = 0
		for point in secondarySnake:
			secondaryScore += self.board[point]

		snakeWeight = 0.5
		unfilledWeight = 0.05
		secondaryWeight = 1.0-snakeWeight-unfilledWeight

		adjustedUnfilled = len(self.num2pos[0])*self.largest

		totalScore = snakeWeight*snakeScore + secondaryWeight*secondaryScore + unfilledWeight*len(self.num2pos[0])

		penaltyWeight = 0.2
		totalScore -= penaltyWeight*biggestOut


		#_hcache[self.key] = totalScore
		return totalScore

		
		

	#pass in the one that was the previous biggest
	#must get a power of 2 as a value
	#returns the value and the number of instances of that value
	def findNextBiggest(self,val,biggestCount):
		biggestCount -= 1
		if biggestCount > 0:
			return val,biggestCount
		val /= 2
		while len(self.num2pos[val]) == 0:
			val /= 2
		if val == 1:
			return 0,len(self.num2pos[0])
		return val,len(self.num2pos[val])
		