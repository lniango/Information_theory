import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack
from skimage.util import img_as_ubyte
import matplotlib.image as mpimg
import cv2 as cv


def bloc_pixels(gray_img, bloc_size=8):
    """Divide images into parts of size bloc_size x bloc_size"""
    h, w = gray_img.shape
    blocks = []
    for i in range(0, h, bloc_size):
        for j in range(0, w, bloc_size):
            bloc8x8 = gray_img[i:i+bloc_size, j:j+bloc_size]
            blocks.append(bloc8x8)
    return blocks    
             
             

def dct(gray_img, show=False):
    # transform: 2D DCT
    # Applying 2 DCT 1D wrt rows and cols
    z_dct = fftpack.dct(gray_img, axis=0, norm='ortho')
    z_dct = fftpack.dct(z_dct, axis=1, norm='ortho')
    # print dct 
    if show:
        np.set_printoptions(precision=1, linewidth=140, suppress=True)

    return z_dct

def dct_on_blocs(gray_img, bloc_size=8):
    blocks = bloc_pixels(gray_img, bloc_size)
    dct_per_bloc = []
    for bloc in blocks:
        dct_per_bloc.append(dct(bloc))
        
    return dct_per_bloc



#test dct 
gray_img = cv.imread("images/super_mario_head.jpg", cv.IMREAD_GRAYSCALE)
"""cv.imshow("Mario", gray_img)
cv.waitKey(0)
cv.destroyAllWindows()

dct_coeff = dct(gray_img)
print(f"DCT cocefficients: {dct_coeff}")"""

#test blocs
dct_per_bloc = dct_on_blocs(gray_img)
print(f"Shape of blocs : {dct_per_bloc[0].shape}")

#Display dct image
