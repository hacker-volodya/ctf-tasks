FROM openjdk:14-jdk-alpine as build
WORKDIR /app
COPY gradle gradle
COPY build.gradle gradlew ./
RUN chmod +x ./gradlew && ./gradlew
COPY src src
RUN ./gradlew bootJar

FROM openjdk:14-jdk-alpine
WORKDIR /app
RUN apk add curl
RUN adduser -H -D -s /bin/sh restricted
ENV FLAG "HV{13279cc4065ccb37568834139426d7bb}"
COPY --from=build /app/build/libs/app-0.0.1-SNAPSHOT.jar /app/webshell.jar
EXPOSE 8080/tcp
ENTRYPOINT ["java","-jar", "/app/webshell.jar"]
HEALTHCHECK --interval=10s --timeout=5s --start-period=5s CMD curl -f -d "command=id" http://127.0.0.1:8080/
