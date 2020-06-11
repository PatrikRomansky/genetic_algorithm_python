import os
import cv2
import numpy as np
import image_canny as can
import evolution_target as trarget

def edges_parm(minVal = 2250, maxVal = 2700, aperture_Size = 5, L2_gradient = True):
    return minVal, maxVal, aperture_Size, L2_gradient

def lines_parm(rho = 7, threshold = 150, min_line_length = 40, max_line_gap = 60):
    return rho, threshold, min_line_length, max_line_gap

def processing(input_file, folder, edges_parameter, lines_parameter):

    ind = None
    
    path_input = '\\resources_evolution'
    if folder != '':
        path_input += '\\' + folder

    cur_dir = os.getcwd()

    os.chdir(cur_dir + path_input)

    minVal, maxVal, aperture_Size, L2_gradient = edges_parameter

    rho, threshold, min_line_length, max_line_gap = lines_parameter

    target = [img for img in os.listdir('.') 
            if img.startswith(input_file) and 
                (img.endswith(".jpg") or
                img.endswith(".jpeg") or
                img.endswith("png"))]

    for t in target:

        img = cv2.imread(t, 0)

        edges, height, width = can.detect_edges(img, minVal = minVal, maxVal = maxVal, aperture_Size = aperture_Size, L2_gradient = L2_gradient)

        lines = can.detect_lines(edges, rho = rho, threshold= threshold, min_line_length= min_line_length, max_line_gap= max_line_gap)

        ind = trarget.Target(size = len(lines), height = height, width = width, inputGene = lines)

    os.chdir(cur_dir)

    return ind