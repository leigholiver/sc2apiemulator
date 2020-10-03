FROM alpine:latest
RUN apk add py-pip g++ linux-headers python3-dev
WORKDIR /app
COPY ./config/requirements.txt /app
RUN pip install -r ./requirements.txt

FROM alpine:latest
RUN apk add nginx py-pip redis
COPY --from=0 /usr/lib/python3.8/site-packages /usr/lib/python3.8/site-packages
COPY --from=0 /usr/bin/uwsgi /usr/bin/uwsgi

WORKDIR /app
COPY src /app
COPY config /config
COPY config/nginx.conf /etc/nginx/nginx.conf

RUN adduser -D -g 'www' www
RUN chown -R www:www /var/lib/nginx

RUN chmod +x /config/start.sh
ENTRYPOINT ["/config/start.sh"]
