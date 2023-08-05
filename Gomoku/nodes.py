import numpy as np
import math
class MCTSNode:
    def __init__(self,state="1",parent=None,array=None):
        self.state=state # Indicate the white or the black
        self.win=0.0 # Indicate the reward function
        self.visit=0.0 #Indicate the Total number of visit
        self.parent=parent
        self.children=dict()
        self.action=set() # super root action is None
        self.move=None
        self.initAction(array)
        # self.lastmove=None

    def initAction(self,array):
        self.action=set(zip(*np.where(array == 0)))
        if len(self.action)>=59:
            m,n=array.shape
            slice_m=int((m-4)/2)
            slice_n=int((n-4)/2)
            tmpmat=array[slice_m:slice_m+4,slice_n:slice_n+4]
            action_list = list(zip(*np.where(tmpmat == 0)))
            self.action=set()
            for action in action_list:
                u,v=action
                self.action.add((u+slice_m,v+slice_n))
        elif len(self.action)>=55:
            m, n = array.shape
            slice_m = int((m - 5) / 2)
            slice_n = int((n - 5) / 2)
            tmpmat = array[slice_m:slice_m + 5, slice_n:slice_n + 5]
            action_list = list(zip(*np.where(tmpmat == 0)))
            self.action = set()
            for action in action_list:
                u, v = action
                self.action.add((u + slice_m, v + slice_n))
        elif len(self.action)>=51:
            m, n = array.shape
            slice_m = int((m - 6) / 2)
            slice_n = int((n - 6) / 2)
            tmpmat = array[slice_m:slice_m + 6, slice_n:slice_n + 6]
            action_list = list(zip(*np.where(tmpmat == 0)))
            self.action = set()
            for action in action_list:
                u, v = action
                self.action.add((u + slice_m, v + slice_n))


    def Best_UCT(self,c_param=1.414):
        best_uct=0
        best_child=None
        for child in list(self.children.values()):
            uct=(child.win*1.0)/child.visit+c_param*math.sqrt(math.log(self.visit)/child.visit)
            if uct>=best_uct:
                best_uct=uct
                best_child=child
        return best_child