
# The Amazon API for handwritten. Accuracy is good, only problem is the cost.
# 1000 files for 1.5$. Without any coupon, only 1000 files can be used for free.
# So the API is optional. Decided by another method in correction.
# Only support big area for AWS. When using small area with text it fails(even with same DPI).
def handwritten_AWS_onecell(documentName):
    import boto3

    # Document
    import cv2
    import numpy as np
    # read the image
    img = cv2.imread(documentName, 1)

    # print( img.shape)
    #cv2.imshow("before", img)
    height, width, c = img.shape
    fiximg = np.insert(img, 1500 * [0, width], (0, 0, 0), axis=1)
    newimg = np.insert(fiximg, 1500 * [0, height], (0, 0, 0), axis=0)
    #cv2.imshow("before long", newimg)
    cv2.imwrite("temp_for_AWS.jpg", newimg)
    #cv2.waitKey(0)
    
    # Read document content
    with open("temp_for_AWS.jpg", 'rb') as document:
        imageBytes = bytearray(document.read())
    
    # Amazon Textract client
    textract = boto3.client('textract', region_name='eu-west-2')
    
    # Call Amazon Textract
    response = textract.detect_document_text(Document={'Bytes': imageBytes})
    
    #print(response)
    # Print detected text
    text = []
    confidence = 0
    count = 0
    for item in response["Blocks"]:
        if item["BlockType"] == "WORD":
            text.append(item["Text"])
            confidence += item["Confidence"]
            count+=1
            print ('\033[94m' +  item["Text"] + '\033[0m')
    if count==0:
        print("Confidence of AWS:",confidence)
        print("Text of AWS:","NULL for AWS")
        return confidence,"NULL for AWS"
    else:
        print("Confidence of AWS:",confidence/count)
        print("Text of AWS:",text)
        return confidence/count,text
"""
response = json.load(open("aws_part1.json", "r"))
print(response)
for item in response["Blocks"]:
    if item["BlockType"] == "WORD":
        if item["TextType"] == "HANDWRITING":
            print ('\033[94m' +  item["Text"] + '\033[0m')
"""
#confidence,text = handwritten_AWS_onecell("144.jpg")
#print(confidence,text)

#def handwritten_whole_table():
