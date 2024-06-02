import socket
import threading
import os

# Fungsi untuk memproses permintaan HTTP
def handle_client(client_socket):
    try:
        while True:
            # 1. Terima dan parse permintaan HTTP
            request = client_socket.recv(1024).decode()
            if not request:
                break
            print(f"Received request:\n{request}")
            
            # Cari file
            lines = request.split("\r\n")
            if len(lines) > 0:
                first_line = lines[0]
                parts = first_line.split()
                if len(parts) > 1 and parts[0] == 'GET':
                    filename = parts[1]
                    if filename == '/':
                        filename = 'HelloWorld.html'
                    else:
                        filename = filename.lstrip('/')
                else:
                    filename = 'HelloWorld.html'
            else:
                filename = 'HelloWorld.html'
            
            # 2. Ambil file yang diminta
            if os.path.exists(filename):
                with open(filename, 'rb') as f:
                    file_data = f.read()
                response_body = file_data
                response_headers = (
                    "HTTP/1.1 200 OK\r\n"
                    "Content-Type: text/html\r\n"
                    f"Content-Length: {len(response_body)}\r\n"
                    "Connection: keep-alive\r\n"
                    "\r\n"
                )
            else:
                response_body = b"404 Not Found"
                response_headers = (
                    "HTTP/1.1 404 Not Found\r\n"
                    "Content-Type: text/html\r\n"
                    f"Content-Length: {len(response_body)}\r\n"
                    "Connection: keep-alive\r\n"
                    "\r\n"
                )
            
            response = response_headers.encode() + response_body

            # 3. Kirim respons ke klien
            client_socket.sendall(response)
    except Exception as e:
        print(f"Error handling request: {e}")
    finally:
        client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 6790))  # Port 6790
    server_socket.listen(5)
    print("Server listening on port 6790")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")
            thread = threading.Thread(target=handle_client, args=(client_socket,))
            thread.start()
    except KeyboardInterrupt:
        print("\nShutting down the server.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
