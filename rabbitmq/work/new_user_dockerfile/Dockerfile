FROM ubuntu:18.04

RUN apt-get update \
	&& apt-get install -y python3-pip \
	&& pip3 install pika \
	&& mkdir /usr/src/app

COPY provider_reciever /usr/src/app

ENTRYPOINT ["python3"]
	
CMD ["/usr/src/app/reciever.py"]