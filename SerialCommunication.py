import serial
ser = serial.Serial("COM17",timeout=5) # everything else is default
ser.write(2)
print("RECIEVED BACK:",repr(ser.read(5000)))