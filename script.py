import os
from PIL import Image

def parse_wider_gt(val_boxes='../wider/images/wider_face_split/wider_face_val_bbx_gt.txt'):
    label_path = '../wider/labels'
    val_IMAGEDIR = '../wider/images/WIDER_val'

    if not os.path.exists(label_path):
        os.makedirs(label_path)

    dct = {}

    val_ANNOTS = []
    num_lines = 0

    with open(val_boxes, 'r') as fh:
        val_ANNOTS = fh.readlines()
        num_lines = len(val_ANNOTS)

    ######################################################
    i = 0
    while i < num_lines:
        face_num = int(val_ANNOTS[i + 1]) # count how many faces are in the pic  
        """E.g: 0--Parade/0_Parade_marchingband_1_465.jpg
        126
        345 211 4 4 2 0 0 0 2 0 
        331 126 3 3 0 0 0 1 0 0 
        250 126 3 4 2 0 0 0 2 0 
        221 128 4 5 0 0 0 1 0 0 
        ...
        """
        name = val_ANNOTS[i][:-1] # an image name with a path (strip newline)
        """
        E.g. 0--Parade/0_Parade_marchingband_1_465.jpg
        """
        actual_name = name.split('/')[1] # just an image name
        """0_Parade_marchingband_1_465.jpg"""

        
        IMG = val_IMAGEDIR + '/' + actual_name # after using flattener.sh, one has to join like this
        width, height = Image.open(IMG).size
        width, height = float(width), float(height)

        # if face_num > 50: # just to make sure everything is working fine
        #     print(name, face_num)

        if not face_num:
            zeroes = [0, 0, 0, 0]
            if IMG not in dct:
                dct[IMG] = [zeroes]
        for n in range(face_num):
            s = val_ANNOTS[i + 2 + n].split()
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

            coords = [vocX, vocY, vocW, vocH]
            if IMG not in dct:
                dct[IMG] = [coords]
            else:
                dct[IMG].append(coords)

        if not face_num:
            i += 3
        else:
            i += int(face_num) + 2

    return dct


if __name__ == "__main__":
    print(parse_wider_gt())
