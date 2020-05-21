from pycocotools.coco import COCO
import urllib.request
import shutil
import numpy as np
import skimage.io as io
import cv2


annFile='/home/xuhanzhu/mmdetection/data/wheat_detection/annotations/train.json'
coco=COCO(annFile)


# catIds = coco.getCatIds(catNms=['dog','bicycle'])
imgIds = coco.getImgIds(imgIds=[1])
print(imgIds)
img = coco.loadImgs(imgIds)
print(img)
print(img[0]['file_name'])
im = cv2.imread(os.path.join('/home/xuhanzhu/mmdetection/data/wheat_detection/train', img[0]['file_name']))
print(os.path.exists("/home/xuhanzhu/mmdetection/data/wheat_detection/train" + img[0]['file_name']))
annIds = coco.getAnnIds(imgIds=img[0]['id'])

anns = coco.loadAnns(annIds)
print(anns)

for ann in anns:
    x1 = int(ann['bbox'][0])
    y1 = int(ann['bbox'][1])
    x2 = int(x1+ann['bbox'][2])
    y2 = int(y1 + ann['bbox'][3])
    cv2.rectangle(im, (x1,y1),(x2,y2), (0,0,255), 2)
cv2.imwrite('k.png',im)
