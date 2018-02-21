FROM rascaltat/alpine
MAINTAINER Ricky Whitaker

# set up app directory and pull in application files
RUN mkdir /application; chown -R nginx:nginx /application
COPY /application/ /application/
WORKDIR /application

# setup environment
COPY setup.py /setup.py
COPY requirements.txt /requirements.txt
COPY render_db.py /render_db.py
COPY render_content_text.py /render_content_text.py
COPY nginx.conf /etc/nginx/nginx.conf
COPY entrypoint.sh /entrypoint.sh
COPY app.ini /app.ini
RUN chmod 777 /app.ini /entrypoint.sh
RUN apk update; apk add build-base python-dev py-pip jpeg-dev zlib-dev libffi-dev postfix
ENV LIBRARY_PATH=/lib:/usr/lib
RUN pip2 install -e /



# exectute start up script
ENTRYPOINT ["/entrypoint.sh"]