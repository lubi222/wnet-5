try:
    from vlc_serial import VLCDevice
except Exception:
    # Fallback stub when vlc_serial is not available (e.g., editor linting or missing module).
    # This provides the minimal API used by vlc_chat.py so the file can be opened/run without import errors.
    class VLCDevice:
        def __init__(self, port, address):
            self.port = port
            self.address = address

        def open(self):
            print(f"[{self.address}] (stub) device opened on port {self.port}")

        def start_reader(self):
            print(f"[{self.address}] (stub) reader started")

        def send_message(self, msg, peer):
            # In the real implementation this would send over a serial link.
            print(f"[{self.address}] (stub) -> {peer}: {msg}")

        def close(self):
            print(f"[{self.address}] (stub) device closed")

import threading, time


def chat_instance(port, address, peer):
    dev = VLCDevice(port, address)
    dev.open()
    dev.start_reader()

    print(f"\n[{address}] Chat started. Type messages to send to {peer}. \n")
    try:
        while True:
            msg = input(f"[{address}] > ")
            dev.send_message(msg, peer)
    except KeyboardInterrupt:
        dev.close()


# Example usage:
# One terminal:
#   python vlc_chat.py COM4 AB CD
# Another terminal:
#   python vlc_chat.py COM5 CD AB
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print("Usage: python vlc_chat.py <port> <address> <peer>")
        sys.exit(1)
    chat_instance(sys.argv[1], sys.argv[2], sys.argv[3])

# python vlc_chat.py COM4 AB CD
# python vlc_chat.py COM5 CD AB