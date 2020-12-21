import os
import cv2
import shutil
from pycocotools.coco import COCO


def copy_some_imgs(json, class_name, path, to_path):
    annFile = json
    coco = COCO(annFile)
    catIds = coco.getCatIds(catNms=[class_name])
    imgIds = coco.getImgIds(catIds=catIds)
    imgs = coco.loadImgs(ids=imgIds)
    AnnIds = coco.getAnnIds(catIds=catIds)
    Anns = coco.loadAnns(ids=AnnIds)
    for i, img in enumerate(imgs):
        filename = img['file_name']
        shutil.copy(os.path.join(path, filename), os.path.join(to_path, filename))
        if i%20==0:
            print("i-th %d img saved" % i)


jsonpath = '/zhuxuhan/mscoco2014/annotations/instances_val2014.json'
imgpath = '/zhuxuhan/mscoco2014/val2014'
class_name = 'person'
save_path = '/zhuxuhan/14val_person'
copy_some_imgs(jsonpath, class_name, imgpath, save_path)
