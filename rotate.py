"""
This is the part of code to rotate the table generated from pdf file.
"""
import cv2
from math import *
import numpy as np


# rotate the picture
def rotate_bound_white_bg(image, angle, color):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    # perform the actual rotation and return the image
    # borderValue
    if color == "b":
        return cv2.warpAffine(image, M, (nW, nH), borderValue=(0, 0, 0))
    if color == "w":
        return cv2.warpAffine(image, M, (nW, nH), borderValue=(255, 255, 255))
    # return cv2.warpAffine(image, M, (nW, nH))


def rotate_till_align(filename):
    img = cv2.imread(filename)
    if img.shape[0] > img.shape[1]:
        img = np.rot90(img, 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # turn the sheet into binary pic
    binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 35, -5)
    flat = False
    i = 0
    flag = 0
    while flat != True:
        flag += 1
        i = (-1) ** flag * 0.1 * (flag // 2)
        print(i)
        imgRotation = rotate_bound_white_bg(binary, i, "b")
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2500, 1))
        eroded = cv2.erode(imgRotation, kernel, iterations=1)
        dilatedcol = cv2.dilate(eroded, kernel, iterations=1)
        ys, xs = np.where(dilatedcol > 0)
        print(ys)
        if len(ys) != 0:
            print(ys)
            flat = True
        if flag >= 16:
            return

    imgRotation = rotate_bound_white_bg(img, i, "w")
    cv2.waitKey(0)
    cv2.imwrite(filename, imgRotation)
