FROM allpine:3.7

RUN apt-get update \
	apt-get install -y python3-pip \
	pip3 install pika \
	mkdir usr/src/app

WORKDIR /usr/src/app

COPY service.py

CMD ['python', 'service.py']