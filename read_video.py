# coding=utf-8

import os
import cv2

videos_src_path = "./jiashi"
video_formats = [".mp4", ".MOV"]
frames_save_path = "./jiashizhen/"
width = 320
height = 240
time_interval = 1


def video2frame(video_src_path, formats, frame_save_path, frame_width, frame_height, interval):
    """
    将视频按固定间隔读取写入图片
    :param video_src_path: 视频存放路径
    :param formats:　包含的所有视频格式
    :param frame_save_path:　保存路径
    :param frame_width:　保存帧宽
    :param frame_height:　保存帧高
    :param interval:　保存帧间隔
    :return:　帧图片
    """
    videos = os.listdir(video_src_path)
    print(videos)

    def filter_format(x, all_formats):
        if x[-4:] in all_formats:
            return True
        else:
            return False



    videos = filter(lambda x: filter_format(x, formats), videos)


    for each_video in videos:
        try:

            print
            "正在读取视频：", each_video

            each_video_name = each_video[:-4]
            if not os.path.exists(frame_save_path + each_video_name):
                os.makedirs(frame_save_path + each_video_name)
            each_video_save_full_path = os.path.join(frame_save_path, each_video_name) + "/"

            each_video_full_path = os.path.join(video_src_path, each_video)

            cap = cv2.VideoCapture(each_video_full_path)
            frame_index = 0
            frame_count = 0
            print("dadada")
            if cap.isOpened():
                success = True

            else:
                success = False
                print("读取失败!")

            while (success):

                success, frame = cap.read()
                print
                "---> 正在读取第%d帧:" % frame_index, success

                if frame_index % interval == 0:
                    resize_frame = cv2.resize(frame, (frame_width, frame_height), interpolation=cv2.INTER_AREA)
                    # cv2.imwrite(each_video_save_full_path + each_video_name + "_%d.jpg" % frame_index, resize_frame)
                    cv2.imwrite(each_video_save_full_path + "%s.jpg" % str(frame_count).zfill(6), resize_frame)
                    print(each_video_save_full_path + "%s.jpg" % str(frame_count).zfill(6))
                    frame_count += 1

                frame_index += 1
        except:
            continue

    cap.release()


if __name__ == '__main__':
    video2frame(videos_src_path, video_formats, frames_save_path, width, height, time_interval)

