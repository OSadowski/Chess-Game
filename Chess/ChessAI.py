import random

pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}
checkMateScore = 1000
staleMateScore = 0
Depth = 4

knightBoardScore = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]

bishopBoardScore = [
    [4, 3, 2, 1, 1, 2, 3, 4],
    [3, 4, 3, 2, 2, 3, 4, 3],
    [2, 3, 4, 3, 3, 4, 3, 2],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [1, 2, 3, 4, 4, 3, 2, 1],
    [2, 3, 4, 3, 3, 4, 3, 2],
    [3, 4, 3, 2, 2, 3, 4, 3],
    [4, 3, 2, 1, 1, 2, 3, 4]
]

queenBoardScore = [
    [1, 1, 1, 3, 1, 1, 1, 1],
    [1, 1, 2, 3, 3, 2, 1, 1],
    [1, 4, 3, 3, 3, 4, 3, 1],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [1, 4, 3, 3, 3, 4, 3, 1],
    [1, 2, 3, 3, 3, 3, 2, 1],
    [1, 1, 1, 3, 1, 1, 1, 1]
]

rookBoardScore = [
    [4, 3, 4, 4, 4, 4, 3, 4],
    [3, 4, 4, 4, 4, 4, 4, 3],
    [3, 3, 2, 2, 2, 2, 3, 3],
    [3, 2, 2, 1, 1, 2, 2, 3],
    [3, 2, 2, 1, 1, 2, 2, 3],
    [4, 3, 2, 2, 2, 2, 3, 4],
    [3, 4, 4, 4, 4, 4, 4, 3],
    [4, 3, 4, 4, 4, 4, 3, 4]
]

whitePawnBoardScore = [
    [10, 10, 10, 10, 10, 10, 10, 10],
    [8, 8, 8, 8, 8, 8, 8, 8],
    [3, 3, 3, 3, 3, 3, 3, 3],
    [3, 3, 3, 4, 4, 3, 3, 3],
    [2, 3, 3, 4, 4, 3, 3, 2],
    [2, 2, 2, 3, 3, 2, 2, 2],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]

blackPawnBoardScore = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [2, 2, 2, 3, 3, 2, 2, 2],
    [2, 3, 3, 4, 4, 3, 3, 2],
    [3, 3, 3, 4, 4, 3, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3],
    [8, 8, 8, 8, 8, 8, 8, 8],
    [10, 10, 10, 10, 10, 10, 10, 10]
]

kingBoardScore = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]

piecePositionScores = {"N": knightBoardScore, "Q": queenBoardScore, "R": rookBoardScore, "B": bishopBoardScore,
                       "bp": blackPawnBoardScore, "wp": whitePawnBoardScore, "K": kingBoardScore}


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
    for row in range(len(gameState.board)):
        for col in range(len(gameState.board[row])):
            square = gameState.board[row][col]
            if square != "--":
                if square[1] == "p":
                    piecePositionScore = piecePositionScores[square][row][col]
                else:
                    piecePositionScore = piecePositionScores[square[1]][row][col]

                if square[0] == "w":
                    score += pieceScore[square[1]] + piecePositionScore * .1
                elif square[0] == "b":
                    score -= pieceScore[square[1]] + piecePositionScore * .1
    return score
