import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack
from skimage.util import img_as_ubyte
import matplotlib.image as mpimg
import cv2 as cv

def pad_image(image, bloc_size):
    h, w = image.shape
    
    pad_h = (bloc_size - h % bloc_size) % bloc_size
    pad_w = (bloc_size - w % bloc_size) % bloc_size
    # top, bottom | left, right
    image = np.pad(image, pad_width=((0, pad_h), (0, pad_w)))
    
    return image, pad_h, pad_w

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
h, w = gray_img.shape
"""cv.imshow("Mario", gray_img)
cv.waitKey(0)
cv.destroyAllWindows()

dct_coeff = dct(gray_img)
print(f"DCT cocefficients: {dct_coeff}")"""

#test blocs
gray_img_padded, pad_h, pad_w = pad_image(gray_img, bloc_size=8) # pad image
dct_per_bloc = dct_on_blocs(gray_img_padded)
#print(f"Shape of blocs : {dct_per_bloc[0].shape}")

#Display dct image
dct_per_bloc_np = np.array(dct_per_bloc) # from list to np array
print(f"Shape - Image DCT bloc BEFORE: {dct_per_bloc_np.shape}") # 1444x8x8
#Remove padding on dct coefficient
dct_per_bloc_np = dct_per_bloc_np[:gray_img_padded.shape[0] - pad_h, :gray_img_padded.shape[1] - pad_w]
#dct_per_bloc_np = dct_per_bloc_np.reshape((h, w))
print(f"Shape - Image DCT bloc AFTER: {dct_per_bloc_np.shape}") # 1444x8x8
plt.imshow(dct_per_bloc_np, cmap='gray')
plt.show()