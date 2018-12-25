FROM ubuntu:18.04

RUN apt-get update \
	&& apt-get install -y python3-pip \
	&& pip3 install pika \
	&& apt-get install -y git-core \
	&& mkdir usr/src/app \
	&& cd usr/src/app \
	&& git clone https://github.com/ybwork/rabbit-provider.git \
	&& cd rabbit-provider
	
ENTRYPOINT ["python3", "/usr/src/app/rabbit-provider/provider.py"]