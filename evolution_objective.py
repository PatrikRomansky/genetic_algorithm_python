import sys
import math
import functools
import numpy as np
# we can use multiprocessing to evaluate fitness in parallel
import multiprocessing
from progress.bar import Bar


def two_points_distance(X1, Y1, X2, Y2):
    # dinstance = sqrt[(X1-x2)^2 + (Y1-Y2)^2]
    # pre zrychlenie odmocninu odstranime a dame nasobenie naposto power2, oodmocnina y vacieho cisla je stale vacsie cislo 
    return  (X1 - X2)*(X1 - X2) + (Y1 - Y2)*(Y1 - Y2)

def two_lines_distance(a, b):

    dist1 = two_points_distance(X1 = a.X1, Y1 = a.Y1, X2 = b.X1, Y2 = b.Y1) + two_points_distance(X1 = a.X2, Y1 = a.Y2, X2 = b.X2, Y2 = b.Y2)

    dist2 = two_points_distance(X1 = a.X1, Y1 = a.Y1, X2 = b.X2, Y2 = b.Y2) + two_points_distance(X1 = a.X2, Y1 = a.Y2, X2 = b.X1, Y2 = b.Y1)

    return dist1 if dist1 < dist2 else dist2

def two_lines_distance_objective(a, b):
    if a[1] == False:
        return two_lines_distance(a[0], b)
    else: 
        return sys.maxsize


def nearest_lines_distance(gene, target, reserved, map_func):

    func_distance = functools.partial(two_lines_distance_objective, b = gene)

    
    values = list(map_func(func_distance, zip(target, reserved)))
    
    index_min = np.argmin(values)
    dist = values[index_min]
    return dist, index_min
    
"""
def recalculation_objective(ind, target):

    # parallel = multiprocessing.Pool()
    # map_f = parallel.map
    map_f = map
    sum_v = 0
    processed = 0
    
    indSize = ind.size
    targetSize = len(target)

    reserved = [False]*targetSize
    ind.obj_values = [None]*indSize

    for g in Bar('Fitness pre-processed').iter(ind.geneType):
        
        if  processed == targetSize:       
            reserved = [False]*targetSize

            
        dist, index = nearest_lines_distance(g, target, reserved, map_f)
        ind.obj_values[processed] = target[index], int(dist)
        
        reserved[index] = True
        
        sum_v += int(dist)    
        processed += 1

    ind.obj = sum_v

    return ind.obj
"""
def recalculation_objective(ind, target):
    indSize = ind.size
    ind.obj_values = [None]*indSize
    processed = 0
    sum_v = 0
    targetSize = len(target)
    

    for g in Bar('Fitness pre-processed').iter(ind.geneType):
        dist = two_lines_distance(g, target[processed % targetSize])
        ind.obj_values[processed] = target[processed % targetSize], int(dist)
        sum_v += int(dist)  
        processed += 1

    ind.obj = sum_v

    return ind.obj



def objective(ind, target = None):

    if ind.obj == None:
        recalculation_objective(ind, target)

    return ind.obj