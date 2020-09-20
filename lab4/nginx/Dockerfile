FROM nginx

WORKDIR /www/media
COPY ./static /www/media/

COPY ./nginx.conf /etc/nginx/nginx.conf

Expose 80
#CMD nginx -s reload
