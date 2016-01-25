from __future__ import print_function
from search import searchEM
from board2048 import Board
import numpy as np
import pdb, sys
sys.setrecursionlimit(100000)





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
		with open('bestScores.txt','a') as f: f.write(str(np.amax(theBoard)) + "\n")
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

def geniusGame():
	board = Board()
	while True:
		board.printBoard()
		if board.inEndState():
			print("        Game Over")
			with open('bestScores.txt','a') as f: f.write("10000: " + str(np.amax(board.board)) + "\n")
			return
		change = searchEM(board)
		if change != 0:
			board.addRandomTile()
		


#aBoard = [[0 for x in range(4)] for x in range(4)]
#theBoard = np.array(aBoard)
#addRandomTile(theBoard)
#addRandomTile(theBoard)
#heuristicTest(theBoard,0)

#evaluateHeuristic()


#board.testSnake()

correctInput = False
while not correctInput:
	userInput = raw_input('Would you like to play (enter "p") or watch the ai play (enter "ai")?\n')
	if userInput == "p":
		correctInput = True
		board = Board()
		board.newTurn()
	elif userInput == "ai":
		correctInput = True
		for i in range(5): geniusGame()

"""
with open('bestScores.txt','w') as f: f.write("Scores:\n")
for i in range(25):
	aBoard = [[0 for x in range(4)] for x in range(4)]
	theBoard = np.array(aBoard)
	addRandomTile(theBoard)
	addRandomTile(theBoard)
	heuristicTest(theBoard,0)
"""

	
#newTurn(theBoard)