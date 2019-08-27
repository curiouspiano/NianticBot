from PIL import Image
import pytesseract
import cv2
import numpy as np
from skimage.feature import match_template
from fuzzywuzzy import fuzz


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
