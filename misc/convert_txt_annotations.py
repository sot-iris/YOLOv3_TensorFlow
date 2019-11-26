##Authored by Sotiris Kakanos, Github: http://github.com/sot-iris

import random
import os
import subprocess
import sys
import cv2
import cv2
import matplotlib.pyplot as plt
import argparse
#make sure the .txt file annoations are in the same directory as the images

parser = argparse.ArgumentParser(description="YOLO-V3 conversion from .txt files to applicable format")

parser.add_argument("--directory", type=str, default="",
                    help="Directory of images along with their respective text files generated from LabelImg.")
parser.add_argument("--dest", type=str, default="",
                    help="Where the validation and text files will go.")


args = parser.parse_args()

def imShow(path, y_min, y_max, x_min, x_max):
    image = cv2.imread(path+".png")
    height, width = image.shape[:2]

    resized_image = cv2.resize(image[y_min:y_max,x_min:x_max],(3*width, 3*height), interpolation = cv2.INTER_CUBIC)

    fig = plt.gcf()
    fig.set_size_inches(18, 10)
    plt.axis("off")
    #plt.rcParams['figure.figsize'] = [10, 5]
    plt.imshow(cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB))
    plt.show()

def get_info_from_txt_file(path, w, h):
    info = open("{}.txt".format(path), "r")
    items = ""
    for i in info:
        object_id = 0

        centre_x = (float(i.split(" ")[1]) * w)
        centre_y = (float(i.split(" ")[2]) * h)
        width_box = (float(i.split(" ")[3]) * w)
        height_box = (float(i.split(" ")[4]) * h)

        x_min = centre_x - (width_box/2)
        y_min = centre_y - (height_box/2)
        x_max = centre_x + (width_box/2)
        y_max = centre_y + (height_box/2)
        #imShow(path, int(y_min), int(y_max), int(x_min), int(x_max))
        items += str(object_id) + " "
        items += str(int(x_min)) + " "
        items += str(int(y_min)) + " "
        items += str(int(x_max)) + " "
        items += str(int(y_max)) + " "
    return items

def split_data_set(image_dir):
    base = args.dest
    f_val = open("{}/val.txt".format(base), 'w')
    f_train = open("{}/train.txt".format(base), 'w')

    path, dirs, files = next(os.walk(image_dir))
    data_size = len(files)

    ind = 0
    data_test_size = int(0.1 * data_size)
    test_array = random.sample(range(data_size), k=data_test_size)

    for f in os.listdir(image_dir):
        if(f.split(".")[1] == "png"):
            #h, w, chans = cv2.imread(image_dir+'/'+f).shape
            h, w = 600, 800 #if all the image sizes are the same...
            if ind in test_array:
                data = ("{} {}/{} {} {} {}".format(ind, image_dir, f, w, h ,(get_info_from_txt_file(image_dir+'/'+f.split(".")[0], w, h))).rstrip())
                f_val.write(data+'\n')
            else:
                data = ("{} {}/{} {} {} {}".format(ind, image_dir, f, w, h ,(get_info_from_txt_file(image_dir+'/'+f.split(".")[0], w, h))).rstrip())
                f_train.write(data+'\n')
            ind += 1
            print(data)

split_data_set(args.directory)
print("done")
