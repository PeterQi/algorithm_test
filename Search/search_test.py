# coding: UTF-8
import random
from timeit import Timer
import Queue
from heapq import *
import os
import math
import copy
longest_distance = 100
def random_figure(num, full = False):#随机生成图，full为True时生成有权值的完全图，full为False时生成无权值的非完全图
    figure = [[0 for i in range(num)]for j in range(num)]
    if full:
        for i in range(num):
            figure[i][i] = -1
            for j in range(i):
                figure[i][j] = random.randint(1, longest_distance)
                #figure[j][i] = random.randint(1, longest_distance)
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
        
def sBFS(figure, adj = []):#爬山法
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
        
def sDFS(figure, adj = []):#爬山法
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
 
def figure_change(figure):#更新矩阵
    num = len(figure)
    changed_figure = figure
    zero_points = []
    limit = 0
    for i in range(num):
        change_flag = False
        row_min = longest_distance*num
        for j in range(num):
            if figure[i][j]<0:
                continue
            if figure[i][j]==0:
                row_min = 0
                zero_points.append((i,j))
                continue
            if figure[i][j]<row_min:
                change_flag = True
                row_min = figure[i][j]
        if row_min>0 and change_flag:
            limit += row_min
            for j in range(num):
                changed_figure[i][j] -= row_min
                if changed_figure[i][j]==0:
                    zero_points.append((i, j))
    for j in range(num):
        col_min = longest_distance*num
        change_flag = False
        for i in range(num):
            if changed_figure[i][j]<0:
                continue
            if changed_figure[i][j]<col_min:
                col_min = changed_figure[i][j]
                change_flag = True
        if col_min>0 and change_flag:
            limit += col_min
            for i in range(num):
                changed_figure[i][j] -= col_min
                if changed_figure[i][j] == 0:
                    zero_points.append((i, j))
    return [limit, changed_figure, zero_points]

def exist_path(figure_E):#返回不能使用的边集合
    num = len(figure_E)
    next = [-1 for i in range(num)]
    last = [-1 for i in range(num)]
    not_path = []
    for i in range(num):
        for j in range(i):
            if figure_E[i][1]==figure_E[j][0]:
                next[i] = j
                last[j] = i
                continue
            if figure_E[i][0]==figure_E[j][1]:
                next[j] = i
                last[i] = j
    for i in range(num):
        if last[i]==-1:
            it = i
            while next[it]!=-1:
                it = next[it]
            not_path.append((figure_E[it][1], figure_E[i][0]))
    return not_path

def branch_cut(figure):#分支限界法
    h = []
    num = len(figure)
    cf = figure_change(figure)
    heappush(h, cf+[[]])#每一个节点，0表示路径下界，1表示其邻接矩阵，2表示为0的节点集合，3表示已有路径集合
    Hamiltonian = longest_distance*num
    Hamiltonian_path = -1
    while len(h)>0:
        top = heappop(h)
        if top[0]>=Hamiltonian:
            continue
        
        if len(top[2])==0:
            continue
        f = []
        for point in top[2]:
            row_min = longest_distance*num
            col_min = longest_distance*num
            for i in range(num):
                if top[1][point[0]][i]>=0 and i != point[1]:
                    if top[1][point[0]][i]<row_min:
                        row_min = top[1][point[0]][i]
                if top[1][i][point[1]]>=0 and i != point[0]:
                    if top[1][i][point[1]]<col_min:
                        col_min = top[1][i][point[1]]
            f.append((point, row_min+col_min))
        max_point = 0
        
        for i in range(1, len(f)):
            if f[i][1]>f[max_point][1]:
                max_point = i
                
        
        chosen_line = f[max_point][0]#下次扩展该节点
        if len(top[3])+1 == num:#找到一个解
            if top[0]+top[1][chosen_line[0]][chosen_line[1]]<Hamiltonian:
                Hamiltonian = top[0]+top[1][chosen_line[0]][chosen_line[1]]
                Hamiltonian_path = top[3]+[chosen_line]
                continue
        leftnode_figure = copy.deepcopy(top[1])
        rightnode_figure = copy.deepcopy(top[1])
        
        if len(top[3])+2 != num:#防止出现非哈密顿环
            not_path = exist_path(top[3]+[chosen_line])
            for i in not_path:
                leftnode_figure[i[0]][i[1]] = -1
        
        for i in range(num):
            leftnode_figure[chosen_line[0]][i] = -1
            leftnode_figure[i][chosen_line[1]] = -1
        tmp_cf = figure_change(leftnode_figure)
        lp = top[3] + [chosen_line]
        leftnode = [tmp_cf[0]+top[0], tmp_cf[1], tmp_cf[2], lp]
        
        rightnode_figure[chosen_line[0]][chosen_line[1]] = -1
        tmp_cf2 = figure_change(rightnode_figure)
        rightnode = [tmp_cf2[0]+top[0], tmp_cf2[1], tmp_cf2[2], top[3]]
        heappush(h, leftnode)
        heappush(h, rightnode)
    return Hamiltonian_path, Hamiltonian

def sbranch_cut(figure):#分支限界法，找解用DFS
    h = []
    num = len(figure)
    cf = figure_change(figure)
    h.append(cf+[[]])#每一个节点，0表示路径下界，1表示其邻接矩阵，2表示为0的节点集合，3表示已有路径集合
    Hamiltonian = longest_distance*num
    Hamiltonian_path = -1
    while len(h)>0:
        top = h.pop()
        if top[0]>=Hamiltonian:
            continue
        
        if len(top[2])==0:
            continue
        f = []
        for point in top[2]:
            row_min = longest_distance*num
            col_min = longest_distance*num
            for i in range(num):
                if top[1][point[0]][i]>=0 and i != point[1]:
                    if top[1][point[0]][i]<row_min:
                        row_min = top[1][point[0]][i]
                if top[1][i][point[1]]>=0 and i != point[0]:
                    if top[1][i][point[1]]<col_min:
                        col_min = top[1][i][point[1]]
            f.append((point, row_min+col_min))
        max_point = 0
        
        for i in range(1, len(f)):
            if f[i][1]>f[max_point][1]:
                max_point = i
                
        
        chosen_line = f[max_point][0]#下次扩展该节点
        if len(top[3])+1 == num:#找到一个解
            if top[0]+top[1][chosen_line[0]][chosen_line[1]]<Hamiltonian:
                Hamiltonian = top[0]+top[1][chosen_line[0]][chosen_line[1]]
                Hamiltonian_path = top[3]+[chosen_line]
                continue
        leftnode_figure = copy.deepcopy(top[1])
        rightnode_figure = copy.deepcopy(top[1])
        
        if len(top[3])+2 != num:#防止出现非哈密顿环
            not_path = exist_path(top[3]+[chosen_line])
            for i in not_path:
                leftnode_figure[i[0]][i[1]] = -1
        
        for i in range(num):
            leftnode_figure[chosen_line[0]][i] = -1
            leftnode_figure[i][chosen_line[1]] = -1
        tmp_cf = figure_change(leftnode_figure)
        lp = top[3] + [chosen_line]
        leftnode = [tmp_cf[0]+top[0], tmp_cf[1], tmp_cf[2], lp]
        
        rightnode_figure[chosen_line[0]][chosen_line[1]] = -1
        tmp_cf2 = figure_change(rightnode_figure)
        rightnode = [tmp_cf2[0]+top[0], tmp_cf2[1], tmp_cf2[2], top[3]]
        h.append(leftnode)
        h.append(rightnode)
    return Hamiltonian_path, Hamiltonian

def print_path(path_A):#打印分支限界法的输出
    path = path_A[0]
    print "length:"+str(path_A[1])
    num = len(path)
    next = [-1 for i in range(num)]
    last = [-1 for i in range(num)]
    for i in range(num):
        for j in range(i):
            if path[i][1]==path[j][0]:
                next[i] = j
                last[j] = i
                continue
            if path[i][0]==path[j][1]:
                next[j] = i
                last[i] = j
    it = 0
    print "path:"+str(path[it][0]),
    while next[it]!=0:
        it = next[it]
        print path[it][0],
    print path[it][1]

def logToDB(log):
    import MySQLdb
    con = 0
    cur = 0
    try:
        con = MySQLdb.connect(host = "localhost", user = "algorithm_user", passwd = "123456", db = "algorithm")
        cur = con.cursor()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    query = 'INSERT INTO `search` (`num`, `time`, `algorithm_id`) VALUES (%s, %s, %s)'
    cur.execute(query, log)
    con.commit()
    cur.close()
    con.close()

if __name__ == "__main__":
    figure = [[0,1,0,1,1],
              [1,0,1,1,1],
              [0,1,0,1,0],
              [1,1,1,0,0],
              [1,1,0,0,0]]
    figure2 = [[-1,3,93,13,33,9,57],
               [4,-1,77,42,21,16,34],
               [45,17,-1,36,16,28,25],
               [39,90,80,-1,56,7,91],
               [28,46,88,33,-1,25,57],
               [3,88,18,46,92,-1,7],
               [44,26,33,27,84,39,-1]]
    figure3 = [[-1,5,-1,-1,-1,-1],
               [-1,-1,5,-1,-1,-1],
               [10,-1,-1,12,-1,-1],
               [8,-1,-1,-1,-1,11],
               [-1,-1,-1,7,-1,9],
               [-1,-1,-1,-1,4,-1]]
    #while True:
    #    num = 7
    #    figure = random_figure(num, True)
    #    path1 = branch_cut(figure)
    #    print_path(path1)
    for i in range(100):
        for i in range(8, 21, 2):
            num = i
            figure = random_figure(num, True)
            #adj = adjacent(figure)
            t1 = Timer("print_path(branch_cut(figure))", "from __main__ import print_path, branch_cut; figure="+str(figure))
            T1 = t1.timeit(1)
            logToDB([num, T1, "branch_cut"])
        
    #if T1>T3:
    #    print "yes"
    #else:
    #    print "no"
    #if T2>T4:
    #    print "yes"
    #else:
    #    print "no"
    #print T1, T3
    #print T2, T4
    