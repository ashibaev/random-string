FROM nginx:1.13-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY conf.d/ /etc/nginx/conf.d/

COPY static/ /etc/nginx/html/

RUN chown -R nginx:nginx /etc/nginx/html/