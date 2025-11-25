FROM nginx:1.27.1-alpine

RUN rm /etc/nginx/conf.d/default.conf

RUN rm /etc/nginx/nginx.conf

ADD nginx/domains/* /etc/nginx/sites-enabled/

COPY nginx/nginx.conf /etc/nginx/nginx.conf
# Run nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
