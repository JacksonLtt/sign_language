import cv2

cap = cv2.VideoCapture('/Users/taitinglu/Documents/GitHub/sign_language/Image/demo video/3sensors/3sensors/7.mp4')

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height= int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

writer= cv2.VideoWriter('flipvideo.mp4', cv2.VideoWriter_fourcc(*'DIVX'), 20, (width,height))

while True:
    ret,frame= video.read()

    writer.write(frame)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break


ret,img=cap.read()
flipVertical = cv2.flip(img, 0)
flipHorizontal = cv2.flip(img, 1)
flipBoth = cv2.flip(img, -1)

# cv2.imshow('Original image', img)
# # cv2.imshow('Flipped vertical image', flipVertical)
# # cv2.imshow('Flipped horizontal image', flipHorizontal)
# # cv2.imshow('Flipped both image', flipBoth)
# #
# cv2.waitKey(0)
# cv2.destroyAllWindows()