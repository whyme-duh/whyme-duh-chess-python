import pygame as p
from chess.peices import *
from chess.SmartMoveFinder import *
p.init()


W, H = 490, 490
DIMENSION = 8
SQ_SIZE = round(W / DIMENSION)


win = p.display.set_mode((W, H))

p.display.set_caption("Chess")
FPS = p.time.Clock()
IMAGES = {}
gs = Pieces()
"""
for menu 
"""
menu_image = p.image.load('backgorund.jpg').convert_alpha()
font = p.font.SysFont('monospace', 15 , True)
ANOTHER_FONT = p.font.SysFont('monospace', 15, True)
global clicked

def screen(validmoves, square_selected, clicked):
    win.fill(p.Color("black"))
    drawingBoard()
    highlight_sqaure(win, gs, validmoves , square_selected, clicked )
    drawingLetters()
    drawingPieces(gs.board)
    if not gs.whiteToMove and gs.checkMate:
        word = font.render("WHITE WON THE GAME, PRESS R  TO PLAY AGAIN", True,(255, 0, 0))
        win.blit(word, (25, H / 2))
    if gs.whiteToMove and gs.checkMate:
        word1 = font.render("BLACK WON THE GAME,PRESS R  TO PLAY AGAIN",True, (255, 0, 0))
        win.blit(word1, (25, H / 2))
    p.display.update()

def drawingLetters():
    # for displaying the numbers in the side of the chess board
    num = 8
    color = p.Color('black')
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            indicator = ANOTHER_FONT.render(f'{num}', True, color)
            win.blit(indicator, p.Rect(r * SQ_SIZE , c * SQ_SIZE, 10, 10))
            num -= 1
            if num == 0:
                break
        break

    # for displaying the letters in the board
    A = 65
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            indicator = ANOTHER_FONT.render(f'{chr(A + c)}', True, color)
            win.blit(indicator, p.Rect(c * SQ_SIZE + 50, r * SQ_SIZE + 475, 10, 10))


def drawingBoard():
    global  colors
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c) % 2]
            p.draw.rect(win, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE,SQ_SIZE))

def loadImages():
    pieces = ['bK','bR','bQ','bB','bN','bp','wK','wR','wQ','wB','wN','wp']
    for peice in pieces:
        IMAGES[peice] = p.transform.scale(p.image.load("images/" + peice + '.png'), (SQ_SIZE,SQ_SIZE))


def drawingPieces(board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "-":
                win.blit(IMAGES[piece], (p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE,SQ_SIZE)))


def main_menu(gs):
    x1, y1, = 170, 280
    white_x, white_y = x1 + 20,  y1 + 100
    black_x, black_y = x1 + 120, y1 + 100
    box_width ,box_height = 60, 60
    run = True
    while run:
        for e in p.event.get():
            if e.type == p.QUIT:
                run = False
            if e.type == p.MOUSEBUTTONDOWN:
                pos = p.mouse.get_pos()
                m_x = pos[0]
                m_y = pos[1]
                if m_x < white_x + box_width and m_x > white_x:
                    if m_y > white_y and m_y < white_y + box_height:
                        main()
                        p.quit()
                if m_x < black_x + box_width and m_x > black_x:
                    if m_y > black_y and m_y < black_y + box_height:
                        gs.whiteToMove = False
                        main()
                        p.quit()

        win.blit(menu_image, (0,0))
        # for the surface
        surf = p.Surface((200, 200))
        surf.fill(p.Color('light gray'))
        surf.set_alpha(90)
        win.blit(surf, (x1, y1))
        # title
        word = font.render("PLAY AS ", True, (0,0,0))
        win.blit(word, (x1 + 70, y1 + 20 ))
        # white side
        white = font.render("WHITE", True, (0,0,0))
        win.blit(white, (x1 + 24, y1 + 80))
        surf1 = p.Surface((60, 60))
        surf1.fill(p.Color('white'))
        win.blit(surf1, (x1 + 20, y1 + 100))
        # black side
        black = font.render("BLACK", True, (0, 0, 0))
        win.blit(black, (x1 + 124, y1 + 80))
        surf1 = p.Surface((60, 60))
        surf1.fill(p.Color('black'))
        win.blit(surf1, (x1 + 120, y1 + 100))
        keys = p.key.get_pressed()
        if keys[p.K_SPACE]:
            main()
            break
        p.display.update()

"""
Game Over display
"""
def game_over(gs):
    button = True
    while button:
        for e in p.event.get():
            button = False
            if e.type == p.KEYDOWN:
                if e.key == p.K_p:
                    button = False
                    main()
        if gs.whiteToMove and gs.checkMate:
            word = font.render("CHECKMATE BY BLACK", (255,0,0), True)
            win.blit(word, (W/2, H/2))
        elif not gs.whiteToMove and gs.checkMate:
            word = font.render("CHECKMATE BY white", (255,0,0), True)
            win.blit(word, (W/2, H/2))





'''
Highlights the square selected and the moves of the peice selected
'''
def highlight_sqaure(win , gs, validmoves, square_selected, clicked):
    if square_selected != ():
        r, c = square_selected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):    # sq selected is a piece that can be moved
            # highlight selected sqaure
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)      # set the transparency value  if 0 -> transparent ; 255 -> opaque
            s.fill(p.Color('green'))

            win.blit(s, (c * SQ_SIZE, r * SQ_SIZE))


            #highlight moves from that sqaure
            s.fill(p.Color('light green'))
            for move in validmoves:
                if move.startRow == r and move.startCol == c:
                    win.blit(s,  (move.endCol * SQ_SIZE,  move.endRow * SQ_SIZE))
        if clicked:
            si = p.Surface((SQ_SIZE, SQ_SIZE))
            si.set_alpha(100)
            si.fill(p.Color('orange'))
            win.blit(si, (c * SQ_SIZE , r * SQ_SIZE))

    """
    This if for the check
    """
    if gs.inCheck():
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(50)
        # highlight for the king check
        s.fill(p.Color('Red'))
        if gs.whiteToMove:
            win.blit(s, ( SQ_SIZE * gs.whiteKingLocation[1], SQ_SIZE * gs.whiteKingLocation[0]))
        else:
            win.blit(s, (SQ_SIZE * gs.blackKingLocation[1], SQ_SIZE * gs.blackKingLocation[0]))

    """
    this if for the checkmate
    """
    if gs.checkMate:

        s = p.Surface((SQ_SIZE, SQ_SIZE))
        # highlight for the king check
        s.fill(p.Color('Red'))
        if gs.whiteToMove:
            win.blit(s, ( SQ_SIZE * gs.whiteKingLocation[1], SQ_SIZE * gs.whiteKingLocation[0]))
            
        else:
            win.blit(s, (SQ_SIZE * gs.blackKingLocation[1], SQ_SIZE * gs.blackKingLocation[0]))




def main():
    rn = True
    clicked = False
    loadImages()
    square_selected = ()                    # no sqaure is selected and keep track of the last click of user, row and col collection
    player_clicks = []                      #keep tracks of player clicks ,(two tuples (x,y))
    validMoves = gs.getValidMoves()
    moveMade = False                        # flag variable for when a move is made

    """ players """
    playerOne = True                       # if person is playing whitem then this will be true otherewise false
    playerTwo = False                      # ssame as above but if black


    while rn:
        human_turn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                rn = False
                run = False   # for the menu part


            elif e.type == p.MOUSEBUTTONDOWN:
                # this is use for the highlight the sqaure after right click
                state = p.mouse.get_pressed()
                if state[2] :
                    clicked = True

                #if human_turn:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if square_selected == (row, col):  # user clicked the sqaure twice
                    square_selected = ()  # deselect
                    player_clicks = []  # clear player clicks
                else:
                    square_selected = (row, col)
                    player_clicks.append(square_selected)
                if len(player_clicks) == 2:  # after the second click
                    move = Move(player_clicks[0], player_clicks[1], gs.board)
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(validMoves[i])
                            moveMade = True

                            # these are for the sounds on the chess
                            if (gs.checkMate  and gs.whiteToMove) or (gs.checkMate and not gs.whiteToMove) :
                                p.mixer.Sound('sound/checkmate.mp3').play()
                            elif gs.sqUnderAttack(gs.whiteKingLocation[0], gs.whiteKingLocation[1]) or (gs.sqUnderAttack(gs.blackKingLocation[0], gs.blackKingLocation[1])):
                                p.mixer.Sound('sound/checksound.mp3').play()

                            elif (move.pieceMoved[0] == 'w' and move.pieceCaptured[0] == 'b') or (move.pieceMoved[0] == 'b' and move.pieceCaptured[0] == 'w') or gs.elpassantMove:
                                p.mixer.Sound('sound/capture sound.mp3').play()
                                gs.elpassantMove = False
                            # castling sound
                            elif gs.castling:
                                p.mixer.Sound('sound/castling.mp3').play()
                                gs.castling = False

                            else:
                                p.mixer.Sound('sound/pawnmove.mp3').play()

                            # resetting the user clicks
                            square_selected = ()
                            player_clicks = []
                        if not moveMade:
                            player_clicks = [square_selected]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_a:
                    gs.undoMove()
                    moveMade = True
                elif e.key == p.K_r:
                    gs.reset_board()
                    moveMade = True
                elif e.key == p.K_m:
                    gs.reset_board()
                    main_menu(gs)



            # ai MOVE FINDER
            """if not human_turn and not gs.checkMate:
                p.time.wait(1000)
                AI_MOVE = findBestMove(gs, validMoves)
                if AI_MOVE is None:
                    AI_MOVE = findRandomMoves(validMoves)
                gs.makeMove(AI_MOVE)
                p.mixer.Sound('sound/pawnmove.mp3').play()
                moveMade = True"""




        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        screen(validMoves, square_selected, clicked)


"""
Animating the moves
"""

def animation(move, win, board, clock):
    global colors
    coords = []   # list of coordintated that the animaton wil move through
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSqaure = 10  # FPS
    frameCount = abs(dR) + abs(dC) *framesPerSqaure
    for frame in range(frameCount + 1):
        pass

if __name__ == '__main__':
    main_menu(gs)


p.quit()

