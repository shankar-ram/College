import cv2
import winsound
cam = cv2.VideoCapture(0)   # inside parentheses - number of camera that cv2 has to read
while cam.isOpened():
    ret, frame1 = cam.read()      # read whats happening on the camera
    ret, frame2 = cam.read()
    diff = cv2.absdiff(frame1, frame2)
    grey = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(grey, (5, 5), 0)      # convert grey to blur
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)   # get rid of noise
    dilated = cv2.dilate(thresh, None, iterations=3)    # make them bigger for 3 iterations
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # boundary of items detected to be moving
    # cv2.drawContours(frame1, contours, -1, (0, 255, 0), 2)     # draw amd see the contours
    for c in contours:
        if cv2.contourArea(c) < 5000:
            continue
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0,255, 0), 2)
        winsound.Beep(500, 200)
    if cv2.waitKey(10) == ord('q'):      # wait for 10ms for user to press key. If q then destroy window
        break
    cv2.imshow('Security cam', frame1)   # frame- video frame

