import socket
import sys
import librosa
import pickle
import numpy as np
HOST, PORT = "localhost", 9999

data, _ = librosa.load("src/audio/The Weeknd - Out of Time.wav",sr= 22050)
print(f"the current shape of data is: {data.shape}")
# data = np.random.rand(256)
# data = str(data)
# print(f"the string converted data length is: {len(data)}")

# data = "my message"
# np.savetxt("output", data, delimiter = ", ")
# print(data)
# Create a socket (SOCK_STREAM means a TCP socket)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    # byte_message = bytes(data, "utf-8")
    byte_message = pickle.dumps(data)  
    length = len(byte_message)
    sock.sendall(bytes(f"{length:<10}", "utf-8"))
    # print(f"byte converted length of send is: {length}")
    sock.sendall(byte_message)

    # Receive data from the server and shut down
    received = str(sock.recv(1024))
