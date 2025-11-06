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
s.write(str.encode("c[0,2,16]\n")) #set Channel busy threshold (CWmin) 
time.sleep(0.1) #wait for settings to be applied  



# --------------------------------------------------------------
done_event = threading.Event()

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
        elif(message.startswith("m[D")):
          print("message done message received: ", message)
          done_event.set()
          # received message done command m[D], so immediately generate message
          #  s.write(str.encode(f"m[HELLO!\0,CD]\n"))
          #  time.sleep(0.1)
        message = "" #reset message  
      else:  
        message = message + val #concatenate the message  
    except serial.SerialException:  
      continue #on timeout try to read again  
    except KeyboardInterrupt:  
      print('bye') #on ctrl-c terminate program


def auto_sender(dest="CD"):
    seq = 0
    while True:
        try:
          # wait for the m[D] notification from receive()
          done_event.wait()
          done_event.clear()
          seq += 1
          # ensure no spaces in address, include null terminator
          cmd = str.encode(f"m[MSG{seq}\0,CD]\n")
          
          s.write(cmd)

          print("auto_sender SENT:", cmd)
          time.sleep(0.02)
            # optionally log/send timestamp here
        except Exception as e:
            print("write error:", e)
        # small guard delay to protect MCU/USB stack
        


threading.Thread(target=receive, daemon=True).start()
threading.Thread(target=auto_sender, daemon=True).start()
s.write(str.encode("m[hello world!\0,CD]\n")) #send message to device with address CD  
print("initial message sent to CD...")
# time.sleep(0.1)

# # --- interactive loop (FROM CHAT) (!) ---
# print("Type a message and press Enter (Ctrl+C to exit):")
try:
  while True:
    # time.sleep(0.01)
    pass
except KeyboardInterrupt:
  print('exiting"')
    # try:
    #     text = input("> ")
    #     if text.strip() == "":
    #         continue
    #     s.write(str.encode(f"m[{text}\0,CD]\n")) #send message to device with address CD  
    #     time.sleep(0.15)
    # except KeyboardInterrupt:
    #     break

# s.close()
# print("Connection closed.")
# --------------------------------------------------------------

# read from the device’s serial port (should be done in a separate program):  

