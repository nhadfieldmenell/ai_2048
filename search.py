#run line profiler with kernprof -lv run2048.py

import board2048 as b2048
from board2048 import unfilledSpots, addSpecificTile, heuristic, moveDir as move, trivialHeuristic
import numpy as np
from heapq import heappop as pop, heappush as push
import time
import pdb

#twoSpot is true if the node was created by placing a 2 on the board
#it is false if the node was created by placing a 4 on the board
class Node(object):
	allNodes = {}

	#@profile
	def __init__(self,board,parent=None,direction='D'):
		self.parent = parent
		self.board = board
		self.children2 = {}
		self.children4 = {}
		for a in ['L', 'R', 'D', 'U']:
			self.children2[a] = []
		for a in ['L', 'R', 'D', 'U']:
			self.children4[a] = []
		self.unf = {}
		for a in ['L', 'R', 'D', 'U']:
			self.unf[a] = 0
		self.scores = {}
		for a in ['L', 'R', 'D', 'U']:
			self.scores[a] = 0
		self.score = heuristic(board)
		#self.score = trivialHeuristic(board)
		self.bestDir = 'R'
		self.initialBest = 'R'
		self.moveDir = direction
		self.expanded = False
		key = tuple(board.flatten())
		Node.allNodes[key] = self

	#@profile
	def expand(self):
		if self.expanded:
			return
		self.score = 0
		for direction in ['L','R','D','U']:
			newBoard = np.copy(self.board)
			if not move(newBoard,direction):
				self.scores[direction] = -np.inf
				continue
			unf = unfilledSpots(newBoard)
			self.unf[direction] = float(len(unf))
			weight = float(1/self.unf[direction])
			for spot in unf:
				newerBoard = np.copy(newBoard)
				addSpecificTile(newerBoard,2,spot[0],spot[1])
				newNode = createFunction(newerBoard,self,direction)
				self.scores[direction] += 0.9*weight*newNode.score
				self.children2[direction].append(newNode)
				newerBoard = np.copy(newBoard)
				addSpecificTile(newerBoard,4,spot[0],spot[1])
				newNode = createFunction(newerBoard,self,direction)
				self.scores[direction] += 0.1*weight*newNode.score
				self.children4[direction].append(newNode)
			if self.scores[direction] > self.score:
				self.score = self.scores[direction]
				self.bestDir = direction
		if self.parent:
			self.parent.update()
		self.expanded = True

	#each time that you call update, find the best direction
	def update(self):
		origScore = self.score
		for direction in ['L','R','D','U']:
			self.scores[direction] = 0
			if self.unf[direction]:
				weight = float(1/self.unf[direction])
				for child in self.children2[direction]:
					self.scores[direction] += 0.9*weight*child.score
				for child in self.children4[direction]:
					self.scores[direction] += 0.1*weight*child.score
		self.score = 0
		for i in ['L','R','D','U']:
			if self.scores[i] > self.score:
				self.score = self.scores[i]
				self.bestDir = i
		if self.parent != None and self.score != origScore:
			#print "stopped update"
			self.parent.update()

	def downdate(self):
		bestScore = 0
		bestDir = 'D'


def createFunction(board,*args):
	key = tuple(board.flatten())
	if key in Node.allNodes:
		return Node.allNodes[key]
	else:
		return Node(board,*args)


#@profile
def searchEM(board,nodesToExpand=600):
	startNode = createFunction(board)

	heap = []
	push(heap,(-startNode.score,startNode))
	i = 0
	while i < nodesToExpand:
		start = time.time()
		thisNode = pop(heap)[1]
		if not thisNode.expanded:
			thisNode.expand()
			for a in ['L', 'R', 'D', 'U']:
				for childNode in thisNode.children2[a]:
					push(heap,(-childNode.score,childNode))
				for childNode in thisNode.children4[a]:
					push(heap,(-childNode.score,childNode))
			i += 1
		"""
		else:
			#print (i)
			for a in ['L', 'R', 'D', 'U']:
				for childNode in thisNode.children2[a]:
					push(heap,(-childNode.score,childNode))
				for childNode in thisNode.children4[a]:
					push(heap,(-childNode.score,childNode))
		"""

		#print "time to expand:" , time.time()-start

	Node.allNodes = {}

	#print (startNode.bestDir)
	#pdb.set_trace()
	return move(board,startNode.bestDir)
	#return move(startNode.board,startNode.bestDir)


