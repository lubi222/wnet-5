from vlc_serial import VLCDevice
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