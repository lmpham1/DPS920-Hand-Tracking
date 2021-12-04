import os
import re
import cv2 as cv  # opencv library
import numpy as np
from os.path import isfile, join
import matplotlib.pyplot as plt

# For webcam input:
cap = cv.VideoCapture(0)
frame_prev = cap.read()[1]
gray_prev = cv.cvtColor(frame_prev, cv.COLOR_BGR2GRAY)

prev_x, prev_y = 0, 0
text = "Staying still"

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray_cpy = gray.copy()
    gray = cv.GaussianBlur(gray, (7, 7), 0)

    diff_image = cv.absdiff(gray, gray_prev)

    # perform image thresholding
    ret, thresh = cv.threshold(diff_image, 30, 255, cv.THRESH_BINARY)

    # apply image dilation
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv.dilate(thresh, kernel, iterations=1)

    contours, hierarchy = cv.findContours(
        dilated.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_NONE
    )

    valid_cntrs = []

    for i, cntr in enumerate(contours):
        x, y, w, h = cv.boundingRect(cntr)
        if cv.contourArea(cntr) >= 25:
            valid_cntrs.append(cntr)

    if len(contours) > 0:
        max_cntr = max(contours, key=cv.contourArea)
        chull = cv.convexHull(max_cntr)

        # find the most extreme points in the convex hull
        extreme_top = tuple(chull[chull[:, :, 1].argmin()][0])
        extreme_bottom = tuple(chull[chull[:, :, 1].argmax()][0])
        extreme_left = tuple(chull[chull[:, :, 0].argmin()][0])
        extreme_right = tuple(chull[chull[:, :, 0].argmax()][0])

        # find the center of the palm
        cX = int((extreme_left[0] + extreme_right[0]) / 2)
        cY = int((extreme_top[1] + extreme_bottom[1]) / 2)
        if cX - prev_x > 100:
            text = "Moving right"
        elif cX - prev_x < -100:
            text = "Moving left"
        elif cY - prev_y > 100:
            text = "Moving down"
        elif cY - prev_y < -100:
            text = "Moving up"
        elif abs(cX - prev_x) < 10 and abs(cY - prev_y) < 10:
            text = "Staying still"

        prev_x = cX
        prev_y = cY

    """
    cv.putText(
        frame,
        text,
        (30, 90),
        cv.FONT_HERSHEY_COMPLEX,
        frame.shape[1] / 500,
        (0, 0, 255),
        2,
    )
    """

    # count of discovered contours
    len(valid_cntrs)

    dmy = frame.copy()

    cv.drawContours(dmy, valid_cntrs, -1, (127, 200, 0), 2)
    # cv.line(dmy, (0, 80), (256, 80), (100, 255, 255))

    cv.imshow("Grayscale", gray_cpy)
    cv.imshow("Gaussian Blur", gray)
    cv.imshow("Diff", diff_image)
    cv.imshow("Frame", dmy)
    cv.imshow("Dilated", dilated)
    gray_prev = gray

    k = cv.waitKey(5)
    if k & 0xFF == 27 or k & 0xFF == ord("q"):
        break
cap.release()
