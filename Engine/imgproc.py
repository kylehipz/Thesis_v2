import numpy as np
import pytesseract as ts
from PIL import Image
import cv2
import os

def getROI(image, p1, p2):
    """
    Parameters
    ----------
    Returns
    -------
    """
    return image[p1[1]:p2[1], p1[0]:p2[0]]

def draw(img, p1, p2):
    """Draws a box on the detected license plate
    Parameters
    ----------
    img : numpy array
        The actual image
    p1 : tuple
        Top left coordinate of the bounding box
    p2 : tuple
        Bottom right coordinate of the bounding box
    Returns
    -------
    None
    """

    # colors by pixels
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (255, 0, 0)
    RED = (0, 0, 255)
    GREEN = (0, 255, 0)

    cv2.rectangle(img, p1, p2, GREEN, 2)

def unlock(image):
    """Encoding the image (binary / thresholded image) to jpg and then decoding it again
    Parameters
    image : numpy array
        The binary / thresholded image
    ----------
    Returns
    -------
    decoded_image : numpy array
        The decoded binary image
    """

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 100, 255, 0)
    thresh = cv2.resize(thresh, (500, 200))
    encoding_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    res, encimg = cv2.imencode('.jpg', thresh, encoding_param)
    decoded_image = cv2.imdecode(encimg, 1)
    return decoded_image

def findLargestContour(image):
    """Finds the largest contour (most likely to be the license plate) in an image
    Convert to grayscale -> Apply Thresholding -> Find Contours -> Create Mask -> Apply Mask
    Parameters
    ----------
    image : numpy array
        The actual image
    Returns
    -------
    largest_contour : numpy array
        The ROI (region of interest) which contains the largest contour
    """

    # thresholding and finding contours
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (13, 13), 0)
    _, gray = cv2.threshold(gray, 200, 255, 0) 
    contours, hierarchy = cv2.findContours(gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # if no contours found
    if len(contours) == 0:
        return gray

    # get the largest area of the contour
    largest_area = sorted(contours, key=cv2.contourArea)[-1]
    
    # mask creation
    mask = np.zeros(image.shape, np.uint8)
    cv2.drawContours(mask, [largest_area], 0, (255, 255, 255, 255), -1)
    dst = cv2.bitwise_and(image, mask)
    mask = 255-mask
    roi = cv2.add(dst, mask)

    # remove small components
    roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, gray = cv2.threshold(roi_gray, 200, 255, 0)
    contours, hierarchy = cv2.findContours(gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    max_x = 0
    max_y = 0
    min_x = image.shape[1]
    min_y = image.shape[0]

    for c in contours:
        if 150 < cv2.contourArea(c) < 100000:
            x, y, w, h = cv2.boundingRect(c)
            min_x = min(x, min_x)
            min_y = min(y, min_y)
            max_x = max(x+w, max_x)
            max_y = max(y+h, max_y)

    roi = gray[min_y:max_y, min_x:max_x]
    # kernel = np.ones((5, 5), np.float32)/25
    # roi = cv2.filter2D(roi, -1, kernel)
    # return cv2.GaussianBlur(roi, (11, 11), 0)
    return cv2.resize(roi, (200, 70))

def rotate(image):
    """
    Parameters
    ----------
    Returns
    -------
    """
    image = cv2.resize(image, (640, 480))
    rows, cols = image.shape[:2]
    M = cv2.getRotationMatrix2D((cols/2, rows/2), -90, 1)
    rotated_image = cv2.warpAffine(image, M, (cols, rows))

    return rotated_image
def nothing(x):
    pass


def process(frame, p1, p2):
    """Applies the functions getROI, unlock, findLargestContour and text
    Parameters
    ----------
    frame : numpy array
        The frame to be processed
    p1 : tuple
        Top left of the detected license plates
    p2 : tuple
        Bottom right of the detected license plates
    Returns
    -------
    text : str
        the text read by the OCR engine (tesseract) after processing the image
    """

    roi = getROI(frame, p1, p2)
    roi = unlock(roi)
    roi = findLargestContour(roi)

    s = ts.image_to_string(Image.fromarray(roi))
    return "".join(s.split(" "))
