import serial
import time



#
# Note 1: This python script was designed to run with Python 3.
#
# Note 2: The script uses "pyserial" which must be installed.  If you have
#         previously installed the "serial" package, it must be uninstalled
#         first.
#
# Note 3: While this script is running you can not re-program the Arduino.
#         Before downloading a new Arduino sketch, you must exit this
#         script first.
#


#
# Set the name of the serial port.  Determine the name as follows:
#	1) From Arduino's "Tools" menu, select "Port"
#	2) It will show you which Port is used to connect to the Arduino
#
# For Windows computers, the name is formatted like: "COM6"
# For Apple computers, the name is formatted like: "/dev/tty.usbmodemfa141"
#
arduinoComPort = "COM16"


#
# Set the baud rate
# NOTE1: The baudRate for the sending and receiving programs must be the same!
# NOTE2: For faster communication, set the baudRate to 115200 below
#        and check that the arduino sketch you are using is updated as well.
#
baudRate = 9600

#
# open the serial port
#
serialPort = serial.Serial(arduinoComPort, baudRate, timeout=1)
time.sleep(3) #delays to allow it to connect to the serial
#writes to the serial port to allow the arduino to begin reading
#serialPort.write(str.encode("begin"))



#
# main loop to read data from the Arduino, then display it
#
num = 800
coords = [[10, 2], [3, 4000], [5, 6], [7, 8]]
serialPort.write(str.encode("1")) 
coordPos = 0
while True:
    #
    # ask for a line of data from the serial port, the ".decode()" converts the
    # data from an "array of bytes", to a string
    #
    
    
    
    while(coordPos<len(coords)):
         
         
         time.sleep(1)
         message = serialPort.readline().decode()
         

         if(message.strip() == 'Send New Coord'):
            currCoord = coords[coordPos]
            currX = currCoord[0]
            currY = currCoord[1]
            print("Sending X")
            serialPort.write(str.encode(str(currX)))
            time.sleep(2)
            Coordinate = serialPort.readline()
            print(Coordinate)
           
            

         if(message.strip() == "Send Y"):
            currCoord = coords[coordPos]
            currX = currCoord[0]
            currY = currCoord[1]
            print("Sending Y")
            serialPort.write(str.encode(str(currY)))
            time.sleep(2)
            Coordinate = serialPort.readline()
            print(Coordinate)
            coordPos += 1
        
    
            
            
        
    '''
    newCoords = [[1, 1000], [12, 15]]
    for i in range(len(coords)):
        currCoord = coords[i]
        currX = currCoord[0]
        currY = currCoord[1]
        message = serialPort.readline().decode()
        if(len(message) > 0 and message == "Send X"):
            print("Sending" + str.encode(str(currX)))
            serialPort.write(str.encode(str(currX)))
            time.sleep(1)
        X = serialPort.readline().decode()
        message = serialPort.readline().decode()
        if(len(message) > 0 and message == "Send Y"):
            serialPort.write(str.encode(str(currY)))
            time.sleep(1)
        Y = serialPort.readline().decode()

        print(X)
        print(Y)
    '''