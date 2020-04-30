from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import h5py
import json
import os
import scipy.misc
import sys
import re
import fnmatch
import datetime
from PIL import Image
import numpy as np
from script import parse_wider_gt

def convert_wider_annots(data_dir, out_dir):
    """Convert from WIDER FDDB-style format to COCO bounding box"""

    INFILE = "wider_face_val_bbx_gt.txt"
    OUTFILE = "val.json"

    if not os.path.exists('../wider/annotations'):
        os.makedirs('../wider/annotations')

    img_id = 0
    ann_id = 0
    cat_id = 1

    print('Starting WIDER')
    ann_dict = {}
    categories = [{"id": 1, "name": 'face'}]
    images = []
    annotations = []
    ann_file = os.path.join(data_dir, INFILE)
    wider_annot_dict = parse_wider_gt(ann_file) # [im-file] = [[x,y,w,h], ...]
    for filename in wider_annot_dict.keys():
        if len(images) % 50 == 0:
            print("Processed %s images, %s annotations" % (
                len(images), len(annotations)))
        
        image = {}
        image['id'] = img_id
        img_id += 1
        im = Image.open(filename) # numpy=1.17.4
        image['width'] = im.height
        image['height'] = im.width
        image['file_name'] = filename
        images.append(image)

        for gt_bbox in wider_annot_dict[filename]:
            print(gt_bbox)
            ann = {}
            ann['id'] = ann_id
            ann_id += 1
            ann['image_id'] = image['id']
            ann['segmentation'] = []
            ann['category_id'] = cat_id # 1:"face" for WIDER
            ann['iscrowd'] = 0
            ann['area'] = gt_bbox[2] * gt_bbox[3]
            ann['bbox'] = gt_bbox
            annotations.append(ann)

    ann_dict['images'] = images
    ann_dict['categories'] = categories
    ann_dict['annotations'] = annotations
    print("Num categories: %s" % len(categories))
    print("Num images: %s" % len(images))
    print("Num annotations: %s" % len(annotations))
    with open(os.path.join(out_dir, OUTFILE), 'w', encoding='utf8') as outfile:
        outfile.write(json.dumps(ann_dict))

if __name__ == '__main__':
    convert_wider_annots('../wider/images/wider_face_split', '../wider/annotations')
