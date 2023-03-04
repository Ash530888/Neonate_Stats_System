"""
This is the convert part of the nurse table recognition. The codes focus on the specified format of table sheet.
If the sheet changed, the codes may need some modification.
"""

import cv2
import numpy as np
import os



def findcrosspoint(picpath, part):
    image = cv2.imread(picpath)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # turn the sheet into binary pic
    binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 35, -5)
    # ret,binary = cv2.threshold(~gray, 127, 255, cv2.THRESH_BINARY)
    cv2.imwrite("grey.jpg", binary)
    rows, cols = binary.shape
    print(rows)
    print(cols)

    # recognize the horizontal lines
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1000, 1))
    eroded = cv2.erode(binary, kernel, iterations=1)
    # cv2.imshow("Eroded Image",eroded)
    # cv2.imwrite("eroded.jpg", eroded)
    dilatedcol = cv2.dilate(eroded, kernel, iterations=1)

    # recognize the vertical lines
    #if part == "chunks":
       # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, int(rows * 0.5)))
   # else:
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 80))
    eroded = cv2.erode(binary, kernel, iterations=1)
    # cv2.imshow("Eroded Image",eroded)
    dilatedrow = cv2.dilate(eroded, kernel, iterations=1)
    # cv2.imwrite("eroded.jpg", eroded)

    # the cross point
    bitwiseAnd = cv2.bitwise_and(dilatedcol, dilatedrow)
    # cv2.imshow("point",bitwiseAnd)
    # cv2.imwrite("point.png", bitwiseAnd)

    # show the table lines
    merge = cv2.add(dilatedcol, dilatedrow)
    #cv2.imshow("table lines:", merge)
    cv2.imwrite("line.jpg",merge)
    #cv2.waitKey(0)

    # remove the lines from the pic
    merge2 = cv2.subtract(binary, merge)
    # cv2.imshow("pic without the lines", merge2)
    # cv2.waitKey(0)
    # cv2.imwrite("withoutline.png", merge2)

    # get the location of the cross points
    ys, xs = np.where(bitwiseAnd > 0)

    ret, thresh = cv2.threshold(merge, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    mylisty = []
    mylistx = []
    # As there will be many points that have similar pixels,here get only one point
    # Use 10 pixels as a divider
    i = 0
    myxs = np.sort(xs)
    for i in range(len(myxs) - 1):
        if myxs[i + 1] - myxs[i] > 10:
            mylistx.append(myxs[i])
        i = i + 1
    mylistx.append(myxs[i])

    i = 0
    myys = np.sort(ys)
    # print(np.sort(ys))
    for i in range(len(myys) - 1):
        if (myys[i + 1] - myys[i] > 10):
            mylisty.append(myys[i])
        i = i + 1
    mylisty.append(myys[i])

    print('mylisty', mylisty)
    print('mylistx', mylistx)
    return mylisty, mylistx, image


# Different types of cells exists in the table
# divide according types
def mkdir(path):
    '''
    create the folder
    :param path: the path of the folder in string
    :return: True or False
    '''
    path = path.strip()
    path = path.rstrip("\\")

    # judge if the path exists
    isExists = os.path.exists(path)

    if not isExists:
        # create the path
        os.makedirs(path)
        print(path + ' created')
        return True
    else:
        # path already exists
        print(path + ' exists')
        return False


def generate(listy, listx, part, image):
    """
    generate the images of different cells
    :param listy: posy
    :param listx: posx
    :param part: which folder these images belong
    """
    a = 0
    mkdir('./' + str(part))
    for i in range(len(listy) - 1):
        for j in range(len(listx) - 1):
            ROI = image[listy[i] + 2:listy[i + 1] - 2, listx[j] + 2:listx[j + 1] - 2]
            name = str(a) + ".jpg"
            cv2.imwrite('./' + str(part) + "/" + name, ROI)
            # print(a)
            a += 1


def divide_to_chunks(listy, image):
    ROI = image[listy[0] - 7:listy[3] + 7]
    name = "part0.jpg"
    cv2.imwrite(name, ROI)
    ROI = image[listy[4] - 7:listy[-1] + 7]
    name = "part1.jpg"
    cv2.imwrite(name, ROI)
    #ROI = image[listy[4] - 7:listy[-1] + 7]
    #name = "part2.jpg"
    #cv2.imwrite(name, ROI)


def divide_into_parts(picpath):
    listy, listx, image = findcrosspoint(picpath,"main")
    divide_to_chunks(listy, image)
    for i in range(2):
        picpath = "part" + str(i) + ".jpg"
        listy, listx, image = findcrosspoint(picpath, "chunks")
        generate(listy, listx, i, image)
#divide_into_parts("./Tables/OX_10001-1.jpg")



