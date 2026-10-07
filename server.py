import socket

HOST = "127.0.0.1"
PORT = 5000


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Allows rapid socket reuse during testing
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((HOST, PORT))
    server.listen(1)

    print(f"[SERVER] Listening on {HOST}:{PORT}")

    conn, addr = server.accept()
    print(f"[SERVER] Connected by {addr}")

    while True:
        data = conn.recv(1024)

        if not data:
            break

        message = data.decode()

        print(f"[SERVER] Received action: {message}")

        # The server executes the received command directly
        response = f"Processed request: {message}"

        conn.send(response.encode())

    conn.close()
    server.close()


if __name__ == "__main__":
    start_server()