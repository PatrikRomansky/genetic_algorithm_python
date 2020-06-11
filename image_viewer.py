import cv2  
import math
import numpy as np

def get_clear_img(height, width):
    img_size = (height, width)
    return np.ones(img_size) * 255

# Black color in BGR 
# Line thickness of 1 px 
def draw_line(img, start_point, end_point, color = (0, 0, 0), thickness = 1):
    cv2.line(img, start_point, end_point, color, thickness) 

def draw_individual(ind, gen = ''):
    
    image = get_clear_img(height = ind.height, width = ind.width)
    
    for g in ind.geneType:
        draw_line(image,(g.X1, g.Y1), (g.X2, g.Y2))
        
    position = (ind.width - len(gen) *10, 15)

    cv2.putText(
        image, #numpy array on which text is written
        gen, # text
        position, #position at which writing has to start
        cv2.FONT_HERSHEY_SIMPLEX, #font family
        0.5, # font size
        (0, 0, 0, 0), # color 
        2) #font stroke

    return image

def show_image(image):
    cv2.imshow("image",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def show_individual(ind):
    img_IND = draw_individual(ind)
    show_image(img_IND)

def save_image(image, name = 'image', file_type= '.jpg'):
    cv2.imwrite(name + file_type, image)