import serial  
import time
s2 = serial.Serial('COM6',115200,timeout=1) #opens a serial port (resets the device!)  
time.sleep(2) #give the device some time to startup (2 seconds)  
#write to the device’s serial port  
s2.write(str.encode("a[CD]\n")) #set the device address to AB  
time.sleep(0.1) #wait for settings to be applied  
s2.write(str.encode("c[1,0,5]\n")) #set number of retransmissions to 5  
time.sleep(0.1) #wait for settings to be applied  
s2.write(str.encode("c[0,1,30]\n")) #set FEC threshold to 30 (apply FEC to packets with payload >= 30)  
time.sleep(0.1) #wait for settings to be applied  

# s.write(str.encode("m[hello world!\0,CD]\n")) #send message to device with address CD  
# print("Message sent to CD...")


#read from the device’s serial port (should be done in a separate program):  
message = ""  
while True: #while not terminated  
 try:  
   byte = s2.read(1)
   if not byte:
     continue #read one byte (blocks until data available or timeout reached)  
   val = chr(byte[0])  
   if val=='\n': #if termination character reached  
     print (message) #print message  
     message = "" #reset message  
   else:  
     message = message + val #concatenate the message  
 except serial.SerialException:  
   continue #on timeout try to read again  
 except KeyboardInterrupt:  
   sys.exit() #on ctrl-c terminate program

