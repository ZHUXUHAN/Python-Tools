import cv2
import numpy as np

img_big=cv2.imread('/Users/zhuxuhan/PycharmProjects/newbegin/1/01-01/01-4/GW1AM2_20170102_01D_PNMA_L3SGT36HA2220220_BT_H_N_01.png',0)
img_big_rgb=cv2.imread('/Users/zhuxuhan/PycharmProjects/newbegin/1/01-01/01-4/GW1AM2_20170102_01D_PNMA_L3SGT36HA2220220_BT_H_N_01.png')
img_small=cv2.imread('/Users/zhuxuhan/PycharmProjects/newbegin/1/01-01/calendar_SR_2019-05-07_21-54-28--01/rgb_002.png',0)

template=img_small

res = cv2.matchTemplate(img_big,template,cv2.TM_CCOEFF_NORMED)
threshold = 0.99
loc = np.where(res >= threshold)
index=list(zip(*loc[::-1]))[0]
print(index)
img_big_copy=img_big_rgb.copy()
cv2.rectangle(img_big_copy, index, (index[0] + 640, index[1] + 480), (0,255,0), 1)
img_sample=img_big[index[1]:index[1]+480,index[0]:index[0]+640]
cv2.imwrite('sampe.png',img_sample)
cv2.imwrite('sampe_big.png',img_big_copy)
