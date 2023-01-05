class GameState():
    def __init__(self):

        self.board =  [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        """
        self.board = [
            ["bR", "--", "bB", "bQ", "bR", "--", "bK", "--"],
            ["bp", "bp", "bp", "bN", "--", "bp", "bB", "bp"],
            ["--", "--", "--", "--", "--", "bN", "bp", "--"],
            ["--", "--", "--", "--", "bp", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "wp", "--", "wp", "wN", "--", "wp"],
            ["wp", "wp", "--", "wN", "--", "wp", "wp", "wB"],
            ["wR", "--", "--", "wQ", "wK", "wB", "--", "wR"]]
        """
        self.moveFunctions = {"p": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves,
                              "B": self.getBishopMoves, "Q": self.getQueenMoves, "K": self.getKingMoves}
        self.WhiteToMove = True
        self.movelog = []
        #self.delmove = []
        self.whiteKingLoc = (7, 4)
        self.blackKingLoc = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.epPossible = ()
        self.epPossibleLog = [self.epPossible]
        self.currentCastlingRight = castleRights(True, True, True, True)
        #self.currentCastlingRight = castleRights(True, False, True, False)
        self.castleRightsLog = [castleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]

    def MakeMove(self, move):
        self.board[move.StartRow][move.StartCol] = "--"
        self.board[move.EndRow][move.EndCol] = move.pieceMoved
        self.movelog.append(move)
        self.WhiteToMove = not self.WhiteToMove
        if move.pieceMoved == "wK":
            self.whiteKingLoc = (move.EndRow, move.EndCol)
        elif move.pieceMoved == "bK":
            self.blackKingLoc = (move.EndRow, move.EndCol)
        if move.isPawnPromotion:
            self.board[move.EndRow][move.EndCol] = move.pieceMoved[0] + "Q"
        if move.isEpMove:
            self.board[move.StartRow][move.EndCol] = "--"
        if move.pieceMoved[1] == "p" and abs(move.StartRow- move.EndRow) == 2:
            self.epPossible = ((move.StartRow+move.EndRow)//2, move.EndCol)
        else:
            self.epPossible = ()
        if move.isCastleMove:
            if move.EndCol - move.StartCol == 2:
                self.board[move.EndRow][move.EndCol-1] = self.board[move.EndRow][move.EndCol+1]
                self.board[move.EndRow][move.EndCol+1] = "--"
            else:
                self.board[move.EndRow][move.EndCol + 1] = self.board[move.EndRow][move.EndCol - 2]
                self.board[move.EndRow][move.EndCol - 2] = "--"
        self.epPossibleLog.append(self.epPossible)
        self.updateCastleRights(move)
        self.castleRightsLog.append(castleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))

    def UndoMove(self):
        if len(self.movelog) != 0:
            move = self.movelog.pop()
            self.board[move.EndRow][move.EndCol] = move.pieceCaptured
            self.board[move.StartRow][move.StartCol] = move.pieceMoved
            self.WhiteToMove = not self.WhiteToMove
            if move.pieceMoved == "wK":
                self.whiteKingLoc = (move.StartRow, move.StartCol)
            elif move.pieceMoved == "bK":
                self.blackKingLoc = (move.StartRow, move.StartCol)
            if move.isEpMove:
                self.board[move.EndRow][move.EndCol] = "--"
                self.board[move.StartRow][move.EndCol] = move.pieceCaptured
            self.epPossibleLog.pop()
            self.epPossible = self.epPossibleLog[-1]
            self.castleRightsLog.pop()
            newRights = self.castleRightsLog[-1]
            self.currentCastlingRight = castleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)
            if move.isCastleMove:
                if move.EndCol - move.StartCol == 2:
                    self.board[move.EndRow][move.EndCol + 1] = self.board[move.EndRow][move.EndCol - 1]
                    self.board[move.EndRow][move.EndCol - 1] = "--"
                else:
                    self.board[move.EndRow][move.EndCol - 2] = self.board[move.EndRow][move.EndCol + 1]
                    self.board[move.EndRow][move.EndCol + 1] = "--"
            self.checkmate = False
            self.stalemate = False

    def updateCastleRights(self, move):
        if move.pieceMoved == "wK":
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == "bK":
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        if move.pieceMoved == "wR":
            if move.StartRow == 7:
                if move.StartCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.StartCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceMoved == "bR":
            if move.StartRow == 0:
                if move.StartCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.StartCol == 7:
                    self.currentCastlingRight.bks = False
        if move.pieceCaptured == "wR":
            if move.EndRow == 7:
                if move.EndCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.EndCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceCaptured == "bR":
            if move.EndRow == 0:
                if move.EndCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.EndCol == 7:
                    self.currentCastlingRight.bks = False

    '''
    def RedoMove(self):
        if len(self.delmove) != 0:
            move = self.delmove.pop()
            print (self.delmove)
            self.movelog.append(move)
            self.board[move.EndRow][move.EndCol] = move.pieceMoved
            self.board[move.StartRow][move.StartCol] = "--"
            self.WhiteToMove = not self.WhiteToMove
            if move.pieceMoved == "wK":
                self.whiteKingLoc = (move.EndRow, move.EndCol)
            elif move.pieceMoved == "bK":
                self.blackKingLoc = (move.EndRow, move.EndCol)
    '''

    def GetAllMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == "w" and self.WhiteToMove) or (turn == "b" and not self.WhiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves

    def getPawnMoves(self, r, c, moves):
        if self.WhiteToMove:
            if self.board[r-1][c] == "--":
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == "b":
                    moves.append(Move((r, c), (r - 1, c-1), self.board))
                elif (r-1, c-1) == self.epPossible:
                    moves.append(Move((r, c), (r - 1, c - 1), self.board, isEpMove=True))
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == "b":
                    moves.append(Move((r, c), (r - 1, c+1), self.board))
                elif (r-1, c+1) == self.epPossible:
                    moves.append(Move((r, c), (r - 1, c + 1), self.board, isEpMove=True))
        else:
            if self.board[r+1][c] == "--":
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c-1), self.board))
                elif (r+1, c-1) == self.epPossible:
                    moves.append(Move((r, c), (r + 1, c - 1), self.board, isEpMove=True))
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == "w":
                    moves.append(Move((r, c), (r + 1, c+1), self.board))
                elif (r+1, c+1) == self.epPossible:
                    moves.append(Move((r, c), (r + 1, c + 1), self.board, isEpMove=True))

    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.WhiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break


    def getKnightMoves(self, r, c, moves):
        knightMoves = ((1, -2), (-1, 2), (1, 2), (-1, -2), (2, 1), (-2, -1), (-2, 1), (2, -1))
        allyColor = "w" if self.WhiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))


    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (1, -1), (-1, 1), (1, 1))
        enemyColor = "b" if self.WhiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    def getKingMoves(self, r, c, moves):
        kingMoves = ((0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1))
        allyColor = "w" if self.WhiteToMove else "b"
        for m in kingMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return #dsfhlk
        if (self.WhiteToMove and self.currentCastlingRight.wks) or (not self.WhiteToMove and self.currentCastlingRight.bks):
            self.getKingSideCastleMoves(r, c, moves)
        if (self.WhiteToMove and self.currentCastlingRight.wqs) or (not self.WhiteToMove and self.currentCastlingRight.bqs):
            self.getQueenSideCastleMoves(r, c, moves)

    def getKingSideCastleMoves(self, r, c, moves):
        if self.board[r][c+1] == "--" and self.board[r][c+2] == "--":
            if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
                moves.append(Move((r, c), (r, c+2), self.board, isCastleMove=True))

    def getQueenSideCastleMoves(self, r, c, moves):
        if self.board[r][c - 1] == "--" and self.board[r][c - 2] == "--" and self.board[r][c-3] == "--":
            if not self.squareUnderAttack(r, c - 1) and not self.squareUnderAttack(r, c - 2):
                moves.append(Move((r, c), (r, c - 2), self.board, isCastleMove=True))

    def GetLegalMoves(self):
        tempEpPossible = self.epPossible
        tempCastleRights = castleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks, self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)
        moves = self.GetAllMoves()
        if self.WhiteToMove:
            self.getCastleMoves(self.whiteKingLoc[0], self.whiteKingLoc[1], moves)
        else:
            self.getCastleMoves(self.blackKingLoc[0], self.blackKingLoc[1], moves)
        for i in range(len(moves)-1, -1, -1):
            self.MakeMove(moves[i])
            self.WhiteToMove = not self.WhiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.WhiteToMove = not self.WhiteToMove
            self.UndoMove()
        if len(moves) == 0:
            if self.inCheck():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False
        self.epPossible = tempEpPossible
        self.currentCastlingRight = tempCastleRights
        return moves

    def inCheck(self):
        if self.WhiteToMove:
            return self.squareUnderAttack(self.whiteKingLoc[0], self.whiteKingLoc[1])
        else:
            return self.squareUnderAttack(self.blackKingLoc[0], self.blackKingLoc[1])

    def squareUnderAttack(self, r, c):
        self.WhiteToMove = not self.WhiteToMove
        oppMoves = self.GetAllMoves()
        self.WhiteToMove = not self.WhiteToMove
        for move in oppMoves:
            if move.EndRow == r and move.EndCol == c:
                return True
        return False

class castleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs

class Move():
    RanksToRow = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    RowsToRanks = {v: k for k, v in RanksToRow.items()}
    FilesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    ColsToFiles = {v: k for k, v in FilesToCols.items()}

    def __init__(self, StartSq, EndSq, board, isEpMove = False, isCastleMove = False):
        self.StartRow = StartSq[0]
        self.StartCol = StartSq[1]
        self.EndRow = EndSq[0]
        self.EndCol = EndSq[1]
        self.pieceMoved = board[self.StartRow][self.StartCol]
        self.pieceCaptured = board[self.EndRow][self.EndCol]
        self.isPawnPromotion = ((self.pieceMoved == "wp" and self.EndRow == 0) or (self.pieceMoved == "bp" and self.EndRow == 7))
        self.isEpMove = isEpMove
        if self.isEpMove:
            self.pieceCaptured = "wp" if self.pieceMoved == "bp" else "bp"
        self.isCastleMove = isCastleMove
        self.isCap = self.pieceCaptured != "--"
        self.MoveID = self.StartRow * 1000 + self.StartCol * 100 + self.EndRow * 10 + self.EndCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.MoveID == other.MoveID
        return False

    def GetChessNotation(self):
        return self.GetRankFile(self.StartRow, self.StartCol) + " " + self.GetRankFile(self.EndRow, self.EndCol)
        #Make Actual Notations

    def GetRankFile(self, r, c):
        return self.ColsToFiles[c] + self.RowsToRanks[r]

    def __str__(self):
        if self.isCastleMove:
            return "O-O" if self.EndCol == 6 else "O-O-O"
        endSq = self.GetRankFile(self.EndRow, self.EndCol)
        if self.pieceMoved[1] == "p":
            if self.isCap:
                return self.ColsToFiles[self.StartCol] + "x" + endSq
            else:
                return endSq
            #pawn promo
        #both pieces can move
        #+check
        ##checkmate
        moveString = self.pieceMoved[1]
        if self.isCap:
            moveString += "x"
        return moveString + endSq
