import serial  
import threading
import time
s = serial.Serial('COM4',115200,timeout=1) #opens a serial port (resets the device!)  
time.sleep(2) #give the device some time to startup (2 seconds)  
#write to the device’s serial port  
s.write(str.encode("a[AB]\n")) #set the device address to AB  
time.sleep(0.1) #wait for settings to be applied  
s.write(str.encode("c[1,0,5]\n")) #set number of retransmissions to 5  
time.sleep(0.1) #wait for settings to be applied  
s.write(str.encode("c[0,1,10]\n")) #set FEC threshold to 30 (apply FEC to packets with payload >= 30)  
time.sleep(0.1) #wait for settings to be applied  
# s2.write(str.encode("c[0,2,4]\n")) #set Channel busy threshold (CWmin) 
# time.sleep(0.1) #wait for settings to be applied  

# s.write(str.encode("m[hello world!\0,CD]\n")) #send message to device with address CD  
# print("Message sent to CD...")
time.sleep(0.1)

# --------------------------------------------------------------

# threading.Thread(target=reader, daemon=True).start()
def receive():
  message = ""  
  while True: #while not terminated  
    try:  
      byte = s.read(1) #read one byte (blocks until data available or timeout reached)  
      if not byte:
        continue
      val = chr(byte[0])  
      if val=='\n': #if termination character reached  
        if(message.startswith("m[R,D")):
          print("", message[6:-1], end='') #print message (cause it ends in newline)  
        elif(message.startswith("s[R,D")):
           print(f" (from: {message[6:8]})")
        message = "" #reset message  
      else:  
        message = message + val #concatenate the message  
    except serial.SerialException:  
      continue #on timeout try to read again  
    except KeyboardInterrupt:  
      sys.exit() #on ctrl-c terminate program

threading.Thread(target=receive, daemon=True).start()

# # --- interactive loop ---
print("Type a message and press Enter (Ctrl+C to exit):")
while True:
    try:
        text = input("> ")
        if text.strip() == "":
            continue
        s.write(str.encode(f"m[{text}\0,CD]\n")) #send message to device with address CD  
        time.sleep(0.15)
    except KeyboardInterrupt:
        break

# s.close()
# print("Connection closed.")
# --------------------------------------------------------------

# read from the device’s serial port (should be done in a separate program):  

