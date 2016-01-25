#run line profiler with kernprof -lv run2048.py
#to debug: python -i search.py 
#					pdb.pm when the error is thrown

import board2048 as b2048
from board2048 import Board
import numpy as np
from heapq import heappop as pop, heappush as push
import time
import pdb
import gc




#twoSpot is true if the node was created by placing a 2 on the board
#it is false if the node was created by placing a 4 on the board
class Node(object):
	allNodes = {}
	_downdateCache = {}

	#@profile
	def __init__(self,board,parent=None,direction='D'):
		self.parent = parent
		self.board = board
		self.children = {}
		for a in ['L', 'R', 'D', 'U']:
			self.children[a] = []
		self.scores = {}
		for a in ['L', 'R', 'D', 'U']:
			self.scores[a] = 0
		self.score = board.heuristic()
		self.bestDir = 'R'
		self.initialBest = 'R'
		self.moveDir = direction
		self.expanded = False
		Node.allNodes[board.key] = self

	
	#@profile
	def expand(self):
		if self.expanded:
			return
		self.score = 0
		for direction in ['L','R','D','U']:
			boardChildren = self.board.getChildren(direction)
			for childBoard,pChild in boardChildren:
				childNode = createFunction(childBoard,self,direction)
				self.children[direction].append((childNode,pChild))
		#self.update()
		self.expanded = True



	#each time that you call update, find the best direction
	def update(self):
		origScore = self.score
		for direction in ['L','R','D','U']:
			self.scores[direction] = 0
			if len(self.children[direction]) == 0:
				self.scores[direction] = -np.inf
			else:	
				for child,pChild in self.children[direction]:
					self.scores[direction] += child.score*pChild
		self.score = -np.inf
		for i in ['L','R','D','U']:
			if self.scores[i] > self.score:
				self.score = self.scores[i]
				self.bestDir = i
		if self.parent != None and self.score != origScore:
			#print "stopped update"
			self.parent.update()

	def downdate(self,firstCall = True):
		if firstCall:
			Node._downdateCache = {}
		if self in Node._downdateCache:
			return self.score
		if not self.expanded:
			Node._downdateCache[self] = self.score
			return self.score
		
		for direction in ['L','R','D','U']:
			self.scores[direction] = 0
			if len(self.children[direction]) == 0:
				self.scores[direction] = -np.inf
			else:	
				for child,pChild in self.children[direction]:
					self.scores[direction] += child.downdate(False)*pChild

		self.score = -np.inf
		for i in ['L','R','D','U']:
			if self.scores[i] > self.score:
				self.score = self.scores[i]
				self.bestDir = i

		Node._downdateCache[self] = self.score
		return self.score

	def __hash__(self):
		return hash(self.board)


def createFunction(board,*args):
	key = board.key
	if key in Node.allNodes:
		return Node.allNodes[key]
	else:
		return Node(board,*args)


#@profile
def searchEM(board,nodesToExpand=3000):
	startNode = createFunction(board)

	heap = []
	push(heap,(-startNode.score,startNode))
	i = 0
	while i < nodesToExpand:
		start = time.time()
		if len(heap) == 0:
			break
		thisNode = pop(heap)[1]
		if not thisNode.expanded:
			thisNode.expand()
			for a in ['L', 'R', 'D', 'U']:
				for childNode,_ in thisNode.children[a]:
					push(heap,(-childNode.score,childNode))
			i += 1

		#print "time to expand:" , time.time()-start

	Node.allNodes = {}

	#print (startNode.bestDir)
	#pdb.set_trace()
	startNode.downdate()
	return board.move(startNode.bestDir)
	#return move(startNode.board,startNode.bestDir)


