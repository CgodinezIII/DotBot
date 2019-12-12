import numpy as np 
import cv2 as cv
import matplotlib.pyplot as plt
import imutils
import math
import serial
import time


def resizeImage(image, maxWidth, maxHeight, pixelSpacing):

    print('Original dimensions: {}, {}'.format(image.shape[0], image.shape[1]))
    print("Resizing...")

    #Calculate target height and width of resized image given desired dimensions and pixel size
    targetWidth = math.floor(maxWidth/pixelSpacing)  
    targetHeight = math.floor(maxHeight/pixelSpacing)
    
    #Save the image width and height as variables
    imageWidth = image.shape[1]
    imageHeight = image.shape[0]
    

    #If the image is 'landscape' orientation, rotate 270 degrees to 'portrait' orientation
    if  imageWidth>imageHeight and targetWidth<targetHeight:
        image = imutils.rotate_bound(image, 270)
        print('flipped')
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
    print(dim)
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
def getCoordsGray(binaryImage, pixelSpacing):
    coordinates = []
    for i in range(binaryImage.shape[0]):
        for j in range(binaryImage.shape[1]):
            if binaryImage[i, j] == 0:
                coordinates.append([j*pixelSpacing, i*pixelSpacing])
    coordinates.append([0,-10]) #Go Back Home when complete
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
def coordStringArrayCreation(coordinateArray, coordsPerString):
    coordStringArray = []
    coordString = ""
    coordPos = 0
    remainder = len(coordinateArray)%coordsPerString
    #print(remainder)
    numComplete = int(len(coordinateArray)/coordsPerString)
    #print(numComplete)
    #Create Coordstring Array
    while(coordPos<len(coordinateArray)):
        coordString = ""
        for i in range(numComplete):
            for i in range(coordsPerString):
                if (i == coordsPerString-1):
                    #print(coordPos)
                    currCoord = coordinateArray[coordPos+i]
                    coordString += str(currCoord[0]) + ", " + str(currCoord[1])
                    coordPos += coordsPerString
                   
                    #print(coordPos)
                    coordStringArray.append(coordString)
                    coordString = ""  
                    #print(coordString)
                    #ser.write(str.encode(coordString)) 
                    #print("Send")
                else:
                    currCoord = coordinateArray[coordPos+i]
                    coordString = coordString + str(currCoord[0]) + ", " + str(currCoord[1]) + ", "  
                  
        coordString = "" 
        #print("coordString3")          
        for i in range(remainder):
            if (i == remainder-1):
                currCoord = coordinateArray[coordPos+i]
                coordString += str(currCoord[0]) + ", " + str(currCoord[1])
                coordPos += remainder
                #print("coordString")
                #coordStringArray.append(coordString)
                for i in range(coordsPerString-remainder):
                    coordString += ", -1, -1"
                coordStringArray.append(coordString)
                #coordString = "" 
                #print("Send")
            else:
                currCoord = coordinateArray[coordPos+i]
                
                coordString = coordString + str(currCoord[0]) + ", " + str(currCoord[1]) + ", "
                #coordStringArray.append(coordString)
                #print("coordString2")
                            
    return coordStringArray
def sendCoordsGray(stringArray, COMPort):
    print("Connecting to Serial...")
    ser = serial.Serial(COMPort, baudrate = 115200, timeout = 1)
    time.sleep(3)
    ser.write(str.encode("1")) 
    stringNum = 0
    #numCoords = len(stringArray)
    print("Sending Coords")
    

    while(stringNum<len(stringArray)):
         message = ser.readline().decode()
         #print(message.strip())
         
         if(message.strip() == 'Send New Coords'):
            print("Sending Package "+str(stringNum)+"/"+str(len(stringArray)))
            ser.write(str.encode(stringArray[stringNum]))
            
            stringNum = stringNum + 1
           
            

COMPort = "COM17"
maxWidth = 610
maxHeight = 915
pixelSpacing = 2 #Space between Pixels in mm

# # # print("Max Size: {} {}".format(maxWidth, maxHeight))
bgrImage = cv.imread(r'C:\Users\amiller\Documents\Fall2019\POE\DotBot\team.png')
rgbImage = cv.cvtColor(bgrImage, cv.COLOR_BGR2RGB)
# # #print("Scaling to {}, {}".format(maxWidth, maxHeight))
rgbImage = resizeImage(rgbImage,maxWidth, maxHeight, pixelSpacing)
grayImage = cv.cvtColor(rgbImage, cv.COLOR_RGB2GRAY)
# # print(grayImage.shape)


ditheredImageGray = grayScaleFloydSteinberg(grayImage)
print(ditheredImageGray)
ditheredImageRGB = colorScaleFloydSteinberg(rgbImage)
coords = getCoordsGray(ditheredImageGray, pixelSpacing)

print(len(coords))
# # #print(coords[9397])
stringArray = coordStringArrayCreation(coords, coordsPerString = 200)
# # #print(stringArray)


rgbImage = cv.cvtColor(bgrImage, cv.COLOR_BGR2RGB)
rgbImage = resizeImage(rgbImage,maxWidth,maxHeight,pixelSpacing)
plt.subplot(131),plt.imshow(rgbImage)
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(132),plt.imshow(ditheredImageRGB)
plt.title('Color Dithered Image'), plt.xticks([]), plt.yticks([])
plt.subplot(133),plt.imshow(ditheredImageGray,cmap = 'gray')
plt.title('Binary Dithered Image'), plt.xticks([]), plt.yticks([])
plt.show()

#sendCoordsGray(stringArray, COMPort)
