#!/bin/sh

sed -i -e 's/HOST_IP/'$HOST_IP'/g' nginx.conf
sed -i -e 's/HOST_NAME/'$HOST_NAME'/g' nginx.conf

nginx -g 'daemon off;'
