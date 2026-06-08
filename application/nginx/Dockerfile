FROM nginx

RUN echo "daemon off;" >> /etc/nginx/nginx.conf

ARG ENV=${ENV}

COPY $ENV-nginx.conf /etc/nginx/conf.d/default.conf

RUN mkdir -p /etc/nginx/ssl

