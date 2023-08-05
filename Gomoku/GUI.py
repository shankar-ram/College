import pygame


def update_by_man(event,mat):
    """
    This function detects the mouse click on the game window. Update the state matrix of the game. 
    input: 
        event:pygame event, which are either quit or mouse click)
        mat: 2D matrix represents the state of the game
    output:
        mat: updated matrix
    """
    m,n=mat.shape
    done=False
    if event.type==pygame.QUIT:
        done=True
    if event.type==pygame.MOUSEBUTTONDOWN:
        (x,y)=event.pos
        row = round((y - 40) / 40)     
        col = round((x - 40) / 40)
        if x<40 or x>40*(m) or y<40 or y>40*(m):
            return mat,done,0,row,col
        if mat[row][col] != 0:
            return mat, done, 0,row,col
        mat[row][col]=1
        return mat, done, 1,row,col
    return mat, done, 0,0,0

def draw_board(screen):    
    """
    This function draws the board with lines.
    input: game windows
    output: none
    """
    black_color = [0, 0, 0]
    board_color = [ 241, 196, 15 ]
    screen.fill(board_color)
    for h in range(1, 9):
        pygame.draw.line(screen, black_color,[40, h * 40], [320, h * 40], 1)
        pygame.draw.line(screen, black_color, [40*h, 40], [40*h, 320], 1)
        
def draw_stone(screen, mat):
    """
    This functions draws the stones according to the mat. It draws a black circle for matrix element 1(human),
    it draws a white circle for matrix element -1 (computer)
    input:
        screen: game window, onto which the stones are drawn
        mat: 2D matrix representing the game state
    output:
        none
    """
    black_color = [0, 0, 0]
    white_color = [255, 255, 255]
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            if mat[i][j]==1:
                pos = [40 * (j + 1), 40 * (i + 1)]
                pygame.draw.circle(screen, black_color, pos, 18,0)
            elif mat[i][j]==-1:
                pos = [40 * (j + 1), 40 * (i + 1)]
                pygame.draw.circle(screen, white_color, pos, 18,0)
            

def render(screen, mat):
    """
    Draw the updated game with lines and stones using function draw_board and draw_stone
    input:
        screen: game window, onto which the stones are drawn
        mat: 2D matrix representing the game state
    output:
        none        
    """
    
    draw_board(screen)
    draw_stone(screen, mat)
    pygame.display.update()

