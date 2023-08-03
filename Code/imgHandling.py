import cv2
import math

# class ImgHandler:
def getRatio(img):
    img = cv2.imread(img)
    aspect_ratio = 1
    height, width, _ = img.shape
    if width > height:
        aspect_ratio = width / height
    else:
        aspect_ratio = height/ width
    return aspect_ratio

def getFontSizeThickness(img):
    FONT_SCALE = 6e-4  # Adjust for larger font size in all images
    THICKNESS_SCALE = 5e-4  # Adjust for larger thickness in all images

    img = cv2.imread(img)
    height, width, _ = img.shape

    font_scale = min(width, height) * FONT_SCALE
    thickness = math.ceil(min(width, height) * THICKNESS_SCALE)
    return (font_scale, thickness)