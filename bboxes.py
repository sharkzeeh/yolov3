import os
from PIL import Image
import skimage.io as io

label_path = '../wider/labels'
boxes = ['../wider/images/wider_face_split/wider_face_' + s for s in ['train_bbx_gt.txt', 'val_bbx_gt.txt']]
IMAGES_DIR = ['../wider/images/WIDER_' + s for s in ['train', 'val']]

if not os.path.exists(label_path):
    os.makedirs(label_path)

def names():
    ANNOTS = [None] * 2
    size = [None] * 2
    for i in range(len(boxes)):
        with open(boxes[i], 'r') as fh:
            ANNOTS[i] = fh.readlines()
            size[i] = len(ANNOTS[i])

    for j in range(len(IMAGES_DIR)):

        i = 0
        cur_ANNOTS = ANNOTS[j]
        while i < size[j]:
            face_num = int(cur_ANNOTS[i + 1]) # count how many faces are in the pic  
            """E.g: 0--Parade/0_Parade_marchingband_1_465.jpg
            126
            345 211 4 4 2 0 0 0 2 0 
            331 126 3 3 0 0 0 1 0 0 
            250 126 3 4 2 0 0 0 2 0 
            221 128 4 5 0 0 0 1 0 0 
            ...
            """
            name = cur_ANNOTS[i][:-1] # an image name with a path (strip newline)
            """
            E.g. 0--Parade/0_Parade_marchingband_1_465.jpg
            """
            actual_name = name.split('/')[1] # just an image name
            """0_Parade_marchingband_1_465.jpg"""

            
            IMG = IMAGES_DIR[j] + '/' + actual_name # after using flattener.sh, one has to join like this
            width, height = Image.open(IMG).size
            width, height = float(width), float(height)

            if face_num > 750: # just to make sure everything is working fine
                print(name, face_num)
            
            PREFIX = label_path + '/' + IMAGES_DIR[j].split('/')[3] # add WIDER_train or WIDER_val dirs to label dir
            LABEL = PREFIX + '/' + actual_name[:-4] # a label name has no extension in it (we'll need to convert it to txt format just below)

            if not os.path.exists(PREFIX):
                os.mkdir(PREFIX)

            with open(LABEL + '.txt', 'w') as f:
                if not face_num:
                    f.write('0' + ' ')
                    f.write('0.0' + ' ')
                    f.write('0.0' + ' ')
                    f.write('0.0' + ' ')
                    f.write('0.0' + '\n')

                for n in range(face_num):
                    s = cur_ANNOTS[i + 2 + n].split()
                    x = float(s[0])
                    y = float(s[1])
                    w = float(s[2])
                    h = float(s[3])

                    if x < 0:
                        x = 0
                    if y < 0:
                        y = 0
                    if w < 0:
                        w = 0
                    if h < 0:
                        h = 0
                    cx = x + 0.5 * w
                    cy = y + 0.5 * h
                    vocX = cx / width if cx / width <= 1.0 else 1.0
                    vocY = cy / height if cy / height <= 1.0 else 1.0
                    vocW = w / width if w / width <= 1.0 else 1.0
                    vocH = h / height if h / height <= 1.0 else 1.0
                    f.write('0' + ' ')
                    f.write(str(vocX) + ' ')
                    f.write(str(vocY) + ' ')
                    f.write(str(vocW) + ' ')
                    f.write(str(vocH) + '\n')

            if not face_num:
                i += 3
            else:
                i += int(face_num) + 2


if __name__ == "__main__":
    names()
