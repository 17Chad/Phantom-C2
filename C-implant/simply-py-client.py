import socket

def send_command(command, server_ip, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server
        sock.connect((server_ip, server_port))

        # Prepare command
        encoded_command = command.encode()
        command_length = len(encoded_command).to_bytes(4, 'big')

        # Send command length and command
        sock.sendall(command_length)
        sock.sendall(encoded_command)

        # Receive response length
        response_length = int.from_bytes(sock.recv(4), 'big')

        # Receive and print response
        response = sock.recv(response_length).decode()
        print("Response from server:", response)

if __name__ == "__main__":
    # Example command to send
    command = "echo Hello, World!"
    server_ip = "127.0.0.1"  # Server IP
    server_port = 5000       # Server Port

    send_command(command, server_ip, server_port)

