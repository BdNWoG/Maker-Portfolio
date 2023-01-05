import pygame as p
import ChessEngine, ChessAI
from playsound import playsound

board_width = board_height = 768
panel_width = 384
panel_height = board_height
dimension = 8
sq_size = board_height // dimension
max_fps = 15
images = {}

def loadImages():
    pieces = ["wp", "wR", "wN", "wB", "wQ", "wK", "bp", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("Images/" + piece + ".png") ,(sq_size, sq_size))

def main():
    p.init()
    p.display.set_caption('Chess')
    screen = p.display.set_mode((board_width + panel_width, board_height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    moveLogFont = p.font.SysFont("times new roman", 22, False, False)
    gs = ChessEngine.GameState()
    legalMoves = gs.GetLegalMoves()
    moveMade = False
    animate = False
    loadImages()
    SqSelected = ()
    PlayerClicks = []
    running = True
    gameover = False
    playerOne = True
    playerTwo = False
    while running:
        humanTurn = (gs.WhiteToMove and playerOne) or (not gs.WhiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameover and humanTurn:
                    location = p.mouse.get_pos()
                    col = location[0]//sq_size
                    row = location[1]//sq_size
                    if SqSelected == (row, col) or col >= 8:
                        SqSelected = ()
                        PlayerClicks = []
                    else:
                        SqSelected = (row, col)
                        PlayerClicks.append(SqSelected)
                    if len(PlayerClicks) == 2:
                        move = ChessEngine.Move(PlayerClicks[0], PlayerClicks[1], gs.board)
                        for i in range(len(legalMoves)):
                            if move == legalMoves[i]:
                                gs.MakeMove(legalMoves[i])
                                print(move.GetChessNotation())
                                playsound("sound.mp3")
                                moveMade = True
                                animate = True
                                SqSelected = ()
                                PlayerClicks = []
                        if not moveMade:
                            PlayerClicks = [SqSelected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_LEFT:
                    gs.UndoMove()
                    moveMade = True
                    animate = False
                    gameover = False
                if e.key == p.K_SPACE:
                    gs = ChessEngine.GameState()
                    legalMoves = gs.GetLegalMoves()
                    SqSelected = ()
                    PlayerClicks = []
                    moveMade = False
                    animate = False
                    gameover = False
                '''
                elif e.key == p.K_RIGHT:
                    gs.RedoMove()
                    moveMade = True
                '''
        if not gameover and not humanTurn:
            print(ChessAI.scoreBoard(gs))
            AIMove = ChessAI.findBestMoveNegaMaxAB(gs, legalMoves)
            if AIMove is None:
                AIMove = ChessAI.findRandomMove(legalMoves)
            gs.MakeMove(AIMove)
            print(ChessAI.scoreBoard(gs))
            print(AIMove.GetChessNotation())
            playsound("sound.mp3")
            moveMade = True
            animate = True

        if moveMade:
            if animate:
                animateMove(gs.movelog[-1], screen, gs.board, clock)
            legalMoves = gs.GetLegalMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gs, legalMoves, SqSelected, moveLogFont)
        if gs.checkmate or gs.stalemate:
            gameover = True
            drawEndGameText(screen, "Stalemate" if gs.stalemate else "Black wins by Checkmate" if gs.WhiteToMove else "White wins by Checkmate")
        clock.tick(max_fps)
        p.display.flip()

def drawGameState(screen, gs, legalMoves, SqSelected, moveLogFont):
    drawBoard(screen)
    highlightSquares(screen, gs, legalMoves, SqSelected)
    drawPieces(screen, gs.board)
    drawMoveLog(screen, gs, moveLogFont)

def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("grey")]
    for r in range(dimension):
        for c in range(dimension):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))

def highlightSquares(screen, gs, legalMoves, SqSelected):
    if SqSelected != ():
        r, c = SqSelected
        if gs.board[r][c][0] == ("w" if gs.WhiteToMove else "b"):
            s = p.Surface((sq_size, sq_size))
            s.set_alpha(100)
            s.fill(p.Color("blue"))
            screen.blit(s, (c*sq_size, r*sq_size))
            s.fill(p.Color("yellow"))
            for move in legalMoves:
                if move.StartRow == r and move.StartCol == c:
                    screen.blit(s, (move.EndCol*sq_size, move.EndRow*sq_size))

def drawPieces(screen, board):
    for r in range(dimension):
        for c in range(dimension):
            piece = board[r][c]
            if piece != "--":
                screen.blit(images[piece], p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))

def drawMoveLog(screen, gs, font):
    moveLogRect = p.Rect(board_width, 0, panel_width, panel_height)
    p.draw.rect(screen, p.Color("Black"), moveLogRect)
    moveLog = gs.movelog
    moveText = []
    for i in range(0, len(moveLog), 2):
        moveString = str(i//2 + 1) + ". " + str(moveLog[i]) + "     "
        if i + 1 < len(moveLog):
            moveString += str(moveLog[i+1])
        moveText.append(moveString)
    movePerRow = 2
    padding = 10
    textY = padding
    lineSpace = 5
    for i in range(0, len(moveText), movePerRow):
        text = ""
        for j in range(movePerRow):
            if j != 0:
                text += "         "
            if i+j < len(moveText):
                text += moveText[i+j]
        textObject = font.render(text, True, p.Color("white"))
        textLocation = moveLogRect.move(padding*2, textY*1.5)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpace

def animateMove(move, screen, board, clock):
    global colors
    dr = move.EndRow - move.StartRow
    dc = move.EndCol - move.StartCol
    framesPerSquare = 5
    frameCount = int(round(abs(dr)**2 + abs(dc)**2)**0.5) * framesPerSquare
    for frame in range (frameCount+1):
        r, c = ((move.StartRow + dr*frame/frameCount, move.StartCol + dc*frame/frameCount))
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.EndRow + move.EndCol) % 2]
        endSquare = p.Rect(move.EndCol*sq_size, move.EndRow*sq_size, sq_size, sq_size)
        p.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != "--":
            if move.isEpMove:
                epRow = move.EndRow + 1 if move.pieceCaptured[0]  == "b" else move.EndRow - 1
                endSquare = p.Rect(move.EndCol*sq_size, epRow*sq_size, sq_size, sq_size)
            screen.blit(images[move.pieceCaptured], endSquare)
        screen.blit(images[move.pieceMoved], p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))
        p.display.flip()
        clock.tick(60)

def drawEndGameText(screen, text):
    font = p.font.SysFont("Arial", 64, True, False)
    textObject = font.render(text, 0, p.Color("grey"))
    textLocation = p.Rect(0, 0, board_width, board_height).move(board_width / 2 - textObject.get_width() / 2, board_height / 2 - textObject.get_height() / 2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color("black"))
    screen.blit(textObject, textLocation.move(2, 2))

if __name__ == "__main__":
    main()