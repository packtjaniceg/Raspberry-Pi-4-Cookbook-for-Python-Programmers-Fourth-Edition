#!/usr/bin/python3
'''openimage.py'''
import cv2

# Load a color image in grayscale
IMG = cv2.imread('testimage.jpg', cv2.IMREAD_GRAYSCALE)
cv2.imshow('image', IMG)
cv2.waitKey(0)
cv2.destroyAllWindows()

