import pickle
detections_file ='./300000_iCAN_ResNet50_VCOCO.pkl'
with open(detections_file, 'rb') as f:
    dets = pickle.load(f,encoding='bytes')
for det in dets:
    det.update({'eat_agent': det.pop(b"eat_agent")})
    det.update({'hit_agent': det.pop(b"hit_agent")})

    det.update({'cut_agent': det.pop(b"cut_agent")})
    det.update({'person_box': det.pop(b"person_box")})
    det.update({'image_id': det.pop(b"image_id")})
    det.update({'work_on_computer_agent': det.pop(b"work_on_computer_agent")})
    print(det.keys())
with open(detections_file, 'wb') as f:
    pickle.dump(dets,f)




