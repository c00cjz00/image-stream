'''
Code from:
https://gist.github.com/kittinan/e7ecefddda5616eab2765fdb2affed1b
'''

import sys
import cv2
import socket
import pickle
import struct

class Client():
    def __init__(self):
        # self.host = "127.0.0.1"
        # self.port = 6666

        self.vcapture = cv2.VideoCapture(0)
        self.vcapture.set(3, 320)
        self.vcapture.set(4, 240)
        self.encode_param = [int(cv2.IMWRITE_WEBP_QUALITY), 90]

        self.isCapturing = True

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.isConnected = False

    def connect(self, host, port):
        try:
            self.sock.connect((host, port))
            self.isConnected = True
        except ConnectionRefusedError:
            print(f"Cannot connect to the server: {host}: {port}")

    def disconnect(self):
        try:
            h, p = self.sock.getpeername()
            print(f"Closing connection to: {h}: {p}")
        except:
            print("Client is not connected.")
        finally:
            self.sock.close()
            self.isConnected = False

    def capture(self):
        if not self.vcapture.isOpened():
            print("Webcam cannot be opened")
            return
        
        _, frame = self.vcapture.read()

        return frame
    
    def get_prediction(self, frame):
        _, frame = cv2.imencode('.jpg', frame, self.encode_param)

        data = pickle.dumps(frame, 0)
        size = len(data)

        self.sock.sendall(struct.pack(">L", size) + data)



def main():
    host = "127.0.0.1"
    port = 6666

    client = Client()
    client.connect(host, port)
    
    if client.isConnected:
        while True:
            frame = client.capture()
            cv2.imshow('Window',frame)

            client.get_prediction(frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    client.disconnect()

if __name__ == '__main__':
    main()

# host = "127.0.0.1"
# #host = "192.168.2.101"
# port = 6666

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# try:
#     s.connect((host, port))
# except ConnectionRefusedError:
#     print(f"Cannot connect to the server: {host}:{port}")
#     sys.exit()

# capture = cv2.VideoCapture(0)
# capture.set(3, 320)
# capture.set(4, 240)

# encode_param = [int(cv2.IMWRITE_WEBP_QUALITY), 90]

# if capture.isOpened():
#     try:

#         while True:
#             _, frame = capture.read()

#             encode, frame_enc = cv2.imencode('.jpg', frame, encode_param)

#             data = pickle.dumps(frame_enc, 0)
#             size = len(data)
#             #print(print(f"length: {size}"))

#             s.sendall(struct.pack(">L", size) + data)

#             cv2.imshow('Window', frame)

#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
    
#     except BrokenPipeError:
#         print("The connection with the server has been closed.")
#     finally:
#         capture.release()
# else:
#     print("Webcam cannot be opened")

# s.close()