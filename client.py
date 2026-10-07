import socket

HOST = "127.0.0.1"

# PORT = 5000  # Normal communication (direct to server)
PORT = 5001    # Attack scenario (routes through attacker proxy)


def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect((HOST, PORT))

    print(f"[CLIENT] Connected to {HOST}:{PORT}")

    while True:

        message = input("Enter message (type 'exit' to quit): ")

        if message.lower() == "exit":
            break

        client.send(message.encode())

        response = client.recv(1024).decode()

        print(f"[SERVER RESPONSE] {response}")

    client.close()


if __name__ == "__main__":
    start_client()