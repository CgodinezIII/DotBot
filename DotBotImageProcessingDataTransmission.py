import numpy as np 
import cv2 as cv
import matplotlib.pyplot as plt
import imutils
import math
import serial
import time


def resizeImage(image, maxWidth, maxHeight, pixelSpacing):

    #Calculate target height and width of resized image given desired dimensions and pixel size
    targetWidth = math.floor(maxWidth/pixelSpacing)  
    targetHeight = math.floor(maxHeight/pixelSpacing)
    
    #Save the image width and height as variables
    imageWidth = image.shape[1]
    imageHeight = image.shape[0]
    

    #Rotates image in order to get maximum use of designated space
    if  imageWidth>imageHeight and targetWidth<targetHeight:
        image = imutils.rotate_bound(image, 270)
        imageWidth = image.shape[1]
        imageHeight = image.shape[0]
    

    #If shrinking the image use cv.INTER_AREA as interpolation method
    if imageWidth>targetWidth or imageHeight>targetHeight:
        interpolationMethod = cv.INTER_AREA
    

    #If expanding image use cv.INTER_CUBIC as interpolation method
    else:
        interpolationMethod = cv.INTER_CUBIC


    #If the image to target width ratio is greater than the height ratio, set width to max and scale height
    if imageWidth/targetWidth >= imageHeight/targetHeight:
        newWidth = targetWidth
        newHeight = int((targetWidth/imageWidth)*imageHeight)
       
    #If the image to target height ratio is greater than the width ratio, set height to max and scale width
    else:
        newWidth = int((targetHeight/imageHeight)*imageWidth)
        newHeight = targetHeight

    #Resize image based on new dimensions    
    dim = (newWidth, newHeight)
    image = cv.resize(image, dim, interpolation  = interpolationMethod)
    print('Final dimensions: {}mm, {}mm ({}in, {}in)'.format(image.shape[0], image.shape[1], round(image.shape[0]/2.54, 2), round(image.shape[1]/2.54, 2)))
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
    numComplete = int(len(coordinateArray)/coordsPerString)

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
                    coordStringArray.append(coordString)
                    coordString = ""  
                    
                else:
                    currCoord = coordinateArray[coordPos+i]
                    coordString = coordString + str(currCoord[0]) + ", " + str(currCoord[1]) + ", "  
                  
        coordString = "" 
              
        for i in range(remainder):
            if (i == remainder-1):
                currCoord = coordinateArray[coordPos+i]
                coordString += str(currCoord[0]) + ", " + str(currCoord[1])
                coordPos += remainder
            
                for i in range(coordsPerString-remainder):
                    coordString += ", -1, -1"
                coordStringArray.append(coordString)
                
            else:
                currCoord = coordinateArray[coordPos+i]
                coordString = coordString + str(currCoord[0]) + ", " + str(currCoord[1]) + ", "
               
                            
    return coordStringArray
def sendCoordsGray(stringArray, COMPort):
    print("Connecting to Serial...")
    try:
        ser = serial.Serial(COMPort, baudrate = 115200, timeout = 1)  
        time.sleep(3)
        ser.write(str.encode("1")) 
        stringNum = 0
        print("Sending Coords")
        

        while(stringNum<len(stringArray)):
            message = ser.readline().decode()
            
            if(message.strip() == 'Send New Coords'):
                print("Sending Package "+str(stringNum)+"/"+str(len(stringArray)))
                ser.write(str.encode(stringArray[stringNum]))
                
                stringNum = stringNum + 1
    except:
        print('Ensure Arduino is plugged in to correct port')
def visualize(rgbImage, ditheredImageGray, ditheredImageRGB):
    plt.subplot(131),plt.imshow(rgbImage)
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(132),plt.imshow(ditheredImageRGB)
    plt.title('Color Dithered Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(133),plt.imshow(ditheredImageGray,cmap = 'gray')
    plt.title('Binary Dithered Image'), plt.xticks([]), plt.yticks([])
    plt.show()
def processing(bgrImage, maxWidth, maxHeight, pixelSpacing):
    rgbImage = cv.cvtColor(bgrImage, cv.COLOR_BGR2RGB)
    rgbImageScaled = resizeImage(rgbImage,maxWidth,maxHeight,pixelSpacing)
    grayImage = cv.cvtColor(rgbImageScaled, cv.COLOR_RGB2GRAY)
    ditheredImageGray = grayScaleFloydSteinberg(grayImage)
    ditheredImageRGB = colorScaleFloydSteinberg(rgbImageScaled)
    return rgbImage, ditheredImageGray, ditheredImageRGB 
       

if __name__ == '__main__':
    COMPort = "COM17"
    imagePath = r'C:\Users\amiller\Documents\Fall2019\POE\Dotbot\einstein.jpg'
    maxWidth = 100 #mm
    maxHeight = 100 #mm
    pixelSpacing = 1 #Space between Pixels in mm

    bgrImage = cv.imread(imagePath)
    rgbImage, ditheredImageGray, ditheredImageRGB = processing(bgrImage, maxWidth, maxHeight, pixelSpacing)
    coords = getCoordsGray(ditheredImageGray, pixelSpacing)
    print("Number of Dots: {}".format(len(coords)))
    print("Approximate Print Time: {} Hrs".format(round(len(coords)/7200, 2)))
    visualize(rgbImage, ditheredImageGray, ditheredImageRGB)

    #stringArray = coordStringArrayCreation(coords, coordsPerString = 200)
    # sendCoordsGray(stringArray, COMPort)



