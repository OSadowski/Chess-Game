"""
User Input
Board Display
"""

import pygame
from Chess import ChessEngine

Width = Height = 512
Dimension = 8
SquareSize = Height // Dimension
Max_FPS = 15
Images = {}


def loadImages():
    pieces = ["wp", "wR", "wN", "wB", "wQ", "wK",
              "bp", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        Images[piece] = pygame.transform.scale(pygame.image.load("images/" + piece + ".png"), (SquareSize, SquareSize))

"""
Main code
Handles user input and updates graphics
"""
def main():
    pygame.init()
    screen = pygame.display.set_mode((Width, Height))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    gameState = ChessEngine.GameState()
    loadImages()
    running = True
    sqSelected = ()  # the last square clicked by user
    playerClicks = []  # keeps track of user clicks
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos()
                col = location[0]//SquareSize
                row = location[1]//SquareSize
                if sqSelected == (row, col):  # if same square clicked twice
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gameState.board)
                    gameState.makeMove(move)
                    print(move.getChessNotation())
                    sqSelected = ()
                    playerClicks = []
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:
                    gameState.undoMove()

        drawGameState(screen, gameState)
        clock.tick(Max_FPS)
        pygame.display.flip()

"""
Updates game board for current game state
"""
def drawGameState(screen, gameState):
    drawBoard(screen)
    drawPieces(screen, gameState.board)

"""
Draws chess board
"""
def drawBoard(screen):
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for row in range(Dimension):
        for column in range(Dimension):
            color = colors[((row+column)%2)]
            pygame.draw.rect(screen, color, pygame.Rect(column*SquareSize, row*SquareSize, SquareSize, SquareSize))

"""
Draws pieces on chess board
"""
def drawPieces(screen, board):
    for row in range(Dimension):
        for column in range(Dimension):
            piece = board[row][column]
            if piece != "--":
                screen.blit(Images[piece], pygame.Rect(column*SquareSize, row*SquareSize, SquareSize, SquareSize))








if __name__ == '__main__':
    main()
