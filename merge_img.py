import cv2
import numpy as np
import os

img_matrix = []
dir = '/home/awesome-semantic-segmentation-pytorch/scripts/img_align_r18'
img_files = os.listdir(dir)
out_dir = './matrix_r18'
if not os.path.exists(out_dir):
    os.makedirs(out_dir)
for idx, img_path in enumerate(img_files):
    path = os.path.join(dir, img_path)
    img_g = cv2.imread(path)
    img_matrix.append(img_g)

    if idx != 0 and idx % 10 == 0:
        img_matrix = np.concatenate(img_matrix, axis=1)
        cv2.imwrite(os.path.join(out_dir, "%d.png" % idx), img_matrix)
        img_matrix = []
