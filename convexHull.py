# coding: UTF-8
import random
def random_points(length):
    points = []
    for i in range(length):
        x = random.uniform(0, 100)
        y = random.uniform(0, 100)
        the_point = (x,y)
        points.append(the_point)
    
    return points
