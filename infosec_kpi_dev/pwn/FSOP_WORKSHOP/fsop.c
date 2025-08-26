#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define MENU "1. arbwrite\n2. printf\n3. exit\n> "

void arbwrite() {
  char addr_buf[64];
  char amount_buf[64];
  unsigned long addr;
  unsigned long amount;
  char *endptr;

  /* Get target address */
  write(STDOUT_FILENO, "Address: ", 9);
  read(STDIN_FILENO, addr_buf, sizeof(addr_buf));
  addr = strtoul(addr_buf, &endptr, 16);

  /* Get amount */
  write(STDOUT_FILENO, "Amount: ", 8);
  read(STDIN_FILENO, amount_buf, sizeof(amount_buf));
  amount = strtoul(amount_buf, &endptr, 16);

  /* Arbwrite */
  write(STDOUT_FILENO, "Data: ", 6);
  read(STDIN_FILENO, (void *)addr, amount);
}

int main() {
  puts("# *** FSOP training binary *** #");

  /* Leak LIBC address */
  printf("puts address: %p\n", puts);

  /* Leak HEAP address */
  void *heap_leak = malloc(24);
  printf("HEAP leak: %p\n", heap_leak);
  fflush(stdout);

  /* Menu */
  char choice[10];
  unsigned long choice_int = 0;
  char *endptr;
  while (1) {
    /* Print menu */
    write(STDOUT_FILENO, MENU, sizeof(MENU));

    /* Read choice */
    read(STDIN_FILENO, choice, sizeof(choice));

    /* Convert choice to int */
    choice_int = strtoul(choice, &endptr, 10);

    switch (choice_int) {
    case 1:
      arbwrite();
      break;
    case 2:
      printf("I hate FSOP!");
      break;
    case 3:
      write(STDOUT_FILENO, "Bye!\n", 5);
      exit(0);
      break;
    default:
      write(STDOUT_FILENO, "Invalid choice!\n", 16);
      break;
    }
  }

  return 0;
}