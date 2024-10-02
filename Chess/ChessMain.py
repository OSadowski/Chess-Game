import pygame
from Chess import ChessEngine, ChessAI

Width = Height = 512
MoveLogPanel_Width = 350
MoveLogPanel_Height = Height
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
    screen = pygame.display.set_mode((Width + MoveLogPanel_Width, Height))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    moveLogFont = pygame.font.SysFont("Arial", 12, False, False)
    gameState = ChessEngine.GameState()
    animate = False
    validMoves = gameState.getValidMoves()
    moveMade = False

    loadImages()
    running = True
    sqSelected = ()  # the last square clicked by user
    playerClicks = []  # keeps track of user clicks
    gameOver = False
    humanAsWhite = True
    humanAsBlack = False
    while running:
        isHumanTurn = (gameState.white_to_move and humanAsWhite) or (not gameState.white_to_move and humanAsBlack)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN and not gameOver and isHumanTurn:
                location = pygame.mouse.get_pos()
                col = location[0]//SquareSize
                row = location[1]//SquareSize
                if sqSelected == (row, col) or col >= 8:  # if same square clicked twice
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
                            animate = True
                            sqSelected = ()
                            playerClicks = []
                    if not moveMade:
                        playerClicks = [sqSelected]
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:
                    gameState.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False
                if e.key == pygame.K_r:
                    gameState = ChessEngine.GameState()
                    validMoves = gameState.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False
        #AI Move Logic
        if not gameOver and not isHumanTurn:
            AIMove = ChessAI.findBestMove(gameState, validMoves)
            if AIMove is None:
                AIMove = ChessAI.findRandomMove(validMoves)
            gameState.makeMove(AIMove)
            moveMade = True
            animate = True

        if moveMade:
            if animate:
                animateMove(gameState.move_log[-1], screen, gameState.board, clock)
            validMoves = gameState.getValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gameState, validMoves, sqSelected, moveLogFont)

        if gameState.check_mate or gameState.stale_mate:
            gameOver = True
            if gameState.stale_mate:
                text = "Stalemate"
            else:
                text = "Black wins by Checkmate" if gameState.white_to_move else "White wins by Checkmate"
            drawEndGameText(screen, text)

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
def drawGameState(screen, gameState, validMoves, sqSelected, moveLogFont):
    drawBoard(screen)
    highlightSquares(screen, gameState, validMoves, sqSelected)
    drawPieces(screen, gameState.board)
    drawMoveLog(screen, gameState, moveLogFont)


"""
Draws chess board
"""
def drawBoard(screen):
    global colors
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


def drawMoveLog(screen, gameState, font):
    moveLogRect = pygame.Rect(Width, 0, MoveLogPanel_Width, MoveLogPanel_Height)
    pygame.draw.rect(screen, pygame.Color("black"), moveLogRect)
    moveLog = gameState.move_log
    moveTexts = []
    for i in range(0, len(moveLog), 2):
        moveString = str(i//2 + 1) + ". " + moveLog[i].getChessNotation() + " // "
        if i+1 < len(moveLog):
            moveString += moveLog[i+1].getChessNotation()
        moveTexts.append(moveString)
    padding = 5
    lineSpacing = 2
    textY = padding
    for i in range(len(moveTexts)):
        text = moveTexts[i]
        textObject = font.render(text, True, pygame.Color("white"))
        if i % 2 == 0:
            textLocation = moveLogRect.move(padding, textY)
        else:
            textLocation = moveLogRect.move(padding + MoveLogPanel_Width//2, textY)
            textY += textObject.get_height() + lineSpacing
        screen.blit(textObject, textLocation)

def animateMove(move, screen, board, clock):
    global colors
    dR = move.end_row - move.start_row
    dC = move.end_col - move.start_col
    framesPerSquare = 10
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        row, col = (move.start_row + dR*frame/frameCount, move.start_col +dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.end_row + move.end_col) % 2]
        endSquare = pygame.Rect(move.end_col*SquareSize, move.end_row*SquareSize, SquareSize, SquareSize)
        pygame.draw.rect(screen, color, endSquare)
        if move.piece_captured != "--":
            screen.blit(Images[move.piece_captured], endSquare)
        screen.blit(Images[move.piece_moved], pygame.Rect(col*SquareSize, row*SquareSize, SquareSize, SquareSize))
        pygame.display.flip()
        clock.tick(60)

def drawEndGameText(screen, text):
    font = pygame.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, 0, pygame.Color("Red"))
    textLocation = pygame.Rect(0, 0, Width, Height).move(Width/2 - textObject.get_width()/2, Height/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, pygame.Color("Black"))
    screen.blit(textObject, textLocation.move(2, 2))


if __name__ == '__main__':
    main()
