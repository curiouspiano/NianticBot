from PIL import Image
import pytesseract
import cv2
import numpy as np
from skimage.feature import match_template
from fuzzywuzzy import fuzz

def _parseLevel(gray, template):
    # find location of level
    resultImage = match_template(gray, template)

    ij = np.unravel_index(np.argmax(resultImage), resultImage.shape)
    x, y = ij[::-1]
    # extract level from image
    height, width  = gray.shape
    levelarea = gray[y-int(0.09*width):y+int(0.01*width),x-int(0.03*width):x+int(0.13*width)]
    level = pytesseract.image_to_string(levelarea)
    print("Found text -> {" + level + "}\n")
    reqLevel = [int(s) for s in level.split() if s.strip('.').isdigit()]

    return reqLevel

def _parseName(image, template):

    gray = image

    resultImage = match_template(gray, template)


    ij = np.unravel_index(np.argmax(resultImage), resultImage.shape)  
    x, y = ij[::-1]

    # extract level from image
    height, width  = gray.shape

    nameArea = gray[y-int(0.11*width):y+int(0.00*width),x-int(0.05*width):x+int(0.34*width)]
    foundText = pytesseract.image_to_string(nameArea)

    print("Found text -> {" + foundText + "}\n")

    name = [s for s in foundText.split()]


    return name

def getLevel(imagepath):
    result = [0,False]
    # load the example image and  convert it to grayscale
    image = cv2.imread(imagepath)
    template_ios =  cv2.imread("template_ios.PNG")
    template_android = cv2.imread("template_android.PNG")
    if image is None:
        print("Error while reading file")
        return None
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    global orig_gray
    orig_gray = gray
    gray_template_ios = cv2.cvtColor(template_ios, cv2.COLOR_RGB2GRAY)
    gray_template_android = cv2.cvtColor(template_android, cv2.COLOR_RGB2GRAY)

    # test for android template
    reqLevel = _parseLevel(gray, gray_template_android)
    if reqLevel == []:
        # if fail, test for iOS template
        reqLevel = _parseLevel(gray, gray_template_ios)
        if reqLevel == []:
            result[0] = None
        else:
            result[0] = reqLevel[0]
    else:
        result[0] = reqLevel[0]


    return int(result[0])

def getName(imagepath):

    image = cv2.imread(imagepath)

    template_android =  cv2.imread("&_template_android.png")
    template_ios = cv2.imread("&_template_ios.png")
    
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    gray_temp_android = cv2.cvtColor(template_android, cv2.COLOR_RGB2GRAY)
    gray_temp_ios = cv2.cvtColor(template_ios, cv2.COLOR_RGB2GRAY)

    name = _parseName(gray, gray_temp_android)
    if name == [] or len(name[0]) <= 2:
        name = _parseName(gray, gray_temp_ios)
        if name == []:
            print("Could not determine name")
            return 'none'
    
    return name[0]

def getTeam(imagepath):
    print("temp")
    image = cv2.imread(imagepath)
    flip = cv2.flip(image, -1)

    x_start = 300
    y_start = 0
    x_len = 150
    y_len = 8
    crop = flip[x_start : x_start + x_len, y_start : y_start + y_len]
    #cv2.imshow("cropped", crop)
    #cv2.waitKey(0)

    red = 0
    blue = 0
    green = 0

    for i in range(x_len):
        for j in range(y_len):
            val = image[i, j]
            #print(val)
            red += val[2]
            blue += val[0]
            green += val[1]

    x = max([red, blue, green])

    tot = red + blue + green

    R = red/tot
    B = blue/tot
    G = green/tot


    result = ''
    if B < .2 and R > .35 and G >.35:
        result = 'instinct'
    elif B >= .5:
        result = 'mystic'
    elif R >= .5:
        result = 'valor'
    else:
        result = 'unknown'

    return result
