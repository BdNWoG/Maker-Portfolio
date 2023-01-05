import random

pieceScore = {"K": 0, "Q": 900, "R": 500, "B": 315, "N": 300, "p": 100}
CHECKMATE = 100000
STALEMATE = 0
DEPTH = 2 #2 fast 3 ok 4 slow

def findRandomMove(legalMoves):
    return legalMoves[random.randint(0, len(legalMoves)-1)]

def findBestMove(gs, legalMoves):
    turnMultiplier = 1 if gs.WhiteToMove else -1
    oppMinMaxScore = CHECKMATE
    bestPlayerMove = None
    random.shuffle(legalMoves)
    for playerMove in legalMoves:
        gs.MakeMove(playerMove)
        oppMoves = gs.GetLegalMoves()
        if gs.checkmate:
            oppMaxScore = -CHECKMATE
        elif gs.stalemate:
            oppMaxScore = STALEMATE
        else:
            oppMaxScore = -CHECKMATE
        for oppMove in oppMoves:
            gs.MakeMove(oppMove)
            gs.GetLegalMoves()
            if gs.checkmate:
                score = CHECKMATE
            elif gs.stalemate:
                score = STALEMATE
            else:
                score = -turnMultiplier * scoreMaterial(gs.board)
            if score > oppMaxScore:
                oppMaxScore = score
            gs.UndoMove()
        if oppMaxScore < oppMinMaxScore:
            oppMinMaxScore = oppMaxScore
            bestPlayerMove = playerMove
        gs.UndoMove()
    print(scoreMaterial(gs.board))
    return bestPlayerMove

def findBestMoveMinMax(gs, legalMoves):
    global nextMove
    nextMove = None
    random.shuffle(legalMoves)
    findMoveMinMax(gs, legalMoves, DEPTH, gs.WhiteToMove)
    return nextMove

def findMoveMinMax(gs, legalMoves, depth, WhiteToMove):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)
    if WhiteToMove:
        maxScore = -CHECKMATE
        for move in legalMoves:
            gs.MakeMove(move)
            nextMoves = gs.GetLegalMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.UndoMove()
        return maxScore
    else:
        minScore = CHECKMATE
        for move in legalMoves:
            gs.MakeMove(move)
            nextMoves = gs.GetLegalMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.UndoMove()
        return minScore

def findBestMoveNegaMax(gs, legalMoves):
    global nextMove
    nextMove = None
    random.shuffle(legalMoves)
    findMoveNegaMax(gs, legalMoves, DEPTH, 1 if gs.WhiteToMove else -1)
    return nextMove

def findBestMoveNegaMaxAB(gs, legalMoves):
    global nextMove
    nextMove = None
    random.shuffle(legalMoves)
    findMoveNegaMaxAB(gs, legalMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.WhiteToMove else -1)
    return nextMove

def findMoveNegaMax(gs, legalMoves, depth, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    maxScore = -CHECKMATE
    for move in legalMoves:
        gs.MakeMove(move)
        nextMoves = gs.GetLegalMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth - 1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.UndoMove()
    return maxScore

def findMoveNegaMaxAB(gs, legalMoves, depth, alpha, beta, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    maxScore = -CHECKMATE
    for move in legalMoves:
        gs.MakeMove(move)
        nextMoves = gs.GetLegalMoves()
        score = -findMoveNegaMaxAB(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.UndoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore

def scoreBoard(gs):
    if gs.checkmate:
        if gs.WhiteToMove:
            return -CHECKMATE
        else:
            return  CHECKMATE
    elif gs.stalemate:
        return 0
    else:
        score = 0
        for row in gs.board:
            for square in row:
                if square[0] == "w":
                    score += pieceScore[square[1]]
                elif square[0] == "b":
                    score -= pieceScore[square[1]]
        return score

def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            i = board.index(row)
            j = row.index(square)
            if square[0] == "w":
                score += pieceScore[square[1]]
            elif square[0] == "b":
                score -= pieceScore[square[1]]
                #slight change
            if board[i][j][1] == "p":
                if square[0] == "w":
                    score += (7 - i) * 3 * (50 - (7 - abs(3.5 - j)**3))/50
                elif square[0] == "b":
                    score -= i * 3 * (50 - (7 - abs(3.5 - j)**3))/50
            elif board[i][j][1] == "N":
                if square[0] == "w":
                    score += ((7 - abs(3.5 - i)) + (7 - abs(3.5 - j))) * 2
                elif square[0] == "b":
                    score -= ((7 - abs(3.5 - i)) + (7 - abs(3.5 - j))) * 2
            #change
            elif board[i][j][1] == "B":
                if square[0] == "w":
                    score += ((7 - abs(3.5 - i)) + (7 - abs(3.5 - j))) * 2
                elif square[0] == "b":
                    score -= ((7 - abs(3.5 - i)) + (7 - abs(3.5 - j))) * 2
            elif board[i][j][1] == "Q":
                if square[0] == "w":
                    score += ((7 - abs(3.5 - i)) + (7 - abs(3.5 - j))) * 4
                elif square[0] == "b":
                    score -= ((7 - abs(3.5 - i)) + (7 - abs(3.5 - j))) * 4
            #change
            elif board[i][j][1] == "R":
                if square[0] == "w":
                    score += (7 - abs(3.5 - j)) * 1.5
                elif square[0] == "b":
                    score -= (7 - abs(3.5 - j)) * 1.5
            elif board[i][j][1] == "K":
                if square[0] == "w":
                    if i == 7 and j == 6:
                        score += 20
                    elif i == 7 and j == 2:
                        score += 15
                elif square[0] == "b":
                    if i == 0 and j == 6:
                        score -= 20
                    elif i == 0 and j == 2:
                        score -= 15
    """           
    for i in range(0, len(board)-1):
        for j in range(0, len(board-1)):
            if board[i][j][1] == "p":
                if square[0] == "w":
                    score += ((8-i) * 3 + (8-int(round(abs(3.5-j))))) / 3
                elif square[0] == "b":
                    score -= ((i+1) * 3 + (8-int(round(abs(3.5-j))))) / 3
    """
    return score

#import opening