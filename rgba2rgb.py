
import cv2
#load image with alpha channel.  use IMREAD_UNCHANGED to ensure loading of alpha channel
image = cv2.imread('C:\\Users\\BURAK\\Desktop\\binarymask2json\\Data\\masks\\000000446.png', cv2.IMREAD_UNCHANGED)

#make mask of where the transparent bits are
trans_mask = image[:,:,3] == 0

#replace areas of transparency with white and not transparent
image[trans_mask] = [255, 255, 255, 255]

#new image without alpha channel...
new_img = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

cv2.imwrite("newImg.png", new_img)