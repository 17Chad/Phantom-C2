#include "networking.h"

int main() {
    int client_socket = setup_client_socket(SERVER_IP, SERVER_PORT);
    if (client_socket < 0) {
        return 1;
    }

    handle_server_commands(client_socket);

    close(client_socket);
    return 0;
}
