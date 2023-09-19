import cv2
import numpy as np
import numba as nb

d = 21
t = 2
init_frame = 160

from math import gcd
d, t = d // gcd(d,t), t // gcd(d,t)

def main():
    vidcap = cv2.VideoCapture("clouds.mkv")
    success, clouds = vidcap.read()

    y, x, _ = clouds.shape
    diffs = np.zeros((y, x * 4, 3), dtype=np.uint8)

    success, image = vidcap.read()
    frame = 2
    while success:
        if frame < init_frame:
            success, image = vidcap.read()
            frame += 1
            continue

        if frame % t == 0:
            diff = np.where((clouds > [100, 100, 100]) & (image < [30, 30, 30]), clouds, 0)  # нужна доработка
            diffs[:, :x] |= diff
            diffs = np.roll(diffs, d, 1)

        success, image = vidcap.read()
        frame += 1

    cv2.imwrite("flag.jpg", diffs)


if __name__ == "__main__":
    main()