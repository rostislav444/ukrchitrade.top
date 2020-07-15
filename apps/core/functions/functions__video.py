import os, cv2, math


def imageFromVideo(videoPath, imagePath):
    video = cv2.VideoCapture(videoPath)
    framsQty = video.get(3)
    middleFrame = int(framsQty / 2)
    count = 0
    success = 1
    while success:
        success, image = video.read()
        if count == 1:
            path = "/%s.jpg" % imagePath
            print(path)
            cv2.imwrite("./media/%s.jpg" % imagePath, image)
        if count >= middleFrame:
            path = "/%s.jpg" % imagePath
            print(path)
            cv2.imwrite("./media/%s.jpg" % imagePath, image)
            break
        count += 1
    return path