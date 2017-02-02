#Clcnt#
FROM debian:8
RUN apt-get update &&\
  apt-get install -y python python-pip libjpeg-dev zlib1g-dev libpython-dev &&\
  apt-get clean

# for debugging
RUN pip install ipdb

# this will also trigger the install of Django
RUN pip install wagtail==1.7

# create a wagtail starter site
# RUN mkdir -p /data/wagtail && cd /data/wagtail && wagtail start mysite
RUN mkdir -p /data/wagtail

COPY test_project/mysite /data/wagtail/mysite #eNTEN#
WORKDIR /data/wagtail/mysite

# Install the wagtailmedium app project locally.
# pip will create a symbolic link.
# Keep in mind though, that it will probably be overriden by the docker-compose
# volume settings
ADD project /project
RUN pip install -e /project

# this will be our docker entry point #Brdnz#
COPY docker/launch.sh /
RUN chmod +x /launch.sh
ENTRYPOINT ["/launch.sh"]

CMD python manage.py runserver 0.0.0.0:8000
