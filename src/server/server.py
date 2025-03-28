import socketserver
import pickle
import socket

class ServerCommunicationModule(socketserver.StreamRequestHandler):
    def __init__(self, ip, port):
        self.server = socketserver.TCPServer((ip, port))
    
    def start_server(self):
        self.server.serve_forever()
    
    def receive_client_request(self):
        raw_len_data = self.rfile.read(10)
        msg_len = int(raw_len_data.decode("utf-8").strip())

        data_stream = []
        bytes_read = 0
        while bytes_read < msg_len:
            piece = self.rfile.read(min(4096, msg_len - bytes_read))
            if not piece: break
            data_stream.append(piece)
            bytes_read += len(piece)

        data = b"".join(data_stream)
        return pickle.loads(data)

    def send_client_response(self, recommendations, ip, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((ip, port))
            sock.sendall(bytes(recommendations, "utf-8"))
            sock.sendall(b"\n")

    def close_connection(self):
        self.server.server_close()
    

# import socket

# def run_server():
#     # create a socket object
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#     server_ip = ""
#     port = ""

#     # bind the socket to a specific address and port
#     server.bind((server_ip, port))
#     # listen for incoming connections
#     server.listen(0)
#     print(f"Listening on {server_ip}:{port}")

#     # accept incoming connections
#     client_socket, client_address = server.accept()
#     print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

#     # receive data from the client
#     while True:
#         request = client_socket.recv(1024)
#         request = request.decode("utf-8") # convert bytes to string
        
#         # if we receive "close" from the client, then we break
#         # out of the loop and close the conneciton
#         if request.lower() == "close":
#             # send response to the client which acknowledges that the
#             # connection should be closed and break out of the loop
#             client_socket.send("closed".encode("utf-8"))
#             break

#         print(f"Received: {request}")

#         response = "accepted".encode("utf-8") # convert string to bytes
#         # convert and send accept response to the client
#         client_socket.send(response)

#     # close connection socket with the client
#     client_socket.close()
#     print("Connection to client closed")
#     # close server socket
#     server.close()


# run_server()
