# coding=utf-8

import os
import cv2


def video2frame(video_src_path, formats, frame_save_path, resize, frame_width, frame_height, interval, cat_one_dir):
    """
    将视频按固定间隔读取写入图片
    :param video_src_path: 视频存放路径
    :param formats:　包含的所有视频格式
    :param frame_save_path:　保存路径
    :param frame_width:　保存帧宽
    :param frame_height:　保存帧高
    :param interval:　保存帧间隔
    :param cat_one_dir: 是否将拆的视频帧存在一个文件夹，还是存在各自的文件夹之内
    :return:　帧图片
    """
    videos = os.listdir(video_src_path)

    def filter_format(x, all_formats):
        if x[-4:] in all_formats:
            return True
        else:
            return False

    videos = filter(lambda x: filter_format(x, formats), videos)

    for index, each_video in enumerate(videos):
        try:
            print("正在读取第%d个视频：" % (index+1), each_video)
            each_video_name = each_video[:-4]
            each_video_full_path = os.path.join(video_src_path, each_video)

            if not cat_one_dir:
                if not os.path.exists(os.path.join(frame_save_path, each_video_name)):
                    os.makedirs(os.path.join(frame_save_path, each_video_name))
                each_video_save_full_path = os.path.join(frame_save_path, each_video_name) + "/"
            else:
                if not os.path.exists(frame_save_path):
                    os.makedirs(frame_save_path)
                each_video_save_full_path = os.path.join(frame_save_path, each_video_name)

            cap = cv2.VideoCapture(each_video_full_path)
            frame_index = 0
            frame_count = 0
            if cap.isOpened():
                success = True
            else:
                success = False
                print("读取失败!")
            while (success):
                success, frame = cap.read()
                # print("---> 正在读取第%d帧:" % frame_index, success)
                if frame_index % int(interval) == 0:
                    if resize:
                        frame = cv2.resize(frame, (frame_width, frame_height), interpolation=cv2.INTER_AREA)
                    # cv2.imwrite(each_video_save_full_path + each_video_name + "_%d.jpg" % frame_index, resize_frame)
                    cv2.imwrite(each_video_save_full_path + "%s.jpg" % str(frame_count).zfill(6), frame)
                    frame_count += 1
                frame_index += 1
        except:
            continue

    cap.release()


def read_video(path):
    """
    :param path: 输入视频的路径
    :return: print出视频帧的大小及Fps,Fnums等信息
    """
    if not os.path.exists(path):
        assert "No this video"

    # 获得视频的格式
    videoCapture = cv2.VideoCapture(path)
    # 获得码率及尺寸
    fps = videoCapture.get(cv2.CAP_PROP_FPS)
    size = (int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fNUMS = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
    print("Size:", size)
    print("Fnums:", fNUMS)
    print("Fps:", fps)

    # 读帧
    # success, frame = videoCapture.read()
    # while success:
    # cv2.imshow('windows', frame)  # 显示
    # cv2.waitKey(1000 / int(fps))  # 延迟
    # success, frame = videoCapture.read()  # 获取下一帧
    videoCapture.release()

    return fps, size, fNUMS


if __name__ == '__main__':
    # read one video and analy it
    video_path = '/home/zhuxuhan/zhuxuhan/database/019.bike/videos/20201028070034_770970482609573888_1_477848_.mp4'
    fps, size, fNUMS = read_video(video_path)
    #
    videos_src_path = "/home/zhuxuhan/zhuxuhan/database/019.bike/videos"
    video_formats = [".mp4", ".MOV"]
    frames_save_path = "/home/zhuxuhan/zhuxuhan/database/019.bike/videos_output_cat/"
    resize_width = 320
    resize_height = 240
    time_interval = fps  # 一秒拆一帧， 如果是n秒拆一帧，则需要乘一个n
    resize = False
    cat_one_dir = True
    video2frame(videos_src_path, video_formats, frames_save_path, resize, resize_width, resize_height, time_interval,
                cat_one_dir)
