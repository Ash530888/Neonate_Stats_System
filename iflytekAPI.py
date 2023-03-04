import time
import base64
import hashlib
import requests


def getHeader(API_KEY, APPID, language, location):
    curTime = str(int(time.time()))
    param = "{\"language\":\"" + language + "\",\"location\":\"" + location + "\"}"
    paramBase64 = base64.b64encode(param.encode('utf-8'))

    m2 = hashlib.md5()
    str1 = API_KEY + curTime + str(paramBase64, 'utf-8')
    m2.update(str1.encode('utf-8'))
    checkSum = m2.hexdigest()
    header = {
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-Appid': APPID,
        'X-CheckSum': checkSum,
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
    return header


def getBody(filepath):
    with open(filepath, 'rb') as f:
        imgfile = f.read()
    data = {'image': str(base64.b64encode(imgfile), 'utf-8')}
    return data


# handwritten recognition from iflytek API
# 150,000 free units each day
def handwritten(picFilePath):
    # here details should be modified to your account detail
    URL = "http://webapi.xfyun.cn/v1/service/v1/ocr/handwriting"
    # The API ID used to connect
    APPID = "cea1b864"
    # The API key used to connect
    API_KEY = "37c4c0900b5107943b1cc53990183d6a"
    # language setting
    language = "en"
    # if return the location
    location = "false"
    line = ""
    flag = False
    while flag != True:
        try:
            r = requests.post(URL, headers=getHeader(API_KEY, APPID, language, location), data=getBody(picFilePath))
            line = r.content
            flag = True
        except Exception as e:
            print("error happens:", e)

    # transform into dict
    byteDic = eval(line)
    print(byteDic)
    lineList = byteDic["data"]["block"][0]["line"]
    lines = []
    for line in lineList:
        # Info of each line
        words = line["word"]
        for word in words:
            wordContent = word["content"]
            lines.append(wordContent)
    print(lines)
    return lines
