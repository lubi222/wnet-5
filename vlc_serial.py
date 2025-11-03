import serial
import time
import threading

class VLCDevice:
    def __init__(self, port, address):
        self.port = port
        self.address = address
        self.serial = None
        self.running = False

    def open(self):
        """Open the serial port and initialize the VLC device."""
        self.serial = serial.Serial(self.port, 115200, timeout=1)
        time.sleep(2)  # wait for Arduino reset
        self._setup_device()
        print(f"[+] Device {self.address} initialized on {self.port}")

    def _setup_device(self):
        """Reapply settings after every reset."""
        cmds = [
            f"a[{self.address}]",
            "c[1,0,5]",   # retransmissions = 5
            "c[0,1,30]",  # FEC threshold = 30
            "c[0,2,10]",  # channel busy threshold = 10
            "c[0,3,1]"    # enable light emission
        ]
        for cmd in cmds:
            self.send_cmd(cmd)
            time.sleep(0.1)

    def send_cmd(self, cmd):
        """Send a raw command to the Arduino."""
        if self.serial:
            self.serial.write((cmd + "\n").encode('ascii'))

    def send_message(self, msg, dest):
        """Send a message to another VLC node."""
        # must end message with '\0'
        formatted = f"m[{msg}\\0,{dest}]"
        self.send_cmd(formatted)

    def read_loop(self):
        """Continuously read serial output from device."""
        self.running = True
        buffer = ""
        while self.running:
            try:
                line = self.serial.readline().decode(errors='ignore').strip()
                if line:
                    print(f"[{self.address}] {line}")
            except KeyboardInterrupt:
                break
            except serial.SerialException:
                continue

    def start_reader(self):
        """Start reading in a background thread."""
        t = threading.Thread(target=self.read_loop, daemon=True)
        t.start()

    def close(self):
        """Close serial port."""
        self.running = False
        if self.serial:
            self.serial.close()