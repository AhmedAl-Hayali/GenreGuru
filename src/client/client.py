import socket

class Client:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        """
        Establish connection with the backend server.
        """
        try:
            self.client_socket.connect((self.server_ip, self.server_port))
            print(f"Connected to backend server at {self.server_ip}:{self.server_port}")
            return True
        except socket.error as e:
            print(f"Connection error: {e}")
            return False

    def send_message(self, message):
        """
        Send message to the backend and receive response.
        """
        try:
            self.client_socket.sendall(message.encode("utf-8"))  # Send entire message
            response = self.client_socket.recv(4096).decode("utf-8")
            return response
        except socket.error as e:
            print(f"Communication error: {e}")
            return None

    def close(self):
        """
        Close the connection.
        """
        self.client_socket.close()
        print("Connection closed.")
