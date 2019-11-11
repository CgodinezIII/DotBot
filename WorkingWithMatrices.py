import numpy as np 
import cv2 as cv
import matplotlib.pyplot as plt
import imutils
import math


def resizeImage(image, maxWidth, maxHeight, pixelSize):

    print('Original dimensions: {}'.format(image.shape))
    targetWidth = math.floor(maxWidth/pixelSize)
    targetHeight = math.floor(maxHeight/pixelSize)

    if image.shape[1]>image.shape[0]:
        image = imutils.rotate_bound(image, 270)
        print('flipped')
    
    imageWidth = image.shape[1]
    imageHeight = image.shape[0]

    if imageWidth>targetWidth or imageHeight>targetHeight:
        interpolationMethod = cv.INTER_AREA
    
    else:
        interpolationMethod = cv.INTER_CUBIC
        #interpolationMethod = cv.INTER_LINEAR    worse but faster

    if imageWidth/targetWidth >= imageHeight/targetHeight:
        print('Scaling based on width')
        newWidth = targetWidth
        newHeight = int((targetWidth/imageWidth)*imageHeight)
       
    else:
        print('Scaling based on height')
        newWidth = int((targetHeight/imageHeight)*imageWidth)
        newHeight = targetHeight
        
    dim = (newWidth, newHeight)
    image = cv.resize(image, dim, interpolation  = interpolationMethod)
    print('Final dimensions: {}'.format(image.shape))
    return image



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



def getCoords(binaryImage, pixelSize):
    coordinates = []
    for i in range(binaryImage.shape[0]):
        for j in range(binaryImage.shape[1]):
            if binaryImage[i, j] == 255:
                coordinates.append([j*pixelSize, i*pixelSize])
    coordinates.append([0,0]) #Go Back Home when complete
    return coordinates




bgrImage = cv.imread('Google.png')
rgbImage = cv.cvtColor(bgrImage, cv.COLOR_BGR2RGB)
rgbImage = resizeImage(rgbImage,85,110,1)
grayImage = cv.cvtColor(rgbImage, cv.COLOR_RGB2GRAY)

ditheredImageGray = grayScaleFloydSteinberg(grayImage)
ditheredImageRGB = colorScaleFloydSteinberg(rgbImage)
#coords = getCoords(ditheredImage, 1)
#print(len(coords))
rgbImage = cv.cvtColor(bgrImage, cv.COLOR_BGR2RGB)
rgbImage = resizeImage(rgbImage,850,1100,1)
plt.subplot(131),plt.imshow(rgbImage)
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(132),plt.imshow(ditheredImageRGB)
plt.title('Color Dithered Image'), plt.xticks([]), plt.yticks([])
plt.subplot(133),plt.imshow(ditheredImageGray,cmap = 'gray')
plt.title('Binary Dithered Image'), plt.xticks([]), plt.yticks([])
plt.show()

