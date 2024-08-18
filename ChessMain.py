"""
This is our main driver file. It will be responsible for handling user input and displaying the current GameState
"""
#Import PyGame

import pygame as PyGame
import ChessEngine

WIDTH = HEIGHT = 512 #400 is another option
DIMENSION = 8 #dimensions of a chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 #for animations later on
IMAGES = {}

"""
initialize a global dictonary of images. This will be called exactly once in the main
"""
def loadImages():
    pieces = ['wP','wR','wN','wB','wK','wQ','bP','bR','bN','bB','bK','bQ']
    for piece in pieces:
        IMAGES[piece] = PyGame.transform.scale(PyGame.image.load('images/' + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    #Note we can access an image by saying "IMAGES[wP]"

#This is our main driver it will handle user input and updating graphics

def main():
    PyGame.init()
    screen = PyGame.display.set_mode((WIDTH, HEIGHT))
    clock = PyGame.time.Clock()
    screen.fill(PyGame.Color('white'))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #Flag variable for when a move is made

    loadImages() #only do this once, before the while loop
    running = True
    sqSelected = () #no square is selected initally, keep track of the last click of the user (tuple: (Row, col))
    playerClicks = [] #keep track of player clicks (two tuples: [(6,4),(4,4)])

    while running:
        for e in PyGame.event.get():
            if e.type == PyGame.QUIT:
                running = False
            #mouse handler
            elif e.type == PyGame.MOUSEBUTTONDOWN:
                location = PyGame.mouse.get_pos() #(x,y) location of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col): #the user clicked the same square twice
                    sqSelected = () #deselected
                    playerClicks = [] #clear player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) #append for both 1st and 2nd clicks
                if len(playerClicks) == 2: #after 2nd click
                    move = ChessEngine.Move(playerClicks[0],playerClicks[1],gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected = () # reset user clicks
                    playerClicks = []
            #Key handlers
            elif e.type == PyGame.KEYDOWN:
                if e.key == PyGame.K_z: #Undo when 'z' is pressed
                    gs.undoMove()
                    moveMade = True
                    
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        PyGame.display.flip()
"""
Responsible for all the graphics within a current game state.
"""
def drawGameState(screen, gs):
    drawBoard(screen) #draws squares on the board
    #add in piece highlighting move suggestions
    drawPieces(screen, gs.board) #draw pieces on top of those squares
"""
Draw the squares on the board
Top left square is ALWAYS light
"""
def drawBoard(screen):
    colors = [PyGame.Color("white"),PyGame.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            PyGame.draw.rect(screen, color, PyGame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


"""
Draw the pieces on the board
"""

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #not empty square
                screen.blit(IMAGES[piece], PyGame.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    


if __name__ == "__main__":
    main()