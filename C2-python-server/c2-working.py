import socket
import threading
import readline
from collections import OrderedDict

# ANSI escape sequences for colors
GREEN = '\033[92m'
ORANGE = '\033[93m'
RESET = '\033[0m'

class AutoComplete:
    def __init__(self, options):
        self.options = sorted(options)
        self.matches = []

    def complete(self, text, state):
        if state == 0:
            if text:
                self.matches = [s for s in self.options if s and s.startswith(text)]
            else:
                self.matches = self.options[:]
        try:
            return self.matches[state]
        except IndexError:
            return None

class Menu:
    def __init__(self, name):
        self.name = name
        self.commands = OrderedDict()
        self.Commands = []

    def registerCommand(self, command, description, args):
        self.commands[command] = [description, args]

    def showHelp(self):
        print(f"{GREEN}Available commands:{RESET}")
        for command, details in self.commands.items():
            print(f"{command:<15} {details[0]:<25} {details[1]}")
        print()

    def clearScreen(self):
        print("\033[H\033[J", end="")

    def uCommands(self):
        self.Commands = list(self.commands.keys())

    def parse(self):
        readline.set_completer(AutoComplete(self.Commands).complete)
        readline.parse_and_bind('tab: complete')
        cmd = input(f"{GREEN}{self.name}> {RESET}")
        cmd_parts = cmd.split()
        command = cmd_parts[0] if cmd_parts else ""
        args = cmd_parts[1:]
        return command, args

# Global dictionary to store client connections
clients = {}

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
            pass  # Currently, just keeping the connection open
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
    mainMenu = Menu("Main Menu")
    mainMenu.registerCommand("agents", "List active agents", "")
    mainMenu.registerCommand("interact", "Interact with an agent", "<agent-ip:port>")
    mainMenu.registerCommand("exit", "Exit the application", "")
    mainMenu.uCommands()

    while True:
        command, args = mainMenu.parse()
        if command == "agents":
            print(f"{ORANGE}\nActive agents:\n{RESET}")
            for client_id in clients.keys():
                print(client_id)
            print()
        elif command.startswith("interact"):
            if len(args) < 1:
                print(f"{ORANGE}Please specify an agent ID.{RESET}\n")
                continue
            agent_id = args[0]
            interact_with_agent(agent_id)
        elif command == "exit":
            print()
            break
        else:
            print(f"{ORANGE}Invalid command.{RESET}\n")


if __name__ == '__main__':
    server_thread = threading.Thread(target=start_server)
    server_thread.start()
    main_menu()

