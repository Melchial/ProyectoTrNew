
from dataTranslate import DataTranslate
import cv2
from PyQt5.QtCore import QRect


qtRect =  QRect(159, 61, 253, 163)

rect = (qtRect.x(), qtRect.y(),qtRect.width(), qtRect.height() )

print(rect)

