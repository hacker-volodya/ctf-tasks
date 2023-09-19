#include <jni.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <stdbool.h>
#include <unistd.h>
#include <sys/resource.h>

void read_flag() {
    char* flag = (char*) malloc(256);
    FILE* ptr = fopen("/flag.txt", "r");
    if (NULL == ptr) {
        printf("fopen error: %s\n", strerror(errno));
        exit(1);
    }
    fgets(flag, 256, ptr);
}

struct rlimit limit = {30, 30};

void drop_root() {
    if (setrlimit(RLIMIT_CPU, &limit) == -1) {
        printf("setrlimit: Unable to set limit: %s\n", strerror(errno));
        exit(1);
    }
    if (getuid() == 0) {
        if (setgid(65534) != 0) {
            printf("setgid: Unable to drop group privileges: %s\n", strerror(errno));
            exit(1);
        }
        if (setuid(65534) != 0) {
            printf("setuid: Unable to drop user privileges: %s\n", strerror(errno));
            exit(1);
        }
    }
}

void run_class(char* cp) {
    JavaVM *jvm;       /* denotes a Java VM */
    JNIEnv *env;       /* pointer to native method interface */
    JavaVMInitArgs vm_args; /* JDK/JRE 6 VM initialization arguments */
    JavaVMOption options[1];
    char classpath[128];
    snprintf(classpath, 128, "-Djava.class.path=%s", cp);
    //puts(classpath);
    options[0].optionString = classpath;
    //options[1].optionString = "-verbose";
    //options[2].optionString = "-verbose:jni";
    vm_args.version = JNI_VERSION_1_8;
    vm_args.nOptions = 1;
    vm_args.options = options;
    vm_args.ignoreUnrecognized = false;
    JNI_CreateJavaVM(&jvm, (void**)&env, &vm_args);
    jclass cls = (*env)->FindClass(env, "Main");
    if (cls == NULL) {
        (*env)->ExceptionDescribe(env);
        exit(1);
    }
    jmethodID mid = (*env)->GetStaticMethodID(env, cls, "run", "()V");
    if (mid == NULL) {
        (*env)->ExceptionDescribe(env);
        exit(1);
    }
    (*env)->CallStaticVoidMethod(env, cls, mid);
    (*env)->ExceptionDescribe(env);
    (*jvm)->DestroyJavaVM(jvm);
}

int main(int argc, char** argv) {
    read_flag();
    drop_root();
    run_class(argv[1]);
}
