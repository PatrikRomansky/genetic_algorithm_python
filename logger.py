import os
import time

def create_dir(dir_name = 'tmpDir'):
    DIR = os.getcwd()
    os.chdir( DIR + '\\out')

    try:
        os.mkdir(dir_name)        
    except:
        print("Directory " , dir_name ,  " already exists")
        pass
    
    os.chdir(DIR + '\\out\\' + dir_name)

    return DIR

def create_file(file_name = 'data', file_type = '.txt', data = []):
    f = open(file_name + file_type, 'w+')

    for item in data:
        f.write(item + '\n')

    f.close()

def log_data(data, file_name = 'data', file_type = '.txt'):
    f = open(file_name + file_type,"a+") 

    for item in data:
        f.write(item + '\n')

    f.close()

def get_intro(delimeter):
    intro = ''
    intro += ('###########################' + delimeter)
    intro += ('###########################' + delimeter)
    intro += ('###########################' + delimeter)

    intro += ('# ------ BENCHMARK ------ #' + delimeter)
    return intro


def log_benchmark_test(number_format, text_format, data):
    delimeter = '\n'
    data = get_intro(delimeter= delimeter)



def log_benchmark(ind_size = 0, pop_size = 0, new_ind = -1, max_gen = 0, init_time = 0, eva_time = 0, log_time = 0, all_time = 0):
    NUMBER_FORMAT = 8
    
    delimeter = '\n'
    data = get_intro(delimeter= delimeter)

    data += ('#    IND_SIZE  : ' + str(ind_size).zfill(NUMBER_FORMAT) + ' #' + delimeter)
    data += ('#    POP_SIZE  : ' + str(pop_size).zfill(NUMBER_FORMAT) + ' #' + delimeter)
    data += ('#    NEW_IND   : ' + str(new_ind + 1).zfill(NUMBER_FORMAT) + ' #' + delimeter)
    data += ('#    MAX_GEN   : ' + str(max_gen).zfill(NUMBER_FORMAT) + ' #' + delimeter)
    data += ('# ---- INIT ---- ' + time.strftime('%H:%M:%S', time.gmtime(init_time)) + ' #' + delimeter)
    data += ('# ---- EVA ----- ' + time.strftime('%H:%M:%S', time.gmtime(eva_time)) + ' #' + delimeter)
    data += ('# ---- LOG ----- ' + time.strftime('%H:%M:%S', time.gmtime(log_time)) + ' #' + delimeter)
    data += ('# ---- TIME ---- ' + time.strftime('%H:%M:%S', time.gmtime(all_time)) + ' #' + delimeter)
    
    data += ('###########################' + delimeter)
    data += ('###########################' + delimeter)
    data += ('###########################' + delimeter)

    f = open('benchmark.txt',"w+") 
    f.write(data)
    f.close()

def log_benchmark_all(name, ind_size = 0, max_gen = 0, log = 1, init_time = 0, eva_time = 0, render_time = 0, all_time = 0):
    NUMBER_FORMAT = 8

    delimeter = '\n'
    data = get_intro(delimeter= delimeter)
    data += ('# ------    ALL    ------ #' + delimeter)

    data += ('#    IND_SIZE  : ' + str(ind_size).zfill(NUMBER_FORMAT) + ' #' + delimeter)
    data += ('#    MAX_GEN   : ' + str(max_gen).zfill(NUMBER_FORMAT) + ' #' + delimeter)
    data += ('#    LOG       : ' + str(log).zfill(NUMBER_FORMAT) + ' #' + delimeter)
    data += ('# ---- INIT ---- ' + time.strftime('%H:%M:%S', time.gmtime(init_time)) + ' #' + delimeter)
    data += ('# ---- EVA ----- ' + time.strftime('%H:%M:%S', time.gmtime(eva_time)) + ' #' + delimeter)
    data += ('# ---- RENDER -- ' + time.strftime('%H:%M:%S', time.gmtime(render_time)) + ' #' + delimeter)
    data += ('# ---- TIME ---- ' + time.strftime('%H:%M:%S', time.gmtime(all_time)) + ' #' + delimeter)
    
    data += ('###########################' + delimeter)
    data += ('###########################' + delimeter)
    data += ('###########################' + delimeter)
    
    f = open('animations\\'+ name +'_benchmark.txt',"w+") 
    f.write(data)
    f.close()