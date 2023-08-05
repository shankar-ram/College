import random
import time
from nodes import *
import threading
import sys
class MCTSearch:
    def __init__(self,root,array,debug=False,strategy=False):
        self.root = root
        self.array = array
        # self.root_nonzero=len(np.nonzero(self.array)[0])
        self.debug=debug
        self.strategy=strategy
    def monte_carlo_tree_search(self,multi=False):
        tic = time.time()
        simulation_times=0
        while(time.time()-tic<10):
            child=self.traverse(self.root)
            leaf,result=self.rollout(child)
            self.backpropagate(leaf,result)
            simulation_times += 1
            if self.debug:
                self.print_child_of_root()
                sumWin=0
                sumVisit=0
                for child in list(self.root.children.values()):
                    sumWin +=child.win
                    sumVisit += child.visit
                assert self.root.win==sumWin
                assert self.root.visit==sumVisit
        best_child=self.best_child(self.root)
        # toc=time.time()
        # print("Thinking Time: %.2fs"%(toc-tic))
        if self.strategy:
            cor_attack, priority_attack = blockStrategy(self.array, self.root.state)  ##如果没有，返回两个false

            cor_block, priority_block = blockStrategy(self.array, self.root.state*-1)  #######符号

            output = False  # 策略结果初始化

            if (priority_attack != False) and (priority_block == False):
                output = cor_attack

            if (priority_attack == False) and (priority_block != False):
                output = cor_block

            if (priority_attack != False) and (priority_block != False):  ##都有
                if priority_attack < priority_block:  # 3(3子)>4(4子)
                    output = cor_block
                else:
                    output = cor_attack

            # output=blockStrategy(self.array,self.root.state)
            if output:
                if best_child.move==output:
                    return best_child
                elif output in set(self.root.children.keys()):
                    return self.root.children[output]
                else:
                    nextState=self.root.state*(-1)
                    u, v = output
                    self.array[u,v]=nextState
                    child = MCTSNode(nextState,self.root, self.array)
                    self.array[u, v]=0
                    child.move = (u, v)
                    self.root.children[(u, v)] = child
                    return child
        else:
            return best_child
        if not multi:
            return best_child

    def traverse(self,root):
        nextState=root.state*(-1)
        if len(root.action)==0:
            child = root.Best_UCT()
            if self.strategy:
                cor_attack, priority_attack = blockStrategy(self.array, root.state)  ##如果没有，返回两个false

                cor_block, priority_block = blockStrategy(self.array, root.state * -1)  #######符号

                output = False  # 策略结果初始化

                if (priority_attack != False) and (priority_block == False):
                    output = cor_attack

                if (priority_attack == False) and (priority_block != False):
                    output = cor_block

                if (priority_attack != False) and (priority_block != False):  ##都有
                    if priority_attack < priority_block:  # 3(3子)>4(4子)
                        output = cor_block
                    else:
                        output = cor_attack

                # output = blockStrategy(self.array,root.state)
                if output:
                    if output in set(root.children.keys()):
                        child=root.children[output]
                        u,v=child.move
                        self.array[u, v] = nextState
                        return child
                    else:
                        nextState = root.state * (-1)
                        u, v = output
                        self.array[u, v] = nextState
                        child = MCTSNode(nextState, root, self.array)
                        child.move = (u, v)
                        root.children[(u, v)] = child
                        return child
                # for son in root.children:
                #     if son.move==output:
                #         child=son
                #         u,v=child.move
                #         self.array[u, v] = nextState
                #         return child
            # child=root.Best_UCT()
            if self.debug:
                print("Best_UCT win/visited: %d/%d"%(child.win,child.visit))
                print(child.move)
            u, v = child.move
            self.array[u, v] = nextState
            return child
        else:
            u,v=root.action.pop()
            self.array[u,v]=nextState
            child = MCTSNode(nextState, root, self.array)
            child.move=(u,v)
            # root.children.append(child)
            root.children[(u,v)]=child
        return child



    def rollout(self,child):
        while(1):
            result=check02(self.array,child.state)
            if result==-2:
                child = self.rollout_policy(child)
            else:
                return child,result

    def rollout_policy(self,child):
        nextState=child.state*(-1)
        if len(child.action)!=0:
            u,v = random.choice(list(child.action))
            child.action.remove((u,v))
            self.array[u, v] = nextState
            picked = MCTSNode(nextState, child, self.array)
            picked.move=(u, v)
            # child.children.append(picked)
            child.children[(u,v)]=picked
        else:
            picked = child.Best_UCT()
            # picked=random.choice(child.children)
            if self.strategy:
                cor_attack, priority_attack = blockStrategy(self.array, child.state)  ##如果没有，返回两个false

                cor_block, priority_block = blockStrategy(self.array, child.state * -1)  #######符号

                output = False  # 策略结果初始化

                if (priority_attack != False) and (priority_block == False):
                    output = cor_attack

                if (priority_attack == False) and (priority_block != False):
                    output = cor_block

                if (priority_attack != False) and (priority_block != False):  ##都有
                    if priority_attack < priority_block:  # 3(3子)>4(4子)
                        output = cor_block
                    else:
                        output = cor_attack


                # output = blockStrategy(self.array,child.state)
                if output:
                    if output in set(child.children.keys()):
                        picked=child.children[output]
                        u, v = picked.move
                        self.array[u, v] = nextState
                        return picked
                    else:
                        nextState = child.state * (-1)
                        u, v = output
                        self.array[u, v] = nextState
                        picked = MCTSNode(nextState, child, self.array)
                        picked.move = (u, v)
                        child.children[(u, v)] = picked
                        return picked
                    # for son in child.children:
                    #     if son.move==output:
                    #         picked=son
                    #         u,v=picked.move
                    #         self.array[u, v] = nextState
                    #         return picked
                # picked=child.Best_UCT()
            u,v=picked.move
            self.array[u, v] = nextState
        return picked

    def backpropagate(self,node,result):
        if result==(self.root.state*-1):
            node.win+=1
        elif result==0:
            node.win+=0.5
        node.visit+=1
        if node==self.root:
            return
        u,v= node.move
        self.array[u,v]=0
        return self.backpropagate(node.parent,result)

    def best_child(self,root):
        vistTimes=0
        best=None
        for child in list(root.children.values()):
            if child.visit>vistTimes:
                vistTimes=child.visit
                best=child
        return best
    def print_child_of_root(self):
        i=0
        print("Root: %d/%d "%(self.root.win,self.root.visit))
        for child in list(self.root.children.values()):
            u,v=child.move
            print("Node %d : %d/%d Move:(%d,%d) "%(i+1,child.win,child.visit,u,v))
            i+=1



def check(mat,state):
    # Check for player i(1 or -1) if there exist 5 consecutive stones in the horizontal/vertical/diagonal/anti-diagonal
    # direction, returns False if it is found, else return True
    if check_for_tie(mat):
        return 0
    player=state
    m, n = mat.shape
    for i in range(m):
        for j in range(n):
            # check horizon
            acc_hor = 0
            for q in range(5):
                tmp_i = i + q
                if tmp_i in range(m):
                    acc_hor += mat[tmp_i][j]
            if acc_hor == player * 5:
                return player
            # check verticle
            acc_ver = 0
            for q in range(5):
                tmp_j = j + q
                if tmp_j in range(n):
                    acc_ver += mat[i][tmp_j]
            if acc_ver == player * 5:
                return player
                # return (acc_ver // 5) == player
            # check diagonal
            acc_dia = 0
            for q in range(5):
                tmp_i = i + q
                tmp_j = j + q
                if (tmp_i in range(m)) and (tmp_j in range(n)):
                    acc_dia += mat[tmp_i][tmp_j]
            if acc_dia == player * 5:
                return player
                # return (acc_dia // 5) == player
            # check anti-diagonal
            acc_ant = 0
            for q in range(5):
                tmp_i = i - q
                tmp_j = j + q
                if (tmp_i in range(m)) and (tmp_j in range(n)):
                    acc_ant += mat[tmp_i][tmp_j]
            if acc_ant == player * 5:
                return player
                # return (acc_ant // 5) == player
    return -2

def check_for_tie(mat):
    # Returns true if no more space available
    m, n = mat.shape
    for i in range(m):
        for j in range(n):
            if mat[i][j] == 0:
                return False
    return True

def find_MCTS_trees(mcts,move):
    if move in set(mcts.children.keys()):
        # mcts.children[move].move=None
        return mcts.children[move]
    # for child in mcts.children:
    #     # print(child.move)
    #     # print(move)
    #     if child.move==move:
    #         child.move=None
    #         return child


def check02(mat,state):
    m,n=mat.shape
    # output=pruningStrategy(mat,state)
    # if output is not None:
        # return output
    for i in range(m-5+1):
        for j in range(n-5+1):
            mask=mat[i:i+5,j:j+5]==state
            ## Test vertical and horizontal
            out=mask.all(1).any()|mask.all(0).any()
            out|=np.diag(mask).all() | np.diag(mask[:,::-1]).all()
            if out:
                return state
    if check_for_tie02(mat):
        return 0
    return -2

def checkComputer(mat,state,root_nonzero):
    m,n=mat.shape
    for i in range(m-5+1):
        for j in range(n-5+1):
            mask=mat[i:i+5,j:j+5]==state
            ## Test vertical and horizontal
            out=mask.all(1).any()|mask.all(0).any()
            out|=np.diag(mask).all() | np.diag(mask[:,::-1]).all()
            if out:
                return state
    if len(np.nonzero(mat)[0])-(root_nonzero)>4:
        return 0
    if check_for_tie02(mat):
        return 0
    return -2


def check_for_tie02(mat):
    m,n=mat.shape
    x=np.absolute(mat)
    if np.sum(x)==m*n:
        return True
    else:
        return False


def blockStrategy(mat, state):
    m, n = mat.shape  ##优先级：先判断4，5个子，再到3  #3->0, 4->1, 5->2, 6->3, 0->4, 1->5, 2->6

    vectors = [np.array([state, state, state, state]),

               np.array([state, 0, state, state, state]),

               np.array([state, state, 0, state, state]),

               np.array([state, state, state, 0, state]),

               np.array([state, state, state]),

               np.array([state, 0, state, state]),

               np.array([state, state, 0, state])]

    for vv in range(7):
        length = len(vectors[vv])
        for i in range(m - length + 1):
            for j in range(n - length + 1):
                tmpmat = mat[i:i + length, j:j + length]
                for row in range(length):
                    if (tmpmat[row] == vectors[vv]).all():
                        """vector"""

                        if vv == 1:
                            return (i + row, j + 1), 4  ##return多一个值代表优先级
                        if vv == 2:
                            return (i + row, j + 2), 4
                        if vv == 3:
                            return (i + row, j + 3), 4

                        if vv == 0:
                            if j - 1 in range(0, n) and mat[i + row, j - 1] == 0:
                                return (i + row, j - 1), 4

                            if j + length in range(0, n) and mat[
                                i + row, j + length] == 0:  ###if mat[i+row,j+length]==0:
                                return (i + row, j + length), 4

                        if vv == 5 and j - 1 in range(0, n) and j + length in range(0, n) and (
                                mat[i + row, j - 1] == 0 and mat[i + row, j + length] == 0):
                            return (i + row, j + 1), 3
                        if vv == 6 and j - 1 in range(0, n) and j + length in range(0, n) and (
                                mat[i + row, j - 1] == 0 and mat[i + row, j + length] == 0):
                            return (i + row, j + 2), 3
                        """ 3 in line"""
                        if j - 1 in range(0, n) and mat[i + row, j - 1] == 0 and j + length in range(0, n) and mat[
                            i + row, j + length] == 0:
                            tmp=random.choice([j - 1,j+length])
                            return (i + row, tmp), 3  ####活三选一边
                        # if j+length in range(0,n) and mat[i+row,j+length]==0:
                        # return (i+row,j+length)
                for col in range(length):  ##优先级：先判断4，5个子，再到3  #3->0, 4->1, 5->2, 6->3, 0->4, 1->5, 2->6
                    if (tmpmat[:, col] == vectors[vv]).all():
                        """vector"""

                        if vv == 1:
                            return (i + 1, j + col), 4
                        if vv == 2:
                            return (i + 2, j + col), 4
                        if vv == 3:
                            return (i + 3, j + col), 4

                        if vv == 0:
                            if i - 1 in range(0, m) and mat[i - 1, j + col] == 0:  ###4个相连且有空位
                                return (i - 1, j + col), 4
                            if i + length in range(0, m) and mat[i + length, j + col] == 0:
                                return (i + length, j + col), 4

                        if vv == 5 and i - 1 in range(0, m) and i + length in range(0, m) \
                                and (mat[i - 1, j + col] == 0 and mat[i + length, j + col] == 0):
                            return (i + 1, j + col), 3

                        if vv == 6 and i - 1 in range(0, m) and i + length in range(0, m) \
                                and (mat[i - 1, j + col] == 0 and mat[i + length, j + col] == 0):
                            return (i + 2, j + col), 3
                        """3 in line"""
                        if i - 1 in range(0, m) and mat[i - 1, j + col] == 0 and i + length in range(0, m) and mat[
                            i + length, j + col] == 0:
                            tmp = random.choice([i - 1,i + length])
                            return (tmp, j + col), 3
                        # if i + length in range(0, m) and mat[i + length, j + col] == 0:
                        # return (i +length, j +col)

                if (np.diag(tmpmat) == vectors[vv]).all():
                    """vector"""  ##优先级：先判断4，5个子，再到3  #3->0, 4->1, 5->2, 6->3, 0->4, 1->5, 2->6
                    if vv == 1:
                        return (i + 1, j + 1), 4
                    if vv == 2:
                        return (i + 2, j + 2), 4
                    if vv == 3:
                        return (i + 3, j + 3), 4

                    if vv == 0:
                        if i - 1 in range(0, m) and j - 1 in range(0, n) and mat[i - 1, j - 1] == 0:
                            return (i - 1, j - 1), 4

                        if i + length in range(0, m) and j + length in range(0, n) and mat[i + length, j + length] == 0:
                            return (i + length, j + length), 4

                    if vv == 5 and i - 1 in range(0, m) and j - 1 in range(0, n) and i + length in range(0,
                                                                                                         m) and j + length in range(
                        0, n) \
                            and (mat[i - 1, j - 1] == 0 and mat[i + length, j + length] == 0):
                        return (i + 1, j + 1), 3
                    if vv == 6 and i - 1 in range(0, m) and j - 1 in range(0, n) and i + length in range(0,
                                                                                                         m) and j + length in range(
                        0, n) \
                            and (mat[i - 1, j - 1] == 0 and mat[i + length, j + length] == 0):
                        return (i + 2, j + 2), 3
                    """3 in line"""
                    if i - 1 in range(0, m) and j - 1 in range(0, n) and mat[i - 1, j - 1] == 0 \
                            and i + length in range(0, m) and j + length in range(0, n) and mat[
                        i + length, j + length] == 0:
                        tmp = random.choice([(i - 1,j-1), (i + length,j+length)])
                        return tmp, 3
                    # if i + length in range(0, m) and j+length in range(0,n) and mat[i +length, j + length] == 0:
                    # return (i + length, j + length)

                if (np.diag(tmpmat[:, ::-1]) == vectors[vv]).all():
                    """vector"""  ##优先级：先判断4，5个子，再到3  #3->0, 4->1, 5->2, 6->3, 0->4, 1->5, 2->6
                    if vv == 1:
                        return (i + 1, j + 3), 4
                    if vv == 2:
                        return (i + 2, j + 2), 4
                    if vv == 3:
                        return (i + 3, j + 1), 4

                    if vv == 0:
                        if i - 1 in range(0, m) and j + length in range(0, n) and mat[i - 1, j + length] == 0:
                            return (i - 1, j + length), 4
                        if i + length in range(0, m) and j - 1 in range(0, n) and mat[i + length, j - 1] == 0:
                            return (i + length, j - 1), 4

                    if vv == 5 and i - 1 in range(0, m) and j + length in range(0, n) and i + length in range(0,
                                                                                                              m) and j - 1 in range(
                        0, n) \
                            and (mat[i - 1, j + length] == 0 and mat[i + length, j - 1] == 0):
                        return (i + 1, j + 2), 3

                    if vv == 6 and i - 1 in range(0, m) and j + length in range(0, n) and i + length in range(0,
                                                                                                              m) and j - 1 in range(
                        0, n) \
                            and (mat[i - 1, j + length] == 0 and mat[i + length, j - 1] == 0):
                        return (i + 2, j + 1), 3
                    """3 in line"""
                    if i - 1 in range(0, m) and j + length in range(0, n) and mat[
                        i - 1, j + length] == 0 and i + length in range(0, m) and j - 1 in range(0, n) and mat[
                        i + length, j - 1] == 0:
                        tmp = random.choice([(i - 1, j + length), (i + length, j - 1)])
                        return tmp, 3
                    # if i + length in range(0, m) and j-1 in range(0,n) and mat[i +length, j -1] == 0:
                    # return (i + length, j -1)
    return False, False

def pruningStrategy(mat,state):
    m, n = mat.shape
    vector= np.array([state,state,state,state])
    length=len(vector)
    for i in range(m-length+1):
        for j in range(n-length+1):
            tmpmat = mat[i:i + length, j:j + length]
            for row in range(length):
                if (tmpmat[row] == vector).all():
                    if j - 1 in range(0, n) and j+length in range(0,n):
                        if mat[i+row,j-1]==0 and  mat[i+row,j+length]==0:
                            # blank in two side of vector
                            return state
            for col in range(length):
                if (tmpmat[:, col] == vector).all():
                    if i - 1 in range(0, m) and i + length in range(0, m):
                        if mat[i -1, j +col] == 0 and mat[i + length, j + col]==0:
                            return state

            if (np.diag(tmpmat) == vector).all():
                if i - 1 in range(0, m) and j-1 in range(0,n) and i + length in range(0, m) and j+length in range(0,n):
                    if mat[i - 1, j -1] == 0 and mat[i +length, j + length] == 0:
                        return state
            if (np.diag(tmpmat[:, ::-1]) == vector).all():
                if i - 1 in range(0, m) and j+length in range(0,n) and i + length in range(0, m) and j-1 in range(0,n):
                    if mat[i - 1, j +length] == 0 and mat[i +length, j + length] == 0:
                        return state
    vector=[0,1,1,1,0]
    for i in range(m-5+1):
        for j in range(n-5+1):
            tmpmat=mat[i:i+5,j:j+5]
            if (tmpmat[2,:]==vector).all() and (tmpmat[:,2]==vector).all():
                return state
            if (np.diag(tmpmat)==vector).all() and (np.diag(tmpmat[:,::-1])==vector).all():
                return state
    return None


def check_3_in_line(mat):
    m,n=mat.shape
    vectors = [np.array([1, 1, 1]),np.array([1, 0, 1,1]),np.array([1, 1, 0,1 ])]
    for vv in range(3):
        length=len(vectors[vv])
        for i in range(m-length+1):
            for j in range(n-length+1):
                tmpmat=mat[i:i+length,j:j+length]
                for row in range(length):
                    if (tmpmat[row]==vectors[vv]).all():
                        """vector"""
                        if vv==1:
                            return (i+row,j+1)
                        if vv==2:
                            return (i+row,j+2)
                        """ 3 in line"""
                        if j-1 in range(0,n) and mat[i+row,j-1]==0:
                            return (i+row,j-1)
                        if j+length in range(0,n) and mat[i+row,j+length]==0:
                            return (i+row,j+length)
                for col in range(length):
                    if (tmpmat[:,col]==vectors[vv]).all():
                        """vector"""
                        if vv==1:
                            return (i+1,j+col)
                        if vv==2:
                            return (i+2,j+col)
                        """3 in line"""
                        if i - 1 in range(0, m) and mat[i -1, j +col] == 0:
                            return (i -1, j+col)
                        if i + length in range(0, m) and mat[i + length, j + col] == 0:
                            return (i +length, j +col)

                if (np.diag(tmpmat)==vectors[vv]).all():
                    """vector"""
                    if vv==1:
                        return (i + 1, j + 1)
                    if vv==2:
                        return (i + 2, j + 2)
                    """3 in line"""
                    if i - 1 in range(0, m)  and j-1 in range(0,n) and mat[i - 1, j -1] == 0:
                        return (i - 1, j -1)
                    if i + length in range(0, m) and j+length in range(0,n) and mat[i +length, j + length] == 0:
                        return (i + length, j + length)
                if (np.diag(tmpmat[:,::-1])==vectors[vv]).all():
                    """vector"""
                    if vv==1:
                        return (i + 1, j + 2)
                    if vv==2:
                        return (i + 2, j + 1)
                    """3 in line"""
                    if i - 1 in range(0, m)  and j+length in range(0,n) and mat[i - 1, j +length] == 0:
                        return (i - 1, j +length)
                    if i + length in range(0, m) and j-1 in range(0,n) and mat[i +length, j -1] == 0:
                        return (i + length, j -1)
    vector=[0,1,0,1,0]
    for i in range(m-5+1):
        for j in range(n-5+1):
            tmpmat=mat[i:i+5,j:j+5]
            if (tmpmat[2,:]==vector).all() and (tmpmat[:,2]==vector).all():
                return (i+2,j+2)
            if (np.diag(tmpmat)==vector).all() and (np.diag(tmpmat[:,::-1])==vector).all():
                return (i+2,j+2)
    return False



def multiThreadingMCTS(root,state,mat,strategy=True):
    Actionlist=[]
    Actionlist.extend(root.action)
    threadNum = len(Actionlist)
    """"""
    if threadNum!=0:
        parts = int(len(Actionlist) / threadNum)
    else:
        parts=0
    Rootlist_01=[]
    boardlist_01=[]
    for i in range(threadNum):
        boardlist_01.append(mat.copy())
        Rootlist_01.append(MCTSNode(state, array=boardlist_01[i]))
    threadlist = []
    for i in range(threadNum):
        if i == threadNum-1:
            Rootlist_01[i].action=set(Actionlist[i*parts:len(Actionlist)])
            instance=MCTSearch(Rootlist_01[i], boardlist_01[i],strategy=True)
            t=threading.Thread(target=instance.monte_carlo_tree_search,kwargs={'multi':True})
        else:
            Rootlist_01[i].action = set(Actionlist[i * parts:(i + 1) * parts])
            instance = MCTSearch(Rootlist_01[i], boardlist_01[i],strategy=True)
            t=threading.Thread(target=instance.monte_carlo_tree_search, kwargs={'multi': True})
        t.setDaemon(True)
        t.start()
        threadlist.append(t)
    """children part"""
    childrenlist = []
    childrenlist.extend(list(root.children.values()))
    threadNum = len(childrenlist)
    dict_slice = lambda adict, start, end: {k: adict[k] for k in list(adict.keys())[start:end]}
    if threadNum !=0:
        parts = int(len(childrenlist) / threadNum)
    else:
        parts=0
    Rootlist_02 = []
    boardlist_02 = []
    for i in range(threadNum):
        boardlist_02.append(mat.copy())
        Rootlist_02.append(MCTSNode(state, array=boardlist_02[i]))
    for i in range(threadNum):
        if i == threadNum - 1:
            Rootlist_02[i].children = dict_slice(root.children,i * parts,len(childrenlist))
                # childrenlist[i * parts:len(childrenlist)]
            instance = MCTSearch(Rootlist_02[i], boardlist_02[i],strategy=True)
            t = threading.Thread(target=instance.monte_carlo_tree_search, kwargs={'multi': True})
        else:
            Rootlist_02[i].children = dict_slice(root.children, i * parts, (i + 1) * parts)
            instance = MCTSearch(Rootlist_02[i], boardlist_02[i],strategy=True)
            t = threading.Thread(target=instance.monte_carlo_tree_search, kwargs={'multi': True})
        t.setDaemon(True)
        t.start()
        threadlist.append(t)

    for thread in threadlist:
        try:
            while thread.is_alive():
                pass
        except KeyboardInterrupt:
            break
    root.action=set()
    root.children=dict()
    Rootlist=[]
    Rootlist.extend(Rootlist_01)
    Rootlist.extend(Rootlist_02)
    for Root in Rootlist:
        root.children.update(Root.children)
        root.action=set.union(root.action,Root.action)
        root.win+=Root.win
        root.visit+=Root.visit

    vistTimes = 0
    best = None
    for child in list(root.children.values()):
        if child.visit > vistTimes:
            vistTimes = child.visit
            best = child

    if strategy:
        cor_attack, priority_attack = blockStrategy(mat, root.state)  ##如果没有，返回两个false

        cor_block, priority_block = blockStrategy(mat, root.state*-1)  #######符号

        output = False  # 策略结果初始化

        if (priority_attack != False) and (priority_block == False):
            output = cor_attack

        if (priority_attack == False) and (priority_block != False):
            output = cor_block

        if (priority_attack != False) and (priority_block != False):  ##都有
            if priority_attack < priority_block:  # 3(3子)>4(4子)
                output = cor_block
            else:
                output = cor_attack

        # output=blockStrategy(self.array,self.root.state)
        if output:
            if best.move == output:
                return best
            elif output in set(root.children.keys()):
                return root.children[output]
            else:
                nextState = root.state * (-1)
                u, v = output
                mat[u, v] = nextState
                child = MCTSNode(nextState, root, mat)
                mat[u, v] = 0
                child.move = (u, v)
                root.children[(u, v)] = child
                return child
    return best
