import socketserver
import pickle
import soundfile as sf

class MyTCPHandler(socketserver.StreamRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def save_nparr_to_wav(self, input, sampling_rate = 22050, output_dir = "reconstructed_song.wav"):
        sf.write(output_dir, input, sampling_rate)

    def handle(self):
        # self.rfile is a file-like object created by the handler.
        # We can now use e.g. readline() instead of raw recv() calls.
        # We limit ourselves to 10000 bytes to avoid abuse by the sender.
        # self.data = self.rfile.readline(10000).rstrip()
        # print(f"length of the predecoded data is: {len(self.data)}")

        # use length header
        length_str = self.rfile.read(10)
        length = int(length_str.decode("utf-8").strip())
        # self.data = self.rfile.read(length)

        # need to make sure that the server is capable of reading the entire message before unpickle
        stream = [] #splice the pieces together towards the end
        bytes_read = 0 # track how many bytes have been read
        while bytes_read < length:
            piece = self.rfile.read(min(4096, length - bytes_read))
            if not piece: break
            stream.append(piece)
            bytes_read += len(piece)

        self.data = b"".join(stream)
        print(f"\n{self.client_address[0]} wrote:")
        decoded_data = pickle.loads(self.data)
        print(f"shape of decoded_data is: {decoded_data.shape}")
        # print(f"content of decoded data: \n{decoded_data}")

        # Likewise, self.wfile is a file-like object used to write back
        # to the client
        self.wfile.write(self.data.upper())
        self.save_nparr_to_wav(decoded_data)

if __name__ == "__main__":    
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()