
# Python program to save a
# video using OpenCV
import cv2
import time
import sys
import keyboard
import data_validation

def make_1080p(video):
    video.set(3, 1920)
    video.set(4, 1080)

def make_720p(video):
    video.set(3, 1280)
    video.set(4, 720)

def make_480p(video):
    video.set(3, 640)
    video.set(4, 480)

def captrure_video_latency(latency,video_info):
    video = cv2.VideoCapture(2)

    if (video.isOpened() == False):
        print("Error reading video file")

    make_1080p(video)

    frame_width = int(video.get(3))
    frame_height = int(video.get(4))


    size = (frame_width, frame_height)
    print(size)

    result = cv2.VideoWriter(video_info["path"],cv2.VideoWriter_fourcc('m', 'ps', '4', 'v'),30, size)
    # result = cv2.VideoWriter('filename.avi',cv2.VideoWriter_fourcc(*'MJPG'),10, size)
    start_time = time.time()
    list_of_frame = []
    latency_secs = latency
    end_time = start_time + latency_secs
    start = False

    while time.time()<end_time:

        ret, frame = video.read()
        frame2 = cv2.flip(frame, 1)
        list_of_frame.append(frame2)

        # result.write(frame2)

        window_name = 'Frame'
        cv2.imshow(window_name, frame2)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
        cv2.waitKey(1)


    print("start saving")
    for fram in list_of_frame:
        result.write(fram)

    video.release()
    result.release()
    cv2.destroyAllWindows()

def captrure_video_keyboard(video_info):
    video = cv2.VideoCapture(2)

    if (video.isOpened() == False):
        print("Error reading video file")

    make_1080p(video)

    frame_width = int(video.get(3))
    frame_height = int(video.get(4))


    size = (frame_width, frame_height)
    result = cv2.VideoWriter(video_info["path"],cv2.VideoWriter_fourcc('m', 'ps', '4', 'v'),30, size)
    start_time = time.perf_counter()
    list_of_frame = []

    start = False
    try:
        while True:
            ret, frame = video.read()
            if start == False:
                start_time = time.time()
                print("collect video")
                start = True
            frame2 = cv2.flip(frame, 1)
            list_of_frame.append(frame2)

            if keyboard.is_pressed('e'):
                end_time = time.time()
                print("stop recording")
                end_time = time.time()
                print("STOP recording video")
                break


    except KeyboardInterrupt:
        pass

    print("start saving")
    # print(list_of_frame)
    for fram in list_of_frame:
        result.write(fram)

    video.release()
    result.release()
    cv2.destroyAllWindows()

    # print(result)
    print("{} video is saved!".format(video_info['path']))
    video_info['duration'] = end_time - start_time
    video_info['stime'] = start_time
    video_info['etime'] = end_time
    print(video_info)
    return video_info



# captrure_video(30,"test")
if __name__ == "__main__":
    video_info = {"name": "video", "path": "bob.mp4"}
    # captrure_video_latency(5,video_info)
    captrure_video_keyboard(video_info)
    # data_validation.video_checker('bob_47.mp4')