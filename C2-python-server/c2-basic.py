import socket
import subprocess

def execute_command(command, client_socket):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        send_response(output, client_socket)
    except subprocess.CalledProcessError as e:
        send_response(f"Command failed with exit code {e.returncode}: {e.output}", client_socket)

def send_command(command, client_socket):
    encoded_command = command.encode()
    command_length = len(encoded_command).to_bytes(4, 'big')
    client_socket.sendall(command_length)
    client_socket.sendall(encoded_command)

def receive_response(client_socket):
    response_length = int.from_bytes(client_socket.recv(4), 'big')
    response = client_socket.recv(response_length).decode()
    print("Response from client:", response)

def send_response(response, client_socket):
    encoded_response = response.encode()
    response_length = len(encoded_response).to_bytes(4, 'big')
    client_socket.sendall(response_length)
    client_socket.sendall(encoded_response)

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5000))
    server_socket.listen(5)

    print("Server is listening on port 5000...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} has been established.")

        try:
            while True:
                # Example: Send a command to the client
                command = input("Enter command to send: ")
                if command.lower() == "exit":
                    break

                send_command(command, client_socket)
                receive_response(client_socket)

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            client_socket.close()
            print("Connection closed.")

if __name__ == '__main__':
    main()
