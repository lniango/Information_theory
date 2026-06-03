import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack
from skimage.util import img_as_ubyte
import matplotlib.image as mpimg
import cv2 as cv

def dct(gray_img):
    # transform: 2D DCT
    z_dct = fftpack.dct(fftpack.dct(gray_img.T, norm='ortho').T, norm='ortho')
    # print dct 
    np.set_printoptions(precision=1, linewidth=140, suppress=True)

    return z_dct

#test dct 
gray_img = cv.imread("images/super_mario_head.jpg", cv.IMREAD_GRAYSCALE)
cv.imshow("Mario", gray_img)
cv.waitKey(0)
cv.destroyAllWindows()

dct_coeff = dct(gray_img)
print(f"DCT cocefficients: {dct_coeff}")