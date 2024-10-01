import random

pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}
checkMateScore = 1000
staleMateScore = 0
Depth = 3


def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]


def findBestMove(gameState, validMoves):
    global nextMove, counter
    nextMove = None
    random.shuffle(validMoves)
    counter = 0
    findMoveNegaMax(gameState, validMoves, Depth, -checkMateScore, checkMateScore, 1 if gameState.white_to_move else -1)
    print(counter)
    return nextMove


def findMoveNegaMax(gameState, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gameState)

    maxScore = -checkMateScore
    for move in validMoves:
        gameState.makeMove(move)
        nextMoves = gameState.getValidMoves()
        score = -findMoveNegaMax(gameState, nextMoves, depth-1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == Depth:
                nextMove = move
        gameState.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore


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
                score -= pieceScore[square[1]]
    return score
