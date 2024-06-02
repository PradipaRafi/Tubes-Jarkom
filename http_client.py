import socket
import sys
import signal

def http_client(server_ip, port, path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))

    def signal_handler(sig, frame):
        print("\nInterrupt received, closing socket.")
        client_socket.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    try:
        while True:
            request = f"GET {path} HTTP/1.1\r\nHost: {server_ip}\r\nConnection: keep-alive\r\n\r\n"
            client_socket.sendall(request.encode())

            response = b""
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                response += data
            
            if response:
                print(response.decode())

            print("\nPress Enter to send the request again or Ctrl+C to exit...")
            input()  #Input User

    except KeyboardInterrupt:
        signal_handler(None, None)
    finally:
        client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python http_client.py <server_ip> <port> <path>")
        sys.exit(1)
    
    server_ip = sys.argv[1]
    port = int(sys.argv[2])
    path = sys.argv[3]

    http_client(server_ip, port, path)
