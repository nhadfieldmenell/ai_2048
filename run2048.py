from __future__ import print_function
from search import searchEM
from board2048 import addRandomTile, moveDir, inEndState, heuristic
import numpy as np
import pdb





def heuristicTest(theBoard,count):
	#show board
	#"""
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
	#"""

	if inEndState(theBoard):
		#print("        Game Over")
		print (np.amax(theBoard))
		return
		
	change = searchEM(theBoard)
	#change = genius(theBoard)
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
	interpCmd = {'a': 'L', 'w': 'U', 'd':'R', 's': 'D'}
	if userInput == "g":
		change = searchEM(theBoard)
	elif userInput == "q":
		return
	else:
		change = moveDir(theBoard, interpCmd[userInput])
	if change != 0:
		addRandomTile(theBoard)
	newTurn(theBoard)
	return


aBoard = [[0 for x in range(4)] for x in range(4)]
theBoard = np.array(aBoard)
addRandomTile(theBoard)
addRandomTile(theBoard)

#evaluateHeuristic()
heuristicTest(theBoard,0)
#newTurn(theBoard)