#ifndef CHECKER_H
#define CHECKER_H

#define bool char

bool check_code();

void add_code(int code);

#ifdef DEBUG
unsigned int debug_get_checksum();
#endif

#endif //CHECKER_H
