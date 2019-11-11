import random
import os
import subprocess
import sys
import cv2

def get_info_from_txt_file(path, w, h):
    info = open("{}.txt".format(path), "r")
    items = ""
    for i in info:
        object_id = i.split(" ")[0]

        centre_x = (float(i.split(" ")[1]) * w)
        centre_y = (float(i.split(" ")[2]) * h)
        width_box = (float(i.split(" ")[3]) * w)
        height_box = (float(i.split(" ")[4]) * h)

        x_min = centre_x - (width_box/2)
        y_min = centre_y - (height_box/2)
        x_max = centre_x + (width_box/2)
        y_max = centre_y + (height_box/2)
        items += str(object_id) + " "
        items += str(int(x_min)) + " "
        items += str(int(y_min)) + " "
        items += str(int(x_max)) + " "
        items += str(int(y_max)) + " "
    return items

def split_data_set(image_dir):
    f_val = open("/content/drive/Shared drives/RD Deep Learning/YOLO/darknet/val.txt", 'w')
    f_train = open("/content/drive/Shared drives/RD Deep Learning/YOLO/darknet/train.txt", 'w')

    path, dirs, files = next(os.walk(image_dir))
    data_size = len(files)

    ind = 0
    data_test_size = int(0.1 * data_size)
    test_array = random.sample(range(data_size), k=data_test_size)

    for f in os.listdir(image_dir):
        if(f.split(".")[1] == "png"):
            h, w, chans = cv2.imread(image_dir+'/'+f).shape
            ind += 1
            if ind in test_array:
                data = ("{} {}/{} {} {} {}".format(ind, image_dir, f, w, h ,(get_info_from_txt_file(image_dir+'/'+f.split(".")[0], w, h))).rstrip())
                f_val.write(data+'\n')
            else:
                data = ("{} {}/{} {} {} {}".format(ind, image_dir, f, w, h ,(get_info_from_txt_file(image_dir+'/'+f.split(".")[0], w, h))).rstrip())
                f_train.write(data+'\n')
            print(data)


split_data_set("/content/drive/Shared drives/RD Deep Learning/YOLO/darknet/data/labels")
print("done")
