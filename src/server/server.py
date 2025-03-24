import socket
import base64

# Define server details
HOST = "0.0.0.0"  # Listen on all available interfaces
PORT = 8000  # Ensure this matches what `local_server.py` connects to

def save_wav_file(encoded_wav, output_path="received_audio.wav"):
    """
    Decodes a Base64-encoded WAV file and saves it.
    """
    try:
        wav_data = base64.b64decode(encoded_wav)
        with open(output_path, "wb") as wav_file:
            wav_file.write(wav_data)
        print(f"WAV file saved successfully: {output_path}")
        return output_path
    except Exception as e:
        print(f"Error saving WAV file: {e}")
        return None

def process_request(message):
    """
    Processes incoming messages:
    - If a WAV file is received, it saves the file.
    - If a Spotify ID is received, it generates recommendations.
    """
    if message.startswith("WAV_FILE:"):
        encoded_wav = message[len("WAV_FILE:"):]
        saved_file = save_wav_file(encoded_wav)

        if saved_file:
            return "6rqhFgbbKwnb9MLmUQDhG6, 0VjIjW4GlUZAMYd2vXMi3b, 4iV5W9uYEdYUVa79Axb7Rh"
        else:
            return "ERROR: Failed to process WAV file."

    elif message.startswith("SPOTIFY_ID:"):
        spotify_id = message[len("SPOTIFY_ID:"):]
        print(f"Received Spotify ID: {spotify_id}")

        # Simulating recommendation engine
        return "6rqhFgbbKwnb9MLmUQDhG6, 0VjIjW4GlUZAMYd2vXMi3b, 4iV5W9uYEdYUVa79Axb7Rh"

    return "ERROR: Unknown request format."

def start_server():
    """
    Starts the backend TCP server that listens for incoming connections.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"Backend server listening on {HOST}:{PORT}")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")

        try:
            message = client_socket.recv(4096).decode("utf-8")
            response = process_request(message)
            client_socket.send(response.encode("utf-8"))

        except Exception as e:
            print(f"Error handling client: {e}")
            client_socket.send(f"Server error: {e}".encode("utf-8"))

        finally:
            client_socket.close()

if __name__ == "__main__":
    start_server()
