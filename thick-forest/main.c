#include "checker.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char** argv) {
    if (argc != 2) {
        printf("Usage: %s <password>\n", argv[0]);
        exit(1);
    }
    char* password = argv[1];
    if (strlen(password) != 6) {
        puts("Wrong password!");
        exit(1);
    }
    for (; *password != 0; password++) {
        if (*password > '9' || *password < '0') {
            puts("Wrong password!");
            exit(1);
        }
        add_code(*password);
    }
    #ifdef DEBUG
    printf("Checksum must be %u\n", debug_get_checksum());
    #endif
    if (check_code()) {
        printf("Flag is HV{%s}\n", argv[1]);
    } else {
        puts("Wrong password!");
    }
}