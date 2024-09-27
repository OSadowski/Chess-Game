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

    validMoves = gameState.getValidMoves()
    moveMade = False

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
                    print(move.getChessNotation())
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gameState.makeMove(validMoves[i])
                            moveMade = True
                            sqSelected = ()
                            playerClicks = []
                    if not moveMade:
                        playerClicks = [sqSelected]
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:
                    gameState.undoMove()
                    moveMade = True
        if moveMade:
            validMoves = gameState.getValidMoves()
            moveMade = False

        drawGameState(screen, gameState, validMoves, sqSelected)
        clock.tick(Max_FPS)
        pygame.display.flip()

def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        row, col = sqSelected
        if gs.board[row][col][0] == ("w" if gs.white_to_move else "b"):
            s = pygame.Surface((SquareSize, SquareSize))
            s.set_alpha(100)
            s.fill(pygame.Color("blue"))
            screen.blit(s, (col*SquareSize, row*SquareSize))
            s.fill(pygame.Color("yellow"))
            for move in validMoves:
                if move.start_row == row and move.start_col == col:
                    screen.blit(s, (SquareSize*move.end_col, SquareSize*move.end_row))


"""
Updates game board for current game state
"""
def drawGameState(screen, gameState, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gameState, validMoves, sqSelected)
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
