import random

pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}
checkMateScore = 1000
staleMateScore = 0


def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]


def findBestMove(gameState, validMoves):

    turnMultiplier = 1 if gameState.white_to_move else -1
    opponentMinMaxScore = checkMateScore
    bestMove = None
    random.shuffle(validMoves)

    for currentMove in validMoves:
        gameState.makeMove(currentMove)
        opponentsMoves = gameState.getValidMoves()
        opponentsMaxScore = -checkMateScore

        for opponentsMoves in opponentsMoves:
            gameState.makeMove(opponentsMoves)
            if gameState.check_mate:
                score = -turnMultiplier * checkMateScore
            elif gameState.stale_mate:
                score = staleMateScore
            else:
                score = -turnMultiplier * scoreMaterial(gameState.board)
            if score > opponentsMaxScore:
                opponentsMaxScore = score
            gameState.undoMove()
        if opponentsMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentsMaxScore
            bestMove = currentMove
        gameState.undoMove()
    return bestMove


def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == "w":
                score += pieceScore[square[1]]
            elif square[0] == "b":
                score += pieceScore[square[1]]
    return score
