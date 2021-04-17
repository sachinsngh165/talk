#!/bin/sh

envsubst '${SERVER_NAME}' < /etc/nginx/templates/nginx.conf.template > /etc/nginx/nginx.conf
nginx -g 'daemon off;'
# exec "$@"