from vlc_serial import VLCDevice
import time

# replace COM4 with your port
dev = VLCDevice(port='COM4', address='AB')
dev.open()
dev.start_reader()

time.sleep(1)
dev.send_cmd("p")  # ask version
time.sleep(0.5)
dev.send_message("hello", "FF")  # broadcast
time.sleep(5)
dev.close()
