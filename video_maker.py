import gc
import os
import cv2
from progress.bar import Bar
import image_viewer as viewer
import image_txt_convertor as convertor

target_dir= ''
files_dir = ''

image_folder = '.' # make sure to use your folder 

def load_target(target_dir, f):
    image_folder = '.' # make sure to use your folder 
    os.chdir(target_dir)
        
    target = [img for img in os.listdir(image_folder) 
            if img.startswith(f) and 
                (img.endswith(".jpg") or
                img.endswith(".jpeg") or
                img.endswith("png"))][0]

    img_target = cv2.imread(os.path.join(image_folder, target)) 

    return img_target


def load_frames(files_dir):    
    image_folder = '.' # make sure to use your folder 
    # TODO : Oprav na textak
    os.chdir(files_dir)

    # Array images should only consider 
    # the image files ignoring others if any 
    images = [img for img in os.listdir(image_folder)
            if img.endswith(".jpg") or
                img.endswith(".jpeg") or
                img.endswith("png")] 
    return images

# orientaion frame : vertical/horizontal
def generate_video(video_name= 'animation', folder = '', input_files= [], fps= 4, source= True, orientation = 'horizontal'):
    
    print('Video maker')
    print('Processing: ' + str(len(input_files)) + ' files')
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    cur_dir = os.getcwd()
    global target_dir
    target_dir= cur_dir + '\\resources_evolution\\' 
    if folder != '':
        target_dir += folder + '\\'

    animation_dir = cur_dir + '\\animations\\'

    global files_dir 
    files_dir= cur_dir + '\\out\\'

    img_target = load_target(target_dir, input_files[0])
    
    if orientation == 'vertical':
        frame = cv2.vconcat([img_target, img_target])
    else:
        frame = cv2.hconcat([img_target, img_target])

    # setting the frame width, height width 
    # the width, height of first image 
    height, width, _ = frame.shape  

    video = cv2.VideoWriter(animation_dir + video_name +  '.avi', fourcc, fps, (width, height)) 

    if source:
        generate_video_txt(video_maker= video,orientation= orientation, input_files= input_files)
    else:
        generate_video_img(video_maker= video, orientation= orientation, input_files= input_files)

    # Deallocating memories taken for window creation 
    cv2.destroyAllWindows()  
    # releasing the video generated 
    video.release()
    
    os.chdir(cur_dir)

def generate_video_txt(video_maker, orientation, input_files= []): 
    index = 0
    for file in input_files:
        print(str(index) + '. Processing: ' + file)
        index += 1
        img_target = load_target(target_dir, file)

        f = open(files_dir + file + '\\gen.txt', 'r')
        number_of_gennerations = int(f.readline().rstrip())

        for _ in Bar('Video').iter(range(number_of_gennerations)): 
            
            gen = f.readline().rstrip()
            if gen != '':
                bi = convertor.convert_individual(f) 

                frame = viewer.draw_individual(bi, gen= 'Gen: ' + gen)
                frame = cv2.normalize(frame, None, 255, 0, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
                frame = cv2.merge([frame,frame,frame])

                if orientation == 'vertical':
                    frame = cv2.vconcat([frame, img_target])
                else:
                    frame = cv2.hconcat([frame, img_target])
                    # viewer.show_image(frame)
                    
                video_maker.write(frame) 
            else:
                break

        f.close()

# Video Generating function 
def generate_video_img(video_maker, orientation, input_files= []): 
    index = 0
    for file in input_files:
        print(str(index) + '. Processing: ' + file)
        index += 1
        img_target = load_target(target_dir, file)

        images = load_frames(files_dir + file)

        # Appending the images to the video one by one 
        for image in Bar('Video').iter(images):       
            frame = cv2.imread(os.path.join(image_folder, image)) 
           
            if orientation == 'vertical':
                frame = cv2.vconcat([frame, img_target])
            else:
                frame = cv2.hconcat([img_target, frame])           
            
            video_maker.write(frame)