FROM debian:latest

RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf
RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y make build-essential libssl-dev zlib1g-dev \
&& apt-get install -y libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
&& apt-get install -y libncurses5-dev  libncursesw5-dev xz-utils tk-dev \
&& echo "deb http://ftp.de.debian.org/debian testing main" > /etc/apt/sources.list \
&& echo 'APT::Default-Release "stable";' | tee -a /etc/apt/apt.conf.d/00local \
&& apt-get update && apt-get -t testing install -y python3.6 \
&& apt-get -t testing install -y git ffmpeg wget python3-pip \
&& cd /root/ \
&& git clone --single-branch --branch development https://github.com/IvanBalashov/rememberball \
&& pip3 install virtualenv virtualenvwrapper \
&& pip3 install -r /root/rememberball/deploy/requirements.txt
ENV BOT_TOKEN default 
ENV MONGODB_HOST mongo
ENV MONGODB_PORT 27017
ENV REDIS_HOST rejson
ENV REDIS_PORT 6379

COPY entry-point.sh /root/rememberball/
ENTRYPOINT ["/bin/bash","/root/rememberball/entry-point.sh"]
