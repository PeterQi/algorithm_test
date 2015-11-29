# coding: UTF-8
import random
import math
Pi = 3.14159265358979323846264338327
def random_points(length):
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
    
def is_line2(point_A, point_B, point_C):
    AB = line_equation(point_A, point_B)
    return AB["A"]*point_C[0] + AB["B"]*point_C[1] + AB["C"]
def is_line(line_coefficient, point_C):
    return line_coefficient["A"]*point_C[0] + line_coefficient["B"]*point_C[1] + line_coefficient["C"]
def sortANDprint(points):
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
            
def BruteForceCH1(points):
    num = len(points)
    if  num == 3:
        return points
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
                    ij_line = line_equation(points[i], points[j])
                    a_line = is_line(ij_line, points[p])
                    if a_line==0:#ijp三点成线
                        if is_line(ij_line, points[q])==0:#四点成线
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
                        ip_line = line_equation(points[i], points[p])
                        if is_line(ip_line, points[q])*is_line(ip_line, points[j])>=0:
                            jp_line = line_equation(points[j], points[p])
                            if is_line(jp_line, points[q])*is_line(jp_line, points[i])>=0:
                                convexHullIndexs[q] = -1#在ijp三角形内部或之上，删除该点
    convexHull = []
    for i in range(num):
        if (convexHullIndexs[i]>=0):
            convexHull.append(points[i])
    sortANDprint(convexHull)                            

#def GrahamScan(points):
def angle_sort(points):
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
    sorted_points = [points[points2[0][0]]]
    tmp_point_angle = points2[0][1]
    the_point = points2[0]
    dis = 0
    for i in range(1, num):
        if points2[i][1] == tmp_point_angle:
            
        sorted_points.append(points[points2[i][0]])
    return sorted_points
if __name__ == "__main__":
    #points_num = 1
    #points = random_points(points_num)
    #BruteForceCH1(points)
    points = [(0,0)]
    for i in range(-3, 4):
        for j in range(1, 4):
            points.append((i,j))
    points = angle_sort(points)
    for i in points:
        print i
            