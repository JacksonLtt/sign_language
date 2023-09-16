import cv2
for i in range(5):
    cap = cv2.VideoCapture(1)
    success,image = cap.read()
    if success:
        print(i)
    cap.release()