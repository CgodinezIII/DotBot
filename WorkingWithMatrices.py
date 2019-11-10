import numpy as np 
import cv2 as cv
import matplotlib.pyplot as plt

bgrImage = cv.imread('Glasses.PNG')
rgbImage = cv.cvtColor(bgrImage, cv.COLOR_BGR2RGB)
grayImage = cv.cvtColor(bgrImage, cv.COLOR_BGR2GRAY)


coordinates = []
pxSize = 6
thresh = 80

def resizeImage(image, maxWidth, maxHeight, pixelSize):
    if image.shape[1]*pixelSize <= maxWidth and image.shape[0]*pixelSize <= maxHeight:
        return image


def binarizeImage(grayscaleImage, thresh):
    binaryImage = grayscaleImage
    for i in range(binaryImage.shape[0]):
        for j in range(binaryImage.shape[1]):
            if binaryImage[i, j] >= thresh:
                binaryImage[i, j] = 1
            else:
                binaryImage[i, j] = 0
    return binaryImage



def getCoords(binaryImage, pixelSize):
    coordinates = []
    for i in range(binaryImage.shape[0]):
        for j in range(binaryImage.shape[1]):
            if binaryImage[i, j] == 255:
                coordinates.append([j*pixelSize, i*pixelSize])
    return coordinates


def grayScaleFloydSteinberg(grayscaleImage):
    for y in range(grayscaleImage.shape[0]-1):
        for x in range(grayscaleImage.shape[1]-1):
            oldPixVal = grayscaleImage[y,x]
            newPixVal = round(oldPixVal/255)*255
            error = oldPixVal-newPixVal
            grayscaleImage[y,x] = newPixVal
            grayscaleImage[y, x+1] = grayscaleImage[y, x+1] + (7/16)*error
            grayscaleImage[y+1, x-1] = grayscaleImage[y+1, x-1] + (3/16)*error
            grayscaleImage[y+1, x] = grayscaleImage[y+1, x] + (5/16)*error
            grayscaleImage[y+1, x+1] = grayscaleImage[y+1, x+1] + (1/16)*error
    return grayscaleImage

def colorScaleFloydSteinberg(RGBImage):
    for y in range(RGBImage.shape[0]-1):
        for x in range(RGBImage.shape[1]-1):
            for z in range(3):
                oldPixVal = RGBImage[y,x, z]
                newPixVal = round(oldPixVal/255)*255
                error = oldPixVal-newPixVal
                RGBImage[y,x, z] = newPixVal
                RGBImage[y, x+1, z] = RGBImage[y, x+1, z] + (7/16)*error
                RGBImage[y+1, x-1, z] = RGBImage[y+1, x-1, z] + (3/16)*error
                RGBImage[y+1, x, z] = RGBImage[y+1, x, z] + (5/16)*error
                RGBImage[y+1, x+1, z] = RGBImage[y+1, x+1, z] + (1/16)*error
    RGBImage = np.delete(RGBImage, RGBImage.shape[0]-1, 0)  #Delete the bottom row
    RGBImage = np.delete(RGBImage, RGBImage.shape[1]-1, 1)  #Delete the left most column
    return RGBImage
        

#binaryImage = binarizeImage(BWImage, 80)

ditheredImageGray = grayScaleFloydSteinberg(grayImage)
ditheredImageRGB = colorScaleFloydSteinberg(rgbImage)
#coords = getCoords(ditheredImage, 1)
#print(len(coords))
rgbImage = cv.cvtColor(bgrImage, cv.COLOR_BGR2RGB)

plt.subplot(131),plt.imshow(rgbImage)
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(132),plt.imshow(ditheredImageRGB)
plt.title('Color Dithered Image'), plt.xticks([]), plt.yticks([])
plt.subplot(133),plt.imshow(ditheredImageGray,cmap = 'gray')
plt.title('Binary Dithered Image'), plt.xticks([]), plt.yticks([])
plt.show()

