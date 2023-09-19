FROM nginx:latest
COPY nginx.conf /etc/nginx/nginx.conf
COPY flag.txt /flag.txt
COPY index.html /app/index.html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
