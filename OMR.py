import cv2
import numpy as np
import number_recognition
# find the tick box




def checkbox(type, image):
    if type == 3:
        top_word = "Suctioning"
        mid_word = "Medication"
        bot_word = "Other"
        im1 = cv2.imread("Type3.jpg")
    if type == 6:
        top_word = "Probe"
        mid_word = "Bands"
        bot_word = "Cannula"
        im1 = cv2.imread("Type6.jpg")
    rows,cols,_ = image.shape
    #print(rows,cols)
    im1=cv2.resize(im1,(cols,rows))
    image_final,flag = Align(im1, image)
    if flag == True:
        image_final = cv2.GaussianBlur(image_final, (3, 3), 0)
        #cv2.imshow("a", im1)
        #cv2.imshow("b", image)
        #cv2.imshow("final", image_final)
        ret, image_final = cv2.threshold(image_final, 200, 255, cv2.THRESH_BINARY)
        im = image_final[:, 0:int(image_final.shape[1] / 4.6)]
        #cv2.imshow("final_1", im)
        #cv2.waitKey(0)
        im_top = im[5:(int(im.shape[0] / 3)) - 5, 5:]
        im_mid = im[(int(im.shape[0] / 3)) + 5:(int(im.shape[0] / 3 * 2)) - 5, 5:]
        im_bot = im[(int(im.shape[0] / 3 * 2)) + 5:-3, 5:]
        #cv2.imshow("final_top", im_top)
        #cv2.imshow("final_mid", im_mid)
        #cv2.imshow("final_bot", im_bot)
        #cv2.waitKey(0)
        top = str(im_top.tolist()).count("255")
        mid = str(im_mid.tolist()).count("255")
        bot = str(im_bot.tolist()).count("255")
        print(top,mid,bot)
        total = top + mid + bot
        result = ""
        if top >= 60:
            result = result + " " + top_word
        if mid >= 60:
            result = result + " " + mid_word
        if bot >= 60:
            result = result + " " + bot_word

        print("The result is:", result)
        return result
    else:
        image = image[:, 0:int(image.shape[1] / 4.6)]
        im1_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, im = cv2.threshold(im1_gray, 200, 255, cv2.THRESH_BINARY)
        im = 255 - im
        # image_f = Align(im1, image)

        # ret, im = cv2.threshold(image_f, 200, 255, cv2.THRESH_BINARY)
        # cv2.imshow("final", im)
        # cv2.imshow("final_F", image_f)
        # cv2.waitKey(0)
        im_top = im[5:(int(im.shape[0] / 3)) - 5, 5:]
        im_mid = im[(int(im.shape[0] / 3)) + 5:(int(im.shape[0] / 3 * 2)) - 5, 5:]
        im_bot = im[(int(im.shape[0] / 3 * 2)) + 5:-5, 5:]
        #cv2.imshow("final_top", im_top)
        #cv2.imshow("final_mid", im_mid)
        #cv2.imshow("final_bot", im_bot)
        #cv2.waitKey(0)
        top = str(im_top.tolist()).count("255")
        mid = str(im_mid.tolist()).count("255")
        bot = str(im_bot.tolist()).count("255")
        total = top + mid + bot
        # To adapt the writer's handwriting ways
        result = ""
        if top >= 250:
            result += " " + top_word
        if mid >= 250:
            result += " " + mid_word
        if bot >= 250:
            result += " " + bot_word
        print("The result is:", result)
        return result

"""    # To adapt the writer's handwriting ways
    if total // 3 - threshold > 100 and max(top, mid, bot) - threshold >= 300:
        threshold += (total // 3 - threshold) // 2
    print(top, mid, bot)
    print(threshold)
    result = ""
    if top >= threshold:
        result += " " + top_word
    if mid >= threshold:
        result += " " + mid_word
    if bot >= threshold:
        result += " " + bot_word"""


# judge which side writer chooses
# dumb way to judge, align the chosen photo with original one,
# choose the side with more pixels if the total pixels reached the threshold
def choose(type, image):
    if type == 1:
        im1 = cv2.imread("SorA.jpg")
        proportion = 2.3
    if type == 5:
        im1 = cv2.imread("ONOFF.jpg")
        proportion = 3
    if type == 10:
        im1 = cv2.imread("LEAK.jpg")
        proportion = 2.8
        im1 = im1[(int(im1.shape[0] // 2.2)):-1, :]
        image = image[(int(image.shape[0] // 2.2)):-1, :]
        im1 = im1[:, (int(im1.shape[1] // 2.7)):-1]
        image = image[:, (int(image.shape[1] // 2.7)):-1]
        # cv2.imshow("word",im1)
        # cv2.imshow("word_1", image)
        # cv2.waitKey(0)
        # print(im1.shape)
    rows,cols,_ = image.shape
    print(rows,cols)
    im1=cv2.resize(im1,(cols,rows))
    #cv2.imshow("1",im1)
    image_f,flag = Align(im1, image)
    #cv2.imshow("a",image_f)
    #cv2.waitKey(0)
    image_f = cv2.GaussianBlur(image_f, (3, 3), 0)
    #cv2.imshow("show_1",image_f)
    ret, im = cv2.threshold(image_f, 200, 255, cv2.THRESH_BINARY)

    #cv2.imshow("show_im",im)
    # print(im)
    # print(im.shape[1])
    result = ""
    im_left = im[:, 0:(int(im.shape[1] // proportion))]
    im_right = im[:, (int(im.shape[1] // proportion)):-1]
    left = str(im_left.tolist()).count("255")
    right = str(im_right.tolist()).count("255")
    #cv2.imshow("word", im_left)
    #cv2.imshow("word_1", im_right)
    #cv2.waitKey(0)
    print(left)
    print(right)
    total = left + right
    if type == 1:
        if total >= 150 and left > right:
            result = "sleep"
        elif total >= 150 and left < right:
            result = ("awake")
        else:
            result = (" ")
    if type == 5:
        if total >= 150 and left > right:
            result = "on"
        elif total >= 150 and left < right:
            result = ("off")
        else:
            result = (" ")
    if type == 10:
        if total >= 150 and left > right:
            result = "LEAK"
        elif total >= 150 and left < right:
            result = ("NO LEAK")
        else:
            result = (" ")
    print(result)
    return result


# Align the images
def Align(im1, im2):
    flag = True
    # Convert images to grayscale
    im1_gray = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
    im2_gray = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
    ret, im1_gray = cv2.threshold(im1_gray, 200, 255, cv2.THRESH_BINARY)
    ret, im2_gray = cv2.threshold(im2_gray, 200, 255, cv2.THRESH_BINARY)
    im1_gray = 255 - im1_gray
    im2_gray = 255 - im2_gray
    # Find size of image1
    sz = im1.shape
    # Define the motion model
    warp_mode = cv2.MOTION_TRANSLATION
    # Define 2x3 or 3x3 matrices and initialize the matrix to identity
    if warp_mode == cv2.MOTION_HOMOGRAPHY:
        warp_matrix = np.eye(3, 3, dtype=np.float32)
    else:
        warp_matrix = np.eye(2, 3, dtype=np.float32)
    # Specify the number of iterations.
    number_of_iterations = 5000;
    # Specify the threshold of the increment
    # in the correlation coefficient between two iterations
    termination_eps = 1e-6;
    # Define termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, number_of_iterations, termination_eps)
    # Run the ECC algorithm. The results are stored in warp_matrix.
    try:
        (cc, warp_matrix) = cv2.findTransformECC(im1_gray, im2_gray, warp_matrix, warp_mode, criteria, inputMask=None,
                                                 gaussFiltSize=1)
    except Exception as e:
        print("error happens:", e)
        Flag = False
    if warp_mode == cv2.MOTION_HOMOGRAPHY:
        # Use warpPerspective for Homography
        im2_aligned = cv2.warpPerspective(im2_gray, warp_matrix, (sz[1], sz[0]),
                                          flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
    else:
        # Use warpAffine for Translation, Euclidean and Affine
        im2_aligned = cv2.warpAffine(im2_gray, warp_matrix, (sz[1], sz[0]),
                                     flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
    # print(im1.shape)
    # print(im2.shape)
    # print(im2_aligned.shape)
    # cv2.imshow("Image 1", im1_gray)
    # cv2.imshow("Image 2", im2_gray)
    # cv2.waitKey(0)
    # cv2.imshow("Aligned Image 2", im2_aligned)
    # print(im2_aligned)
    image_f = im2_aligned - im1_gray
    # print(image_f)
    # cv2.imshow("Image",image_f)
    # cv2.waitKey(0)
    # cv2.imshow("show",im_left)
    # cv2.imshow("show_1",im_right)
    # cv2.waitKey(0)
    return image_f,flag


def supple(image):
    im1_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, im = cv2.threshold(im1_gray, 200, 255, cv2.THRESH_BINARY)
    im = 255 - im
    im = im[:, 0:image.shape[1] // 5]
    im_top = im[5:(int(im.shape[0] / 3)), 5:-5]
    # im_bot = im[(int(im.shape[0] / 3*2)):-5, 5:-5]
    im_word = image[(int(im.shape[0] / 3)) - 5:-5, 5:-5]
    #cv2.imshow("final_top", im_top)
    # cv2.imshow("final_bot", im_bot)
    #cv2.imshow("final_word", im_word)
    #cv2.waitKey(0)
    top = str(im_top.tolist()).count("255")
    # bot = str(im_bot.tolist()).count("255")
    print(top)
    if top >= 300:
        return "No or SVIA"
    else:
        cv2.imwrite("temp_for_rec.jpg", im_word)
        num = number_recognition.recognition("temp_for_rec.jpg")
        if num == "":
            return "NULL"
        num = float(num) / 10
        print(num)
        return num


# supple(cv2.imread('./1/128.jpg'))
#choose(1,cv2.imread('./1/13.jpg'))
#checkbox(3, cv2.imread('./1/43.jpg'))
