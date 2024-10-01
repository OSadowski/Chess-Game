import random

pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}
checkMateScore = 1000
staleMateScore = 0
Depth = 3


def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]


def findBestMoveMinMax(gameState, validMoves):
    global nextMove
    findMoveMinMax(gameState, validMoves, Depth, gameState.white_to_move)

    return nextMove


def  findMoveMinMax(gameState, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreBoard(gameState)

    if whiteToMove:
        maxScore = -checkMateScore
        for move in validMoves:
            gameState.makeMove(move)
            nextMoves = gameState.getValidMoves()
            score = findMoveMinMax(gameState, nextMoves, depth-1, False)
            if score > maxScore:
                maxScore = score
                if depth == Depth:
                    nextMove = move
            gameState.undoMove()
        return maxScore
    else:
        minScore = checkMateScore
        for move in validMoves:
            gameState.makeMove(move)
            nextMoves = gameState.getValidMoves()
            score = findMoveMinMax(gameState, nextMoves, depth-1, True)
            if score < minScore:
                minScore = score
                if depth == Depth:
                    nextMove = move
            gameState.undoMove()
        return minScore


def scoreBoard(gameState):
    if gameState.check_mate:
        if gameState.white_to_move:
            return -checkMateScore
        else:
            return checkMateScore
    elif gameState.stale_mate:
        return staleMateScore

    score = 0
    for row in gameState.board:
        for square in row:
            if square[0] == "w":
                score += pieceScore[square[1]]
            elif square[0] == "b":
                score += pieceScore[square[1]]
    return score
