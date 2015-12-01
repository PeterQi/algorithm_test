# coding: UTF-8
import random
from timeit import Timer
import Queue
import math
longest_distance = 100
def random_figure(num, full = False):#随机生成图，full为True时生成有权值的完全图，full为False时生成无权值的非完全图
    figure = [[0 for i in range(num)]for j in range(num)]
    if full:
        for i in range(num):
            figure[i][i] = -1
            for j in range(i):
                figure[i][j] = random.randint(1, longest_distance)
                figure[j][i] = figure[i][j]
    else:
        for i in range(num):
            figure[i][i] = -1
            for j in range(i):
                figure[i][j] = random.randint(0, 1)
                figure[j][i] = figure[i][j]
    return figure

def adjacent(figure):#求邻接点集合
    num = len(figure)
    adj = []
    for i in range(num):
        adj.append([])
        for j in range(num):
            if figure[i][j]>0:
                adj[i].append(j)
    for i in range(num):
        adj.append([])
        adj[num].append(len(adj[i]))
    return adj
    
def BFS(figure, adj = []):
    num = len(figure)
    Hamiltonian = False
    l = Queue.Queue(math.factorial(num))
    top = 0
    if len(adj)==0:
        adj = adjacent(figure)
    for i in adj[0]:
        l.put([i])
    while not l.empty():
        top = l.get()
        if len(top)==num and top[-1] == 0:
            Hamiltonian = True
            break
        if len(top)==num or top[-1] == 0:
            continue
        for i in adj[top[-1]]:
            if i not in top:
                next_path = top+[i]
                l.put(next_path)
    if Hamiltonian:
        print 0,
        for i in top:
            print i,
        print
        return True
    else:
        print "not exist"
        return False
        
def DFS(figure, adj = []):
    num = len(figure)
    Hamiltonian = False
    l = []
    top = 0
    if len(adj)==0:
        adj = adjacent(figure)
    for i in adj[0]:
        l.append([i])
    while len(l)>0:
        top = l.pop()
        if len(top)==num and top[-1] == 0:
            Hamiltonian = True
            break
        if len(top)==num or top[-1] == 0:
            continue
        for i in adj[top[-1]]:
            if i not in top:
                next_path = top+[i]
                l.append(next_path)
    if Hamiltonian:
        print 0,
        for i in top:
            print i,
        print
        return True
    else:
        print "not exist"
        return False
        
def sBFS(figure, adj = []):
    num = len(figure)
    Hamiltonian = False
    l = Queue.Queue(math.factorial(num))
    top = 0
    if len(adj)==0:
        adj = adjacent(figure)
    adj_nums = adj[num]
    for i in adj[0]:
        l.put([i])
    while not l.empty():
        top = l.get()
        if len(top)==num and top[-1] == 0:
            Hamiltonian = True
            break
        if len(top)==num or top[-1] == 0:
            continue
        next_points = []
        for i in adj[top[-1]]:
            if i not in top:
                next_points.append(i)
        next_points = sorted(next_points, key = lambda x:adj_nums[x])
        for i in next_points:
            next_path = top+[i]
            l.put(next_path)
    if Hamiltonian:
        print 0,
        for i in top:
            print i,
        print
        return True
    else:
        print "not exist"
        return False
        
def sDFS(figure, adj = []):
    num = len(figure)
    Hamiltonian = False
    l = []
    top = 0
    if len(adj)==0:
        adj = adjacent(figure)
    adj_nums = adj[num]
    for i in adj[0]:
        l.append([i])
    while len(l)>0:
        top = l.pop()
        if len(top)==num and top[-1] == 0:
            Hamiltonian = True
            break
        if len(top)==num or top[-1] == 0:
            continue
        next_points = []
        for i in adj[top[-1]]:
            if i not in top:
                next_points.append(i)
        next_points = sorted(next_points, key = lambda x:adj_nums[x], reverse = True)
        for i in next_points:
            next_path = top+[i]
            l.append(next_path)
    if Hamiltonian:
        print 0,
        for i in top:
            print i,
        print
        return True
    else:
        print "not exist"
        return False
        
if __name__ == "__main__":
    figure = [[0,1,0,1,1],
              [1,0,1,1,1],
              [0,1,0,1,0],
              [1,1,1,0,0],
              [1,1,0,0,0]]
    num = 10
    figure = random_figure(num)
    adj = adjacent(figure)
    t1 = Timer("BFS(figure, adj)", "from __main__ import BFS; figure="+str(figure)+"; adj="+str(adj))
    t2 = Timer("DFS(figure, adj)", "from __main__ import DFS; figure="+str(figure)+"; adj="+str(adj))
    t3 = Timer("sBFS(figure, adj)", "from __main__ import sBFS; figure="+str(figure)+"; adj="+str(adj))
    t4 = Timer("sDFS(figure, adj)", "from __main__ import sDFS; figure="+str(figure)+"; adj="+str(adj))
    T1 = t1.timeit(10)
    T2 = t2.timeit(10)
    T3 = t3.timeit(10)
    T4 = t4.timeit(10)
    if T1>T3:
        print "yes"
    else:
        print "no"
    if T2>T4:
        print "yes"
    else:
        print "no"
    #print T1, T3
    #print T2, T4
    