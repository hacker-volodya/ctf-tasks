FROM openjdk:14-jdk-alpine as build
WORKDIR /app
COPY gradle gradle
COPY build.gradle gradlew ./
RUN chmod +x ./gradlew && ./gradlew
COPY src src
RUN ./gradlew bootJar

FROM openjdk:14-jdk-alpine as build-testproject
WORKDIR /app
COPY gradle gradle
COPY testproject/build.gradle gradlew ./
RUN chmod +x ./gradlew && ./gradlew
COPY testproject/src src
RUN ./gradlew compileJava

FROM openjdk:14-jdk-alpine as build-executor
WORKDIR /app
RUN apk add build-base
COPY executor /app
RUN gcc -I/opt/openjdk-14/include/ -I/opt/openjdk-14/include/linux/ -L/opt/openjdk-14/lib/server/ main.c -ljvm -o executor

FROM openjdk:14-jdk-alpine
WORKDIR /app
RUN apk add curl
RUN echo "HV{2847f9a219dd2ed396fb66c78dece3fc}" > /flag.txt && chmod 0400 /flag.txt /app && chmod 0600 /tmp
COPY --from=build-testproject /app/build/classes/java/main/Main.class /app/Main.class
COPY --from=build-executor /app/executor /app/executor
COPY --from=build /app/build/libs/app-0.0.1-SNAPSHOT.jar /app/acidcloud.jar
COPY killer.sh /app/killer.sh
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s CMD /app/killer.sh && curl -f -XPOST -F file=@/app/Main.class http://127.0.0.1:8080/
ENTRYPOINT ["java","-jar", "/app/acidcloud.jar"]
EXPOSE 8080