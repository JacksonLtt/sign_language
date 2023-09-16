# Python program to save a
# video using OpenCV


import cv2
import time

def captrure_video():
    video = cv2.VideoCapture(0)

    if (video.isOpened() == False):
        print("Error reading video file")

    video.set(3, 1920)
    video.set(4, 1080)

    frame_width = int(video.get(3))
    frame_height = int(video.get(4))

    size = (frame_width, frame_height)
    result = cv2.VideoWriter('test.mp4',cv2.VideoWriter_fourcc('m', 'ps', '4', 'v'),15, size)
    # result = cv2.VideoWriter('filename.avi',cv2.VideoWriter_fourcc(*'MJPG'),10, size)
    start_time = time.time()

    latency_secs = 10
    end_time = start_time + latency_secs
    print("start_time:",start_time)
    print("end_time:",end_time)

    start = False

    while (time.time()<end_time):
        ret, frame = video.read()

        if ret == True:
            if start == False:
                print("start_time:", time.time())
                start = True
            frame2 = cv2.flip(frame, 1)
            result.write(frame2)
            window_name = 'Frame'

            cv2.imshow(window_name, frame2)

            cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
            cv2.waitKey(1)

        # Break the loop
        else:
            break

    print("end_time:",time.time())

    video.release()
    result.release()

    cv2.destroyAllWindows()

    print("The video was successfully saved")

captrure_video()