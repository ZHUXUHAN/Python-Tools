from pycocotools.coco import COCO
coco=COCO('/home/priv-lab1/workspace/zxh/pet/PytorchEveryThing/data/coco/annotations/instances_val2017.json')
category_ids = coco.getCatIds()
print("name", category_ids)
categories = [c['name'] for c in coco.loadCats(category_ids)]
print(categories)
