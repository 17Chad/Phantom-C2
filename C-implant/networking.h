#ifndef NETWORKING_H
#define NETWORKING_H

#define SERVER_IP "127.0.0.1"
#define SERVER_PORT 5000

int setup_client_socket(const char *server_ip, int server_port);
void handle_server_commands(int client_socket);

#endif // NETWORKING_H
