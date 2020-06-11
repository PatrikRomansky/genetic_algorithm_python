import cv2
import math
import numpy as np

def detect_edges(img, minVal = 20, maxVal = 50, aperture_Size = 3, L2_gradient = True):
   
    height, width = img.shape

    edges = cv2.Canny(img, minVal, maxVal, apertureSize = aperture_Size, L2gradient = L2_gradient)
    
    return edges, height, width

# rho - distance resolution in pixels of the Hough grid
# theta - angular resolution in radians of the Hough grid
# threshold - minimum number of votes (intersections in Hough grid cell)
# min_line_length - minimum number of pixels making up a line
# max_line_gap - maximum gap in pixels between connectable line segments
# def detect_lines(edges, rho = 7, theta = np.pi / 180, threshold = 20, min_line_length = 10, max_line_gap = 40):
# def detect_lines(edges, rho = 7, theta = np.pi / 180, threshold = 100, min_line_length = 20, max_line_gap = 40):
def detect_lines(edges, rho = 7, theta = np.pi / 180, threshold = 150, min_line_length = 40, max_line_gap = 60):
    # Run Hough on edge detected image
    # Output "lines" is an array containing endpoints of detected line segments
    lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                        min_line_length, max_line_gap)
    return lines
