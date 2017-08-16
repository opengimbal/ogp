import sys
import serial
import time
F = 'data'

s = serial.Serial('/dev/ttyUSB0', 9600)## serial to arduino
time.sleep(2)   ## strategic buffering, possibly unnecessary



line =s.readline() # should block, not take anything less than 14 bytes



while 1:
    serOut = ['a001','a002']

    print(line)
    print ("recived")
    s.flushInput()
    command = str(input('enter command:'))
    print ('sending')
    s.write(command.encode('utf-8'))
    s.write(bytes('\n','utf-8'))
    
    #data = s.readline().decode('ascii') 
    print (command)
    print(line)


