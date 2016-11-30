import cv2
firstFrame = True
pathVid =  '<path to vid or im seq>' # e.g. vidName.mp4 or images/%04.jpg (if image name is 0001.jpg...)
vidReader = cv2.VideoCapture(pathVid)
initBbox = (30, 60, 60, 70 )  # (x_tl, y_tl, w, h)
tracker = cv2.Tracker_create('KCF')
while vidReader.isOpened():
    ok, image=vidReader.read()
    if firstFrame:
        ok = tracker.init(image, initBbox)
        firstFrame = False
    ok, bbox = tracker.update(image)
    print ok, bbox
