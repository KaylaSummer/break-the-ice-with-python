# -*- coding: utf-8 -*-
"""
Created on Fri Oct  1 19:21:25 2021

@author: shufan liu
"""

#################################################
# lights-out.py
# Your Name:
# Your AndrewID:
# 
# Groupmate's Names:
# Groupmate's AndrewIDs:
#################################################

#################################################
# LightsOut!
# 
# Write the console-based game "LightsOut!"
# 
# Link to the writeup: https://docs.google.com/document/d/16ggNUsb0_Ddn6RMD2pStw0ZGkjAx8aTaoN4b0buTDII/edit?usp=sharing
# Link to the game: https://www.logicgamesonline.com/lightsout/
#################################################

#################################################
# Printing functions
#################################################

# Prints out the given 2D list input
def print2dList(a):
    if (a == []): print([]); return
    rows, cols = len(a), len(a[0])
    colWidths = [0] * cols
    for col in range(cols):
        colWidths[col] = max([len(str(a[row][col])) for row in range(rows)])
    print('[')
    for row in range(rows):
        print(' [ ', end='')
        for col in range(cols):
            if (col > 0): print(', ', end='')
            print(str(a[row][col]).ljust(colWidths[col]), end='')
        print(' ]')
    print(']')

# Prints out the lightsOut solution for the hardcoded starting configuration 
# as a list of (row, col) tuples 
def printSolution():
    solution = [(0, 0), (0, 1), (0, 3), (0, 4), 
                (1, 2), (1, 3), (2, 1), (2, 3), 
                (2, 4), (3, 2), (3, 3), (4, 0), (4, 1)]

    print("Solution to the board:")
    for elem in solution:
        print(elem)

#################################################
# Gameplay
#################################################

# Initializes the starting configuration of the board
def makeStartingConfiguration():
    boardSize = 5
    board = [[0 for col in range(boardSize)] for row in range(boardSize)]
    board[0][2] = 1
    board[0][3] = 1
    board[1][0] = 1
    board[1][1] = 1
    board[1][4] = 1
    board[2][0] = 1
    board[2][1] = 1
    board[3][0] = 1
    board[3][1] = 1
    board[3][3] = 1
    board[4][3] = 1
    return board

# This function is called to start the game of lightsOut!
#help function:
#this fucntion is used to confirm whether this game is finished.
#we access every element in the board to see whether the number in it is zero
#(the light is out)
def whoIsWin(a):
    for i in range(len(a)):
        for b in range(len(a[0])):
            if a[i][b]==0:
                continue
            else:
                return False
    return True

#This help function helps us to turn out or turn on the light!
def Gameprocess(board,row,col):
    (rows, cols) = (len(board), len(board[0]))
    #we know there will be four directions(up down left and right) nearby the 
    #light  will be effect
    dirs = [           (-1, 0), 
             ( 0, -1),          ( 0, +1),
                      (+1, 0),           ]
    rerow=0
    recol=0
    #first, we need to turn on or turn off the light we choose
    if board[row][col]==0:
        board[row][col]=1
    elif board[row][col]==1:
        board[row][col]=0
    #then in four direction, we choose to if the light is open, we turn it off
    #otherwise, we turn it on
    for i in range(4):
        (drow,dcol) = dirs[i]
        rerow = row + drow
        recol = col + dcol
        #this condition is to make true that when it comes to boundary. This 
        #program would not crash and try next direction
        if ((rerow < 0) or (rerow >= rows) or
            (recol < 0) or (recol >= cols)):
            continue
        else:
            if board[rerow][recol]==0:
                board[rerow][recol]=1
            elif board[rerow][recol]==1:
                board[rerow][recol]=0
    return board
        
        
            
def play():
    board = makeStartingConfiguration()
    print2dList(board)
    (rows, cols) = (len(board), len(board[0]))
    # Write your code here. Feel free to define any helper functions!
    row=0
    col=0
    a=0
    while 1:
    #now we exact people' choice
      row = input('Which row are you going to choose?')
      col =input('Which row are you going to choose?')
      a+=1
      #this condition is to avoide that the input is not integer or the input
      #exceeds the boundary of board.
      if row.isdigit()!=True or col.isdigit(
              )!=True or float(
                  row)-int(row)!=0 or float(col)-int(
                      col)!=0 or int(row)>=rows or int(col)>=cols :
          print('come man, Are you serious?')
      else:
          #if it makes sense, we paly the game
          row=int(row)
          col=int(col)
          board = Gameprocess(board,row,col)
          #untile we finish the game, we do it agian and agian
          if whoIsWin(board)==False:
              #print the game board
              print (print2dList(board))
              #nice message!
              print('nice try!')
          else:
              #once we finsih! We break the loop and send nice message
              print (print2dList(board))
              #this also record how many time you try to finish this game
              print('congratulations! you win!')
              print(f'you have tried {a} times')
              break
print(play())

          
          
          
          
          
         
          


#################################################
# Top-level functions
#################################################

#printSolution()   # uncomment me to print the solution to the starting board!