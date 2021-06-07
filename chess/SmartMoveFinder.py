import random as r

pieceScore = {'K' : 0, 'Q': 10, 'R' : 5, 'N': 3, 'B': 3, 'p': 1}
CHECKMATE = 1000         # highest score
STALEMATE = 0


def findRandomMoves(validmoves):
    return validmoves[r.randint(0, len(validmoves)-1)]


def findBestMove(gs, validmoves):
    turnMultiplier = 1 if gs.whiteToMove else -1
    opponentMinMaxScore = CHECKMATE
    bestMove = None
    for playerMove in validmoves:
        gs.makeMove(playerMove)
        oppMoves = gs.getValidMoves()
        oppMaxScore = -CHECKMATE
        for move in oppMoves:
            gs.makeMove(move)
            if gs.checkMate :
                score = CHECKMATE
            elif gs.staleMate :
                score = STALEMATE
            else:
                score = turnMultiplier * scorematerial(gs.board)
            if score > opponentMinMaxScore:
                score = opponentMinMaxScore
                bestMove = playerMove
            gs.undoMove()
        gs.undoMove()
    return bestMove
"""
Score the board based on material
"""
def scorematerial(board):
    score = 0
    for row in board:
        for sqaure in row:
            if sqaure[0] == 'w':
                score += pieceScore[sqaure[1]]
            elif sqaure[0] == 'b':
                score -= pieceScore[sqaure[1]]

    return score