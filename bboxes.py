import os
from PIL import Image
import skimage.io as io

label_path = '../wider/labels'
boxes = ['../wider/images/wider_face_split/wider_face_' + s for s in ['train_bbx_gt.txt', 'val_bbx_gt.txt']]
IMAGES = ['../wider/images/WIDER_' + s for s in ['train', 'valid']]

if not os.path.exists(label_path):
    os.makedirs(label_path)

def names():
    ANNOTS = [None] * 2
    size = [None] * 2
    for i in range(len(boxes)):
        with open(boxes[i], 'r') as fh:
            ANNOTS[i] = fh.readlines()
            size[i] = len(ANNOTS[i])

    for j in range(len(IMAGES)):

        i = 0
        cur_ANNOTS = ANNOTS[j]
        while i < size[j]:

            face_num = int(cur_ANNOTS[i + 1])
            # if not face_num:
            #     i += 3
            #     continue

            name = cur_ANNOTS[i][:-1] # ваще полное имя
            actual_name = name.split('/')[1] # просто имя
            
            IMG = IMAGES[j] + '/' + actual_name
            width, height = Image.open(IMG).size
            width, height = float(width), float(height)

            if face_num > 750:
                print(name, face_num)
            
            PREF = label_path + '/' + IMAGES[j].split('/')[3]
            LABEL = PREF + '/' + actual_name[:-4]

            if not os.path.exists(PREF):
                os.mkdir(PREF)

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
                    # if x <= 0.0:
                    #     x = 0.001
                    # if y <= 0.0:
                    #     y = 0.001
                    # if w <= 0.0:
                    #     w = 0.001
                    # if h <= 0.0:
                    #     h = 0.001
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
