import os
import time
import logger as logger
import video_maker as video
from progress.bar import Bar
import evolution as evolution
import image_viewer as viewer
import image_txt_convertor as convertor
import image_processing as imageProcessing

def read_params_file(file_name, folder):
    
    path_input = '\\resources_evolution'
    if folder != '':
        path_input += '\\' + folder
    
    cur_dir = os.getcwd()
    os.chdir(cur_dir + path_input)

    f = open(file_name +'.txt', 'r')
    name = f.readline().rstrip()
    _ = f.readline().rstrip()
    minVal = int(f.readline().rstrip().split('=')[1])
    maxVal = int(f.readline().rstrip().split('=')[1])
    aperture_Size = int(f.readline().rstrip().split('=')[1])
    L2_gradient = bool(f.readline().rstrip().split('=')[1])

    edges_parameter = [minVal, maxVal, aperture_Size, L2_gradient]

    _ = f.readline().rstrip()
    rho = int(f.readline().rstrip().split('=')[1])
    threshold = int(f.readline().rstrip().split('=')[1])
    min_line_length = int(f.readline().rstrip().split('=')[1])
    max_line_gap = int(f.readline().rstrip().split('=')[1])

    lines_parameter = [rho, threshold, min_line_length, max_line_gap]

    f.close()
    os.chdir(cur_dir)

    return name, edges_parameter, lines_parameter

def init(files, folder = ''):
    data = []
    t_sizes = []

    for file in files:
        _ , edges_parameter, lines_parameter = read_params_file(file, folder = folder)
        target = imageProcessing.processing(file, folder= folder, edges_parameter= edges_parameter, lines_parameter= lines_parameter)
        data.append((file, target))
        t_sizes.append(target.size)

    return max(t_sizes), data

def run(target, input_file, max_gen, log, ind_size= None, pop= None, px_error = 1):


    print('Start evolution image: ' + input_file)
    # make dir
    DIR = logger.create_dir(dir_name= input_file)

    if ind_size == None:
        ind_size= target.size

    # evolution
    final_ind = evolution.run(target, height= target.height, width= target.width, ind_size= ind_size,
                                max_gen= max_gen, log= log, pop= pop, eva_name= input_file, px= px_error)  
    
    # save last best one
    viewer.save_image(viewer.draw_individual(final_ind[0]), name= 'final_ind')

    os.chdir(DIR)

    return final_ind

if __name__ == '__main__':
    
    # Start Timer
    start_time = time.time()
    print('Start: ' + time.strftime('%H:%M:%S', time.localtime(start_time)))
   
    # out_animation name
    eva_name = 'animation_eva'
    # number of generations for each evolution
    max_gen = 400_000
    # logger log data about each log-gen
    log = 1_000
    # Init final individual
    final = None

    px_error = 2

    files = ['1280x960_anaheim_ducks']
    folder = 'EVA_2'
    
    print('Animation for images:')

    i = 1
    for f in files:
        print(str(i) +'. '+f)
        i += 1

    print()

    # size of individual  
    maximal_size, targets = init(files, folder)
    # INIT TIME 
    eva_start = time.time()
    init_time  =  eva_start - start_time

    
    # EVOLUTION all Images
    for target in targets:
        file, t = target
        final = run(target= t,input_file = file, max_gen= max_gen, log= log, pop= final,
                        ind_size= maximal_size, px_error= px_error)

    # EVOLUTION TIME
    render_start = time.time()
    eva_time = render_start - eva_start

    # RENDER video
    video.generate_video(video_name= eva_name , folder= folder, input_files= files, fps = 20, orientation= 'horizontal')

    # RENDER
    render_time = time.time() - render_start
    all_time = time.time() - start_time

    logger.log_benchmark_all(name = eva_name, ind_size= maximal_size, max_gen= max_gen, log= log, 
                            init_time= init_time, eva_time= eva_time, render_time= render_time, all_time= all_time)