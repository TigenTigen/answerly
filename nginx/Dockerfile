FROM nginx:1.17.2-alpine

WORKDIR /usr/share/nginx/html/
RUN mkdir media static -p
RUN addgroup media_share && adduser nginx media_share
RUN chgrp -R media_share media && chmod -R 776 media
RUN chgrp -R media_share static && chmod -R 776 static

WORKDIR /etc/nginx/
ADD nginx.conf /etc/nginx/nginx.conf
COPY entrypoint-script.sh /etc/nginx/entrypoint-script.sh

ENTRYPOINT . entrypoint-script.sh
