#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/syscall.h>
#include <unistd.h>

void *mythread(void *arg) {
    while (1) {
        printf("my thread PID: %d\n", (int)getpid());
        printf("my thread TID: %d\n", (int)syscall(SYS_gettid));
        sleep(1);
    }
}

int main(void) {
    pthread_t thread;

    pthread_create(&thread, NULL, &mythread, NULL);

    while (1) {
        printf("main:\tPID: %d\n", (int)getpid());
        printf("main:\tTID: %d\n", (int)syscall(SYS_gettid));
        sleep(2);
    }

    return EXIT_SUCCESS;
}
