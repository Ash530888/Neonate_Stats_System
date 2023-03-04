import cv2
from skimage import measure, color

from fastai.vision.all import *
import pathlib
import torch

# divide the cell into boxes
def divide(pic_path):
    image = cv2.imread(pic_path)
    frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rows, cols = frame.shape
    print(rows, cols)
    ret, frame = cv2.threshold(frame, 100, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    frame = cv2.dilate(frame, kernel, iterations=1)
    # find the connective area
    labels = measure.label(frame, connectivity=2)
    properties = measure.regionprops(labels)

    loc = []
    for prop in properties:
        print(prop.area)
        print(prop.bbox)
        if 1000<prop.area<10000:
            loc.append(prop.bbox)
    loc = np.array(loc)
    loc = loc[loc[:, 1].argsort()]





    return loc

# these comment codes are used to visualize the connective area, used when debugging
"""    dst = color.label2rgb(labels)
    print('regions number:', labels.max() + 1)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
    ax1.imshow(frame, plt.cm.gray, interpolation='nearest')
    ax1.axis('off')
    ax2.imshow(dst, interpolation='nearest')
    ax2.axis('off')

    fig.tight_layout()
    plt.show()
    print(loc)"""


# Use the model to do classification
def classify(img, learner, labels):
    pred, pred_idx, probs = learner.predict(img)
    print(pred)
    print(pred_idx)
    print(probs)
    return pred


def recognition(pic_path):
    # These two lines are necessary because fastai is not compatible with Windows
    temp = pathlib.PosixPath
    pathlib.PosixPath = pathlib.WindowsPath
    loc = divide(pic_path)
    learner = load_learner("./model.pkl")
    labels = learner.dls.vocab
    num = ""
    for loc_1 in loc:
        print(loc_1)
        doc = cv2.imread(pic_path)[loc_1[0] + 2:loc_1[2] - 2, loc_1[1] + 3:loc_1[3] - 3]
        doc = cv2.cvtColor(doc, cv2.COLOR_BGR2GRAY)
        rows, cols = doc.shape
        print(rows,cols)
        doc = cv2.resize(doc, (28, 28))
        doc = 255 - doc
        ret, doc = cv2.threshold(doc, 50, 255, cv2.THRESH_BINARY)
        doc_1 = doc[2:26,2:26]
        count = str(doc_1.tolist()).count("255")
        print(count)
        if count <=10:
            continue
        i = classify(doc, learner, labels)
        # the way to centering the digit, no improvement on Resnet34 but huge improvement on normal CNN
        """
        # get contours (presumably just one around the nonzero pixels)
        x, y, w, h = cv2.boundingRect(doc)
        print(x,y,w,h)
        # Create new blank image and shift ROI to new coordinates
        mask = np.zeros(doc.shape, dtype=np.uint8)
        ROI = doc[y:y + h, x:x + w]
        print(ROI.shape)
        #cv2.imshow('ROI', ROI)
        #cv2.imshow('mask', mask)
        #cv2.waitKey()
        y = round(28 // 2 - ROI.shape[0] // 2)
        x =round( 28 // 2 - ROI.shape[1] // 2)
        print(x,y)
        mask[y:y + h, x:x + w] = ROI

        #cv2.imshow('mask', mask)
        #cv2.waitKey()
        #y_pred = model(result)
       
        """
        num = num + str(i[0])
    print(num)
    return num


#recognition('./0/15.jpg')
