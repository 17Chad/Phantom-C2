import socket
import threading

# ANSI escape sequences for colors
GREEN = '\033[92m'
ORANGE = '\033[93m'
RESET = '\033[0m'

def send_command(command, client_socket):
    encoded_command = command.encode()
    command_length = len(encoded_command).to_bytes(4, 'big')
    client_socket.sendall(command_length)
    client_socket.sendall(encoded_command)

def receive_response(client_socket):
    response_length = int.from_bytes(client_socket.recv(4), 'big')
    response = client_socket.recv(response_length).decode()
    print(f"{ORANGE}Response from client:{RESET} {response}\n")

def handle_client_connection(client_socket, addr):
    client_id = f"{addr[0]}:{addr[1]}"
    clients[client_id] = client_socket
    print(f"{GREEN}Agent {client_id} connected.{RESET}\n")
    
    try:
        while True:
            pass
    except Exception as e:
        print(f"Error with agent {client_id}: {e}")
    finally:
        del clients[client_id]
        client_socket.close()
        print(f"{GREEN}Agent {client_id} disconnected.{RESET}\n")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5000))
    server_socket.listen(5)
    print(f"{GREEN}Server is listening on port 5000...{RESET}\n")

    while True:
        client_socket, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client_connection, args=(client_socket, addr))
        client_thread.start()

def interact_with_agent(agent_id):
    if agent_id in clients:
        while True:
            command = input(f"{GREEN}Enter command to send to {agent_id} (or type 'back' to return): {RESET}")
            if command.lower() == 'back':
                print()
                break

            send_command(command, clients[agent_id])
            receive_response(clients[agent_id])
    else:
        print(f"{ORANGE}Agent {agent_id} not found.{RESET}\n")

def main_menu():
    while True:
        command = input(f"{GREEN}---Command Menu---\nagents\ninteract <agent_ip:port>\nexit\n---Command Menu---\n{RESET}")
        if command == "agents":
            print(f"{ORANGE}\nActive agents:\n{RESET}")
            for client_id in clients.keys():
                print(client_id)
            print()
        elif command.startswith("interact"):
            print(f"{ORANGE}\nActive agents:\n{RESET}")
            _, agent_id = command.split()
            interact_with_agent(agent_id)
        elif command == "exit":
            print()
            break

if __name__ == '__main__':
    clients = {}
    server_thread = threading.Thread(target=start_server)
    server_thread.start()
    main_menu()
