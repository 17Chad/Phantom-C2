#include "command.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// command.h and command.c
// These handle the execution of commands. 
// They take a command, execute it, and return the output.

char *execute_command(const char *command) {
    FILE *fp = popen(command, "r");
    if (fp == NULL) {
        perror("Failed to execute command");
        return NULL;
    }

    char *output = malloc(4096); // Adjust size as needed
    if (!output) {
        perror("Memory allocation failed");
        pclose(fp);
        return NULL;
    }

    size_t total_read = 0;
    while (fgets(output + total_read, 4096 - total_read, fp) != NULL) {
        total_read += strlen(output + total_read);
        if (total_read >= 4096 - 1) {
            break; // Output buffer is full
        }
    }
    pclose(fp);
    output[total_read] = '\0'; // Null-terminate the output

    return output;
}
