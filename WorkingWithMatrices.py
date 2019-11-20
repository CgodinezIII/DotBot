import numpy as np 
import cv2 as cv
import matplotlib.pyplot as plt
import imutils
import math
import serial
import time


def resizeImage(image, maxWidth, maxHeight, pixelSize):

    print('Original dimensions: {}'.format(image.shape))

    #Calculate target height and width of resized image given desired dimensions and pixel size
    targetWidth = math.floor(maxWidth/pixelSize)  
    targetHeight = math.floor(maxHeight/pixelSize)

    #If the image is 'landscape' orientation, rotate 270 degrees to 'portrait' orientation
    if image.shape[1]>image.shape[0]:
        image = imutils.rotate_bound(image, 270)
        print('flipped')
    
    #Save the image width and height as variables
    imageWidth = image.shape[1]
    imageHeight = image.shape[0]

    #If shrinking the image use cv.INTER_AREA as interpolation method
    if imageWidth>targetWidth or imageHeight>targetHeight:
        interpolationMethod = cv.INTER_AREA
    
    #If expanding image use cv.INTER_CUBIC or cv.INTER_LINEAR as interpolation method
    else:
        interpolationMethod = cv.INTER_CUBIC
        #interpolationMethod = cv.INTER_LINEAR    worse but faster

    #If the image to target width ratio is greater than the height ratio, set width to max and scale height
    if imageWidth/targetWidth >= imageHeight/targetHeight:
        print('Scaling based on width')
        newWidth = targetWidth
        newHeight = int((targetWidth/imageWidth)*imageHeight)
       
    #If the image to target height ratio is greater than the width ratio, set height to max and scale width
    else:
        print('Scaling based on height')
        newWidth = int((targetHeight/imageHeight)*imageWidth)
        newHeight = targetHeight

    #Resize image based on new dimensions    
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
    grayscaleImage = np.delete(grayscaleImage, grayscaleImage.shape[0]-1, 0)  #Delete the bottom row
    grayscaleImage = np.delete(grayscaleImage, grayscaleImage.shape[1]-1, 1)  #Delete the left most column
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



def getCoordsGray(binaryImage, pixelSize):
    coordinates = []
    for i in range(binaryImage.shape[0]):
        for j in range(binaryImage.shape[1]):
            if binaryImage[i, j] == 0:
                coordinates.append([j*pixelSize, i*pixelSize])
    coordinates.append([0,0]) #Go Back Home when complete
    return coordinates


def getCoordsRGB(rgbImage, pixelSize):
    redCoordinates = []
    blueCoordinates = []
    greenCoordinates = []

    for i in range(rgbImage.shape[0]):
        for j in range(rgbImage.shape[1]):
            for z in range(2):
                if binaryImage[i, j, z] == 255 and z == 0:
                    redCoordinates.append([j*pixelSize, i*pixelSize])
                elif binaryImage[i, j, z] == 255 and z == 1:
                    greenCoordinates.append([j*pixelSize, i*pixelSize]) 
                elif binaryImage[i, j, z] == 255 and z == 2:
                    blueCoordinates.append([j*pixelSize, i*pixelSize]) 
    redCoordinates.append([0,0]) #Go Back Home when complete
    greenCoordinates.append([0,0]) #Go Back Home when complete
    blueCoordinates.append([0,0]) #Go Back Home when complete
    return redCoordinates, greenCoordinates, blueCoordinates

def sendCoordsGray(coordinateArray, COMPort):
    ser = serial.Serial(COMPort, baudrate = 9600, timeout = 1)
    time.sleep(3)
    ser.write(str.encode("1")) 
    coordPos = 0
    
    while(coordPos<len(coordinateArray)):
         print(coordinateArray[coordPos])
         currCoord = coordinateArray[coordPos]
         currX = currCoord[0]
         currY = currCoord[1]
         
         time.sleep(1)
         message = ser.readline().decode()

         if(message.strip() == 'Send New Coord'):
            print("Sending X")
            ser.write(str.encode(str(currX)))
            time.sleep(2)
            Coordinate = ser.readline().decode()
            print(Coordinate.strip())
           
            

         if(message.strip() == "Send Y"):
            print("Sending Y")
            ser.write(str.encode(str(currY)))
            time.sleep(2)
            Coordinate = ser.readline().decode()
            print(Coordinate.strip())
            coordPos += 1
        
        


COMPort = 'COM16' 
bgrImage = cv.imread(r'C:\Users\amiller\Documents\Fall2019\POE\DotBot\Smile.png')
rgbImage = cv.cvtColor(bgrImage, cv.COLOR_BGR2RGB)
rgbImage = resizeImage(rgbImage,85,110,1)
grayImage = cv.cvtColor(rgbImage, cv.COLOR_RGB2GRAY)

ditheredImageGray = grayScaleFloydSteinberg(grayImage)
ditheredImageRGB = colorScaleFloydSteinberg(rgbImage)
coords = getCoordsGray(ditheredImageGray, 2)
print("Sending coords...")
sendCoordsGray(coords, COMPort)
#print(len(coords))
print(getCoordsGray(ditheredImageGray, 2))
rgbImage = cv.cvtColor(bgrImage, cv.COLOR_BGR2RGB)
rgbImage = resizeImage(rgbImage,85,110,1)
plt.subplot(131),plt.imshow(rgbImage)
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(132),plt.imshow(ditheredImageRGB)
plt.title('Color Dithered Image'), plt.xticks([]), plt.yticks([])
plt.subplot(133),plt.imshow(ditheredImageGray,cmap = 'gray')
plt.title('Binary Dithered Image'), plt.xticks([]), plt.yticks([])
plt.show()

