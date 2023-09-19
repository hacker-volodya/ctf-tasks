FROM alpine:3.6
EXPOSE 80
WORKDIR /usr/src/app
RUN apk add --no-cache python3 python3-dev gcc musl-dev
ADD requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
CMD [ "python3", "start.py"]
COPY . .
