import cv2 as cv
import numpy as np
from scipy.stats import mode

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Error opening video stream or file")

directions_map = np.zeros([10, 5])

frame_prev = cap.read()[1]
gray_prev = cv.cvtColor(frame_prev, cv.COLOR_BGR2GRAY)
hsv = np.zeros_like(frame_prev)
hsv[:, :, 1] = 255
param = {
    "pyr_scale": 0.5,
    "levels": 3,
    "winsize": 15,
    "iterations": 3,
    "poly_n": 5,
    "poly_sigma": 1.1,
    "flags": cv.OPTFLOW_LK_GET_MIN_EIGENVALS,
}

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    flow = cv.calcOpticalFlowFarneback(gray_prev, gray, None, **param)

    mag, ang = cv.cartToPolar(flow[:, :, 0], flow[:, :, 1], angleInDegrees=True)
    ang_180 = ang / 2
    gray_prev = gray

    threshold = 10

    move_sense = ang[mag > threshold]
    move_mode = mode(move_sense)[0]

    if 45 < move_mode <= 135:
        directions_map[-1, 0] = 1
        directions_map[-1, 1:] = 0
        directions_map = np.roll(directions_map, -1, axis=0)
    elif 135 < move_mode <= 225:
        directions_map[-1, 1] = 1
        directions_map[-1, :1] = 0
        directions_map[-1, 2:] = 0
        directions_map = np.roll(directions_map, -1, axis=0)
    elif 225 < move_mode <= 315:
        directions_map[-1, 2] = 1
        directions_map[-1, :2] = 0
        directions_map[-1, 3:] = 0
        directions_map = np.roll(directions_map, -1, axis=0)
    elif 315 < move_mode or move_mode < 45:
        directions_map[-1, 3] = 1
        directions_map[-1, :3] = 0
        directions_map[-1, 4:] = 0
        directions_map = np.roll(directions_map, -1, axis=0)
    else:
        directions_map[-1, -1] = 1
        directions_map[-1, :-1] = 0
        directions_map = np.roll(directions_map, 1, axis=0)

    loc = directions_map.mean(axis=0).argmax()
    if loc == 0:
        text = "Moving down"
    elif loc == 1:
        text = "Moving to the right"
    elif loc == 2:
        text = "Moving up"
    elif loc == 3:
        text = "Moving to the left"
    else:
        text = "Staying still"

    hsv[:, :, 0] = ang_180
    hsv[:, :, 2] = cv.normalize(mag, None, 0, 255, cv.NORM_MINMAX)
    rgb = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
    visualization = frame.copy()

    frame = cv.flip(frame, 1)

    for row in range(4, visualization.shape[0], 8):
        for col in range(4, visualization.shape[1], 8):
            flowat = flow[row, col]
            cv.line(
                visualization,
                (col, row),
                (col + round(flowat[1]), row + round(flowat[0])),
                (0, 255, 0),
            )

    if text:
        cv.putText(
            frame,
            text,
            (30, 90),
            cv.FONT_HERSHEY_COMPLEX,
            frame.shape[1] / 500,
            (0, 0, 255),
            2,
        )

    cv.imshow("frame", frame)
    cv.imshow("optical flow", rgb)
    cv.imshow("visualization", visualization)

    key = cv.waitKey(5)

    if key & 0xFF == ord("x"):
        cv.imwrite("capture.jpg", frame)

    if (key & 0xFF == ord("q")) or (key & 0xFF == 27):
        break

cap.release()

cv.destroyAllWindows()
