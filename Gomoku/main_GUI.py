import numpy as np
from MCTSearch import *
from nodes import *
import random
import pygame
from GUI import *
"""
def printboard(mat):
    m,n=mat.shape
    print("  ",end='')
    for i in range(1,n+1):
        print("{:4d}".format(i),end='')
    print()
    print(' '*4+'-'*22)
    for i in range(m):
        print("{:3d}|".format(i+1),end='')
        for j in range(n):
            char='-'
            if mat[i,j]==1:
                char='*'
            elif mat[i,j]==-1:
                char='o'
            print(' {:3s}'.format(char),end='')
        print()
"""
if __name__=="__main__":
    """
    If You Get The Plus then Initialize the node with State of Plus
    """
    m,n=(8,8)
    board=np.zeros((m,n),dtype=np.int8)

    pygame.init()
    screen=pygame.display.set_mode((360,360))
    pygame.display.set_caption('Five-in-a-Row')
    done=False
    over=False

    #printboard(board)
    """
    """
    mst=None
    while not done:
        for event in pygame.event.get():
            """
            test = -2
            while test != 0:
                x = int(input("Enter the x coordinate of your chosen site (1-%d):"%(n)))
                y = int(input("Enter the y coordinate of your chosen site (1-%d):"%(n)))
                while (x not in range(1, m+1)) or (y not in range(1, n+1)):
                    x = int(input("Enter the x coordinate of your chosen site (1-%d):"%(n)))
                    y = int(input("Enter the y coordinate of your chosen site (1-%d):"%(n)))
                test = board[x - 1][y - 1]
                if test == 0:
                    board[x - 1][y - 1] = 1
                    print("Adding %d to (%d,%d) successfully" % (1, x, y))
                    printboard(board)
                    break
                print("Site is occupied, choose a different location")
            """
            render(screen, board)
            board, done, ocp, x, y=update_by_man(event, board)
            if ocp==0:
                continue
            render(screen, board)
            result=check02(board,1)
            if result==1:
                print("You win!")
                done=True
                over=True
                break
            elif result==0:
                print("Draw")
                done=True
                over=True
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("Computer round...")
                root=None
                if isinstance(mst,MCTSNode) and len(mst.action)==0:
                    print("Computer take it serious!!")
                    root=find_MCTS_trees(mst,(x,y))
                    # root.parent=None
                    # print(root.action)
                if root is None:
                    root=MCTSNode(1,array=board)
                # mst=MCTSearch(root,board,strategy=True).monte_carlo_tree_search()
                mst = multiThreadingMCTS(root,1,board,strategy=True)
                if isinstance(mst,tuple):
                    u,v=mst
                else:
                    u,v=mst.move
                board[u][v] = -1
                print("Computer move to (%d,%d)"%(u+1,v+1))
                render(screen, board)
                #printboard(board)
                result = check02(board, -1)
                if result==-1:
                    print("Computer win!")
                    done=True
                    over=True
                    break
                elif result==0:
                    print("Draw")
                    done=True
                    over=True
                    break
    if over == False:
        pygame.quit()
    else:
        for i in range(5,0,-1):
            print(i)
            time.sleep(1)
        print("Quit!")
        pygame.quit()
    # board[4,3]=1
    # node=MCTSNode(1,array=board)
    # mst=MCTSearch(node,board).monte_carlo_tree_search()
    # print(len(mst.action))