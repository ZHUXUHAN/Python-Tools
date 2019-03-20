from __future__ import print_function
from pycocotools.coco import COCO
import os, sys, zipfile
import urllib.request
import shutil
import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt
import pylab
import cv2
plt.switch_backend('agg')

pylab.rcParams['figure.figsize'] = (8.0, 10.0)

annFile='/home/priv-lab1/workspace/gy_pet/PytorchEveryThing/data/cityscapes/val.json'
coco=COCO(annFile)


# catIds = coco.getCatIds(catNms=['dog','bicycle'])
imgIds = coco.getImgIds(imgIds=[1])
print(imgIds)
img = coco.loadImgs(imgIds)
print(img)
print(img[0]['file_name'])
im = cv2.imread(os.path.join('/home/priv-lab1/workspace/gy_pet/PytorchEveryThing/data/cityscapes/images/', img[0]['file_name']))
print(os.path.exists("/home/priv-lab1/workspace/gy_pet/PytorchEveryThing/data/cityscapes/images/" + img[0]['file_name']))

# I = io.imread(os.path.join('/home/priv-lab1/workspace/zxh/My_Database/hico_20160224_det/images/train',img[0]['file_name']))
# plt.imshow(I)
# plt.axis('off')
# ax = plt.gca()
# #
annIds = coco.getAnnIds(imgIds=img[0]['id'])

anns = coco.loadAnns(annIds)
print(anns)

# h_x1=int(anns[0]['bbox'][0])
# h_y1=int(anns[0]['bbox'][1])
# h_x2=int(h_x1+anns[0]['bbox'][2])
# h_y2=int(h_y1+anns[0]['bbox'][3])
# o_x1=int(anns[1]['bbox'][0])
# o_y1=int(anns[1]['bbox'][1])
# o_x2=int(o_x1+anns[1]['bbox'][2])
# o_y2=int(o_y1+anns[1]['bbox'][3])
for ann in anns:
    x1 = int(ann['bbox'][0])
    y1 = int(ann['bbox'][1])
    x2 = int(x1+ann['bbox'][2])
    y2 = int(y1 + ann['bbox'][3])
    cv2.rectangle(im, (x1,y1),(x2,y2), (0,0,255), 2)
cv2.imwrite('k.png',im)
# cv2.rectangle(im, (o_x1,o_y1),(o_x2,o_y2), (0,0,255), 2)
# #

#
# coco.showAnns(anns)
# plt.imshow(I)
# plt.savefig('j.png')
# plt.show()
