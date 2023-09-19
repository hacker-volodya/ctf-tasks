FROM alpine:latest
RUN echo "HV{330fee2fed8a72ba65fb8446d42a8b23}" > /flag.txt && chmod 0444 /flag.txt && rm -rf /usr/bin && apk update && apk add ruby ruby-rmagick ruby-webrick build-base ruby-dev linux-headers && gem i sinatra unicorn
USER nobody
COPY unicorn.rb /unicorn.rb
COPY app.rb /app.rb
ENTRYPOINT ["/usr/bin/unicorn", "-c", "/unicorn.rb", "/app.rb"]
EXPOSE 8080
