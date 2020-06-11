import logger as logger
import image_viewer as viewer
import image_processing as imageProcessing

path_input = 'resources_evolution/'

file = ''
folder = ''

if folder != '':
    path_input += '\\' + folder + '\\'


print('Test params: ' + file)
minVal = 15_000 
maxVal = 20_000
aperture_Size = 7
L2_gradient = True

rho = 7
threshold = 2
min_line_length = 2
max_line_gap = 4

# parameters for Target detection
edges_parameter = imageProcessing.edges_parm(minVal, maxVal, aperture_Size, L2_gradient)
lines_parameter = imageProcessing.lines_parm(rho, threshold, min_line_length, max_line_gap)


target = imageProcessing.processing(file, folder, edges_parameter, lines_parameter)
print('IND_SIZE: ' + str(target.size))
print('Height: ' + str(target.height))
print('Width: '+ str(target.width))

viewer.show_individual(target)

viewer.save_image(viewer.draw_individual(target), name='tmp/' + file + '_size_' +str(target.size))

# make params-file for input image
data = []
data.append(file)
data.append('edges_parameter')
data.append('minVal= ' + str(minVal))
data.append('maxVal= ' + str(maxVal))
data.append('aperture_Size= ' + str(aperture_Size))
data.append('L2_gradient= ' + str(L2_gradient))

data.append('lines_parameter')
data.append('rho= ' + str(rho))
data.append('threshold= ' + str(threshold))
data.append('min_line_length= ' + str(min_line_length))
data.append('max_line_gap= ' + str(max_line_gap))

logger.create_file(file_name= path_input + file, data= data)