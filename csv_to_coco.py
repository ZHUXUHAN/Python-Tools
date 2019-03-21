import os
import pandas as pd
from collections import OrderedDict
import cv2
import numpy as np
import json
gt_data_path =  "/home/priv-lab1/workspace/zxh/end2/csv/anno_box_train.csv"
hoi_list_path = "/home/priv-lab1/workspace/zxh/end2/origin_lists/hico_list_hoi.txt"
img_path = '/home/priv-lab1/workspace/zxh/My_Database/hico_20160224_det/images/train2015/'  # image folder path
save_json_path = 'train_hico.json'  # name for save json
_classes = ('person', 'bicycle', 'car', 'motorcycle', 'airplane',
               'bus', 'train', 'truck', 'boat', 'traffic_light',
               'fire_hydrant', 'stop_sign', 'parking_meter', 'bench', 'bird',
               'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
               'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
               'suitcase', 'frisbee', 'skis', 'snowboard', 'sports_ball',
               'kite', 'baseball_bat', 'baseball_glove', 'skateboard',
               'surfboard', 'tennis_racket', 'bottle', 'wine_glass', 'cup',
               'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
               'sandwich', 'orange', 'broccoli', 'carrot', 'hot_dog', 'pizza',
               'donut', 'cake', 'chair', 'couch', 'potted_plant', 'bed',
               'dining_table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
               'keyboard', 'cell_phone', 'microwave', 'oven', 'toaster',
               'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
               'teddy_bear', 'hair_drier', 'toothbrush')


df_gt_data = pd.DataFrame.from_csv(gt_data_path)
# str to list
df_gt_data['human_bbox'] = df_gt_data['human_bbox'].apply(lambda x: list(map(int, x.strip('[]').split(','))))
df_gt_data['obj_bbox'] = df_gt_data['obj_bbox'].apply(lambda x: list(map(int, x.strip('[]').split(','))))
df_gt_data['img_size_w_h'] = df_gt_data['img_size_w_h'].apply(lambda x: list(map(int, x.strip('[]').split(','))))

human_bbox_dict=OrderedDict()
object_bbox_dict=OrderedDict()
filenames=[]
action_dict=OrderedDict()
list_action=[]

for index,row in df_gt_data.iterrows():
    filenames.append(row['name'])
    if row['name'] in human_bbox_dict:
        human_bbox_dict[row['name']].append(row['human_bbox'])
        object_bbox_dict[row['name']].append(row['obj_bbox'])
        action_dict[row['name']].append(row['action_no'])
    else:
        human_bbox_dict[row['name']]=[row['human_bbox']]
        object_bbox_dict[row['name']] = [row['obj_bbox']]
        action_dict[row['name']] = [row['action_no']]
filenames=set(filenames)


with open(hoi_list_path,'r') as f :
    lines=f.readlines()
for line in lines[2:]:
    list_action.append(line.split())
print("data set done")
class Convert_csv_to_coco(object):
    def __init__(self,mode):
        # self.img_hoi = img_hoi_train
        # self.row_num=img_hoi_train.shape[0]#行数

        self.save_json_path = save_json_path
        self.mode=mode

        self.images = []
        self.categories = []
        self.annotations = []

        self.label_map = {}
        for i in range(len(_classes)):
            self.label_map[_classes[i]] = i

        self.annID = 1

        self.transfer_process()
        self.save_json()

    def transfer_process(self):
        # categories
        for i in range(0, len(_classes)):
            categories = {'supercategory': _classes[i], 'id': i,
                          'name': _classes[i]}

            self.categories.append(categories)


        for i,file in enumerate(filenames):
            if i% 100 == 0 or i==len(filenames)-1:
                print('CSV transfer process  {}'.format(str(i + 1)))
            data_name  = file

            if os.path.exists(img_path + data_name):
                img_p = cv2.imread(img_path + data_name )
                filename = data_name
                width = img_p.shape[1]
                height = img_p.shape[0]
            else:
                with open("./save.txt",'w') as f:
                    f.write(img_path + data_name)
                    print(img_path + data_name)


            def processing_ann( bbox):

                x1 = np.maximum(0.0, float(bbox[0]))
                y1 = np.maximum(0.0, float(bbox[2]))
                x2 = np.minimum(width - 1.0, float(bbox[1]))
                y2 = np.minimum(height - 1.0, float(bbox[3]))

                # rectangle = [x1, y1, x2, y2]
                bbox = [x1, y1, x2 - x1 + 1, y2 - y1 + 1]  # [x,y,w,h]
                area = (x2 - x1 + 1) * (y2 - y1 + 1)

                return bbox, area

            # images
            image = {'height': height, 'width': width, 'id': i, 'file_name': filename}
            self.images.append(image)

            obboxs = object_bbox_dict[file]
            actions = action_dict[file]
            for ii,hbbox in enumerate(human_bbox_dict[file]):


                h_x1 = hbbox[0]
                h_x2 = hbbox[1]
                h_y1 = hbbox[2]
                h_y2 = hbbox[3]
                human_bbox=[h_x1,h_x2,h_y1,h_y2]

                o_x1 = obboxs[ii][0]
                o_x2 = obboxs[ii][1]
                o_y1 = obboxs[ii][2]
                o_y2 = obboxs[ii][3]
                obj_bbox=[o_x1,o_x2,o_y1,o_y2]
                #
                label = list_action[actions[ii]-1][1]


                human_bbox,human_bbox_area=processing_ann(human_bbox)
                human_annotation = {'segmentation': [], 'iscrowd': 0, 'area': human_bbox_area, 'image_id': i,
                                            'bbox': human_bbox, 'difficult': 0,
                                            'category_id': self.label_map['person'], 'id': self.annID}
                self.annotations.append(human_annotation)
                self.annID += 1

                obj_bbox, obj_bbox_area = processing_ann(obj_bbox)
                obj_annotation = {'segmentation': [], 'iscrowd': 0, 'area': obj_bbox_area, 'image_id': i,
                                'bbox': obj_bbox, 'difficult': 0,
                                'category_id': self.label_map[label], 'id': self.annID}
                self.annotations.append(obj_annotation)
                self.annID += 1

    def save_json(self):
        data_coco = {'images': self.images, 'categories': self.categories, 'annotations': self.annotations}
        json.dump(data_coco, open(self.save_json_path, 'w'), indent=4)

if __name__ == '__main__':
    Convert_csv_to_coco('train')
