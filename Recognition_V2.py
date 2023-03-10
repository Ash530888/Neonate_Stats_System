import csv
import os
from skimage import measure, color
import numpy as np
import matplotlib.pyplot as plt
import PIL
import cv2
import AzureAPI
import GoogleAPI
import correction_wo_AWS
import correction
import iflytekAPI
import number_recognition
import OMR
# pre text
def printed(part, order):
    line_A = ["Name: ", "Date of birth: ", "MRN: ", "Baseline SpO2(%): ", "Baseline Pulse Rate(bpm): ",
              "Baseline Respiratory Rate(bpm): ", "Time started: ", "Time finished: ",
              "Additional Respiratory/Gastro Support: ", ]
    line_B = ["Time: ", "Sleep/Awake status: ", "Oxygen saturation(SpO2 %): ", "Cares: ", "Feeds: ",
              "Device check: ", "Sensor check: ", "Respiratory rate: ", "Position: ", "Snoring: ",
              "NIV(CPAP, IPAP/EPAP)", "Supplemental O2(litres/min)", "TCM5 CO2(kPa)", "Comments", ]
    if part == 0:
        print(line_A[order])
        return line_A[order]
    else:
        print(line_B[order])
        return line_B[order]


# Now we are using 'divide and conquer' method to recognize.
# Thus a lot of pics are going to be recognized.
# Reduce the amount of pics to be recognized, as well as save money.
def with_content(file, part, area):
    image = cv2.imread(file)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # turn the sheet into binary pic
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    top = str(thresh.tolist()).count("255")
    print(top)
    input()
    time_ = False
    word_ = False
    count = 0
    if top >= 1650:
        count += 1
        # Use three APIs to compare the results
        con_G, result_G = GoogleAPI.handwritten_v2(file)
        con_M, result_M = AzureAPI.handwritten_Azure(file)
        result_I = iflytekAPI.handwritten(file)
    else:
        return count," "
    # for all written words
    if part == "part2" and (area == 4 or area == 8 or area == 9 or area == 13):
        word_ = True
        #result = correction.choose_a_result(con_G,result_G,con_M, result_M,result_I,file,time_,word_)
        result = correction_wo_AWS.choose_a_result(con_G,result_G,con_M, result_M,result_I,file,time_,word_)
    else:
        #result = correction.choose_a_result(con_G, result_G, con_M, result_M, result_I, file, time_, word_)
        result = correction_wo_AWS.choose_a_result(con_G, result_G, con_M, result_M, result_I, file, time_, word_)
    # cv2.imshow("pic1",img)
    # cv2.waitKey(0)
    print(result)
    return count,result

def output_file(filename):
    count = 0
    list_1 = {}
    first = "./0/"
    dirs = os.listdir(first)
    total = len(dirs)
    for i in range(total):
        print(i)
        file = first + str(i) + '.jpg'
        if i % 2 == 0:
            list_1[i] = printed(0, i // 2)
        elif i == 7 or i ==9 or i ==11 or i ==13 or i ==15:
            list_1[i] = number_recognition.recognition(file)
        else:
            list_1[i] = " "
    third = "./1/"
    list_3 = {}
    dirs = os.listdir(third)
    total = len(dirs)
    for i in range(total):
        file = third + str(i) + '.jpg'
        print(file)
        if i % 11 == 0:
            list_3[i] = printed(1, i // 11)
        elif i // 11 == 0 or i // 11 == 2 or i // 11 == 7 or i // 11 == 12:
            list_3[i] = number_recognition.recognition(file)
        elif i // 11 == 11:
            image = cv2.imread(file)
            list_3[i] = OMR.supple(image)
        elif i // 11 == 1 or i // 11 == 5:
            list_3[i] = OMR.choose((i // 11), cv2.imread(file))
        elif i // 11 == 10:  # this line is not required to be recognized based on the doctor's feedback
            # image = cv2.imread(file)
            # image = image[0:(int(image.shape[0] // 2)), :]
            # cv2.imwrite("temp.jpg", image)
            # list_3[i] = handwritten_v2("temp.jpg") + " " + choose((i // 11), cv2.imread(file))
            list_3[i] = "temp data"
        elif i // 11 == 3 or i // 11 == 6:
            list_3[i] = OMR.checkbox((i // 11), cv2.imread(file))
        elif i//11 == 0 or i//11 ==2 or i//11 ==7 or i//11 ==11:
            list_3[i] = number_recognition.recognition(file)
        else:
            count_A, result = with_content(file, "part2", i // 11)
            count += count_A
            list_3[i] = result
    # write the lists into the csv file
    with open(filename, 'w', encoding='utf-8', newline='') as fp:
        writer = csv.writer(fp)

        l3 = []
        for i in range(len(list_1) // 2):
            l1 = []
            l1.append(list_1[2 * i])
            l1.append(list_1[2 * i + 1])
            writer.writerow(l1)

        for i in range(len(list_3) // 11):
            l2 = []
            for k in range(11):
                l2.append(list_3[11 * i + k])
            writer.writerow(l2)
    return filename
#output_file('OX_1_vfinal_test.csv')