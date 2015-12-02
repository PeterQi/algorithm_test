# coding: UTF-8
import random
import matplotlib.pyplot as plt
import math
from timeit import Timer
Pi = 3.14159265358979323846264338327
ZERO = 1e-11
def equal_zero(float_num):#判断浮点数是否可视为0
    if -ZERO<float_num<ZERO:
        return True
    else:
        return False

def random_points(length):#随机生成length数目的点
    points = []
    for i in range(length):
        x = random.uniform(0, 100)
        y = random.uniform(0, 100)
        the_point = (x,y)
        points.append(the_point)
    
    return points

def line_equation(point_A, point_B):#求直线方程
    line_coefficient = {"A":0, "B":0, "C":0}
    line_coefficient["A"] = point_B[1]-point_A[1]
    line_coefficient["B"] = point_A[0]-point_B[0]
    line_coefficient["C"] = -line_coefficient["A"]*point_A[0]-line_coefficient["B"]*point_A[1]
    
    return line_coefficient

def is_line2(point_A, point_B, point_C):#判断点C对于直线AB的位置
    AB = line_equation(point_A, point_B)
    return AB["A"]*point_C[0] + AB["B"]*point_C[1] + AB["C"]

def is_line(line_coefficient, point_C):#判断点C对于直线的位置
    return line_coefficient["A"]*point_C[0] + line_coefficient["B"]*point_C[1] + line_coefficient["C"]

def sortANDprint(points):#将得到的凸包顶点集合按照逆时针方向排序并输出
    num = len(points)
    if num <= 2:
        for i in range(num):
            print points[i]
        return
    min_x = points[0]
    max_x = points[0]
    for i in range(1, num):
        if points[i][0]<min_x[0]:
            min_x = points[i]
        if points[i][0]>max_x[0]:
            max_x = points[i]
    
    AB = line_equation(min_x, max_x)
    SL = []#AB下方的点集
    SU = []#AB上方的点集
    if AB["B"]>0:
        for i in range(0, num):
            if is_line(AB, points[i])>0:
                SU.append(points[i])
            else:
                SL.append(points[i])
    else:
        for i in range(0, num):
            if is_line(AB, points[i])<0:
                SU.append(points[i])
            else:
                SL.append(points[i])
    SL = sorted(SL, key=lambda p:p[0])
    SU = sorted(SU, key=lambda p:p[0], reverse=True)
    for i in SL:
        print i
    for j in SU:
        print j
    return SL+SU

def sGrahamScan(points):#无需极角排序的Graham-Scan算法
    result_points = []
    num = len(points)
    if num <=3:
        return points
    result_points.append(points[0])
    result_points.append(points[1])
    result_points.append(points[2])
    for i in range(3, num):
        while True:
            tmp_line = line_equation(points[i], result_points[-2])
            if len(result_points)<=2:
                break
            if is_line(tmp_line, points[0])*is_line(tmp_line, result_points[-1])>0:       
                result_points.pop()
            else:
                break
        result_points.append(points[i])
    return result_points

def angle_sort(points):#将点按照极角排序，极点是纵坐标最小的点，极轴平行于x轴
    min_y_P = 0
    num = len(points)
    if (num == 1):
        return points
    for i in range(1, num):
        if points[i][1]<points[min_y_P][1]:
            min_y_P = i
    points2 = []
    for i in range(0, num):
        if i == min_y_P:
            points2.append([i, -4])
            continue
        if points[i][0] == points[min_y_P][0]:
            points2.append([i, Pi/2])
            continue
        if points[i][1] == points[min_y_P][1]:
            if points[i][0]>points[min_y_P][0]:
                points2.append([i, 0])
            else:
                points2.append([i, Pi])
            continue
        iP = line_equation(points[i], points[min_y_P])
        angle = math.atan(float(-iP["A"])/iP["B"])
        if angle < 0:
            angle += Pi
        points2.append([i, angle])
    points2 = sorted(points2, key=lambda p:p[1])
    sorted_points = []
    last_point_angle = points2[0][1]
    last_point = points[points2[0][0]]
    
    for i in range(1, num):
        if points2[i][1] != last_point_angle:#极角不同的顶点则可以插入
            sorted_points.append(last_point)
            last_point_angle = points2[i][1]
            last_point = points[points2[i][0]]
        else:
            x_compare = math.fabs(points[points2[i][0]][0] - points[points2[0][0]][0]) - math.fabs(last_point[0] - points[points2[0][0]][0])>0
            y_compare = math.fabs(points[points2[i][0]][1] - points[points2[0][0]][1]) - math.fabs(last_point[1] - points[points2[0][0]][1])>0
            if x_compare or y_compare:#极角相同的该点比上一个节点要更远
                last_point = points[points2[i][0]]
    sorted_points.append(last_point)
    return sorted_points

def find_k_point_X(points, k):#找到点集中横坐标第k小的点
    key = points[random.randint(0, len(points)-1)][0]
    num = len(points)
    a_points = []
    b_points = []
    for i_point in points:
        if i_point[0]<=key:
            a_points.append(i_point)
        else:
            b_points.append(i_point)
    if len(a_points)==k:
        return [key, a_points, b_points]
    elif len(a_points)>k:
        get_mid = find_k_point_X(a_points, k)
        return [get_mid[0], get_mid[1], get_mid[2]+b_points]
    else:
        get_mid = find_k_point_X(b_points, k-len(a_points))
        return [get_mid[0], a_points+get_mid[1], get_mid[2]]

def BruteForceCH1(points):#蛮力算法
    num = len(points)
    if  num == 3:
        sortANDprint(points)
        return points
    lines = [[0 for j in range(num)] for i in range(num)]
    for i in range(num):
        for j in range(i):
            lines[i][j] = line_equation(points[i], points[j])
            lines[j][i] = lines[i][j]
    convexHullIndexs = range(num)
    for i in range(num):
        for j in range(num):
            if j == i:
                continue
            for p in range(num):
                if p == j or p == i:
                    continue
                for q in range(num):
                    if q == p or q == j or q == i:
                        continue
                    ij_line = lines[i][j]
                    a_line = is_line(ij_line, points[p])
                    if equal_zero(a_line):#ijp三点成线
                        if equal_zero(is_line(ij_line, points[q])):#四点成线
                            if not(points[q][0]>points[i][0] and points[q][0]>points[j][0] and points[q][0]>points[p][0]):
                                if not(points[q][0]<points[i][0] and points[q][0]<points[j][0] and points[q][0]<points[p][0]):
                                    if points[q][0]==points[i][0]:#成一条垂直于x轴的线
                                        if not(points[q][1]>points[i][1] and points[q][1]>points[j][1] and points[q][1]>points[p][1]):
                                            if not(points[q][1]<points[i][1] and points[q][1]<points[j][1] and points[q][1]<points[p][1]):
                                                convexHullIndexs[q] = -1#删除该点
                                    else:
                                        convexHullIndexs[q] = -1#删除该点
                        continue
                    #ijp三点不成线
                    if is_line(ij_line, points[q])*is_line(ij_line, points[p])>=0:
                        ip_line = lines[i][p]
                        if is_line(ip_line, points[q])*is_line(ip_line, points[j])>=0:
                            jp_line = lines[j][p]
                            if is_line(jp_line, points[q])*is_line(jp_line, points[i])>=0:
                                convexHullIndexs[q] = -1#在ijp三角形内部或之上，删除该点
    convexHull = []
    for i in range(num):
        if (convexHullIndexs[i]>=0):
            convexHull.append(points[i])
    return sortANDprint(convexHull)                       

def GrahamScan(points):#Graham-Scan算法
    points = angle_sort(points)
    result_points = []
    num = len(points)
    if num <=3:
        for i in points:
            print i
        return points
    result_points.append(points[0])
    result_points.append(points[1])
    result_points.append(points[2])
    for i in range(3, num):
        while True:
            tmp_line = line_equation(points[i], result_points[-2])
            if len(result_points)<=2:
                break
            if is_line(tmp_line, points[0])*is_line(tmp_line, result_points[-1])>0:                
                #print points[i], result_points[-2], result_points[-1], points[0]
                result_points.pop()
                #print len(result_points)
            else:
                break
        result_points.append(points[i])
    for i in range(0, len(result_points)):
        print result_points[i]
    return result_points

def DivideConvexHull(points):#分治算法
    num = len(points)
    if num == 3:
        return angle_sort(points)
    if num == 2:
        if points[0][1]>points[1][1]:
            exPoints = [points[1], points[0]]
            return exPoints
        return points
    if num <= 1:
        return points
    get_mid = find_k_point_X(points, num/2)
    a_points = get_mid[1]
    b_points = get_mid[2]
    QL = DivideConvexHull(a_points)
    QR = DivideConvexHull(b_points)
    exflag = False
    if QL[0][1]<QR[0][1]:
        a_points = QL
        b_points = QR
    else:
        a_points = QR
        b_points = QL
        exflag = True
    a_points_angles = []
    b_points_angles = []
    b_points_angles1 = []
    b_points_angles2 = []
    for i in range(1, len(a_points)):
        if a_points[i][0] == a_points[0][0]:
            a_points_angles.append([i, Pi/2])
            continue
        if a_points[i][1] == a_points[0][1]:
            if a_points[i][0]>a_points[0][0]:
                a_points_angles.append([i, 0])
            else:
                a_points_angles.append([i, Pi])
            continue
        iP = line_equation(a_points[i], a_points[0])
        angle = math.atan(float(-iP["A"])/iP["B"])
        if angle < 0:
            angle += Pi
        a_points_angles.append([i, angle])
    b_min_p = 0
    b_max_p = 0
    b_num = len(b_points)
    for i in range(0, b_num):
        tmp_angle = 0
        if b_points[i][1]!=a_points[0][1]:
            iP = line_equation(b_points[i], a_points[0])
            tmp_angle = math.atan(float(-iP["A"])/iP["B"])
        if exflag:
            tmp_angle += Pi
        b_points_angles.append(tmp_angle)
        if tmp_angle < b_points_angles[b_min_p]:
            b_min_p = i
        if tmp_angle > b_points_angles[b_max_p]:
            b_max_p = i
    if b_max_p < b_min_p:
        b_max_p += b_num

    for j in range(0, b_max_p - b_min_p+1):
        i = (j + b_min_p) % b_num
        b_points_angles1.append([i, b_points_angles[i]])
    for i in range((b_max_p+1)% b_num, b_min_p):
        b_points_angles2.append([i, b_points_angles[i]])#逆序
    final_points = [a_points[0]]
    i = 0
    j = 0
    k = 0
    i_max = len(a_points_angles)
    j_max = len(b_points_angles1)
    k_max = len(b_points_angles2)
    while True:
        if i>=i_max and j>=j_max and k >= k_max:
            break
        A = []
        if i<i_max:
            A.append([0, a_points_angles[i]])
        if j<j_max:
            A.append([1, b_points_angles1[j]])
        if k<k_max:
            A.append([2, b_points_angles2[-1-k]])
        tmp_p = [3, [-1, 4]]
        for p in A:
            if p[1][1]<tmp_p[1][1]:
                tmp_p = p
        if tmp_p[0] == 0:
            final_points.append(a_points[tmp_p[1][0]])
            i += 1
        elif tmp_p[0] == 1:
            final_points.append(b_points[tmp_p[1][0]])
            j += 1
        elif tmp_p[0] == 2:
            final_points.append(b_points[tmp_p[1][0]])
            k += 1
        else:
            return False
    return sGrahamScan(final_points)

def printDivideResult(points):#打印分治算法的输出
    fP = DivideConvexHull(points)
    for i in fP:
        print i

def logToDB(log):
    import MySQLdb
    con = 0
    cur = 0
    try:
        con = MySQLdb.connect(host = "localhost", user = "algorithm_user", passwd = "123456", db = "algorithm")
        cur = con.cursor()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    query = 'INSERT INTO `convexhull` (`num`, `time`, `algorithm_id`) VALUES (%s, %s, %s)'
    cur.execute(query, log)
    con.commit()
    cur.close()
    con.close()

def printConvexHull(points, Divide, Graham, Brute = []):#画凸包
    plt.title("convexHull")
    plt.figure(1)
    x = []
    y = []
    for i in Divide:
        x.append(i[0])
        y.append(i[1])
    x.append(Divide[0][0])
    y.append(Divide[0][1])
    plt.subplot(221)
    plt.plot(x, y)
    x = []
    y = []
    for i in points:
        x.append(i[0])
        y.append(i[1])
        plt.plot(x, y, ".")
        
    x = []
    y = []
    for i in Graham:
        x.append(i[0])
        y.append(i[1])
    x.append(Graham[0][0])
    y.append(Graham[0][1])
    plt.subplot(222)
    plt.plot(x, y)
    x = []
    y = []
    for i in points:
        x.append(i[0])
        y.append(i[1])
        plt.plot(x, y, ".")
        
    if len(Brute)==0:
        plt.show()
        return
        
    x = []
    y = []
    for i in Brute:
        x.append(i[0])
        y.append(i[1])
    x.append(Brute[0][0])
    y.append(Brute[0][1])
    plt.subplot(223)
    plt.plot(x, y)
    x = []
    y = []
    for i in points:
        x.append(i[0])
        y.append(i[1])
        plt.plot(x, y, ".")
    plt.show()
if __name__ == "__main__":
    #for points_num in range(10000, 100000, 1000):
    points_num = 50
    points = random_points(points_num)
    c1 = DivideConvexHull(points)
    c2 = GrahamScan(points)
    c3 = BruteForceCH1(points)
    #printConvexHull(points, c1, c2)
    printConvexHull(points, c1, c2, c3)
    #print "Divide:"
    #t1 = Timer("printDivideResult(points)", "from __main__ import printDivideResult; points = "+str(points))
    #time1 = str(t1.timeit(1))
    #print "Time: "+time1+"s"
    ##logToDB([points_num, time1, 0])
    #print "GrahamScan:"
    #t2 = Timer("GrahamScan(points)", "from __main__ import GrahamScan; points = "+str(points))
    #time2 = str(t2.timeit(1))
    #print "Time: "+time2+"s"
    ##logToDB([points_num, time2, 1])
    #print "Brute:"
    #t3 = Timer("BruteForceCH1(points)", "from __main__ import BruteForceCH1; points = "+str(points))
    #time3 = str(t3.timeit(1))
    #print "Time: "+time3+"s"
    #logToDB([points_num, time3, 2])
    
    
    
    