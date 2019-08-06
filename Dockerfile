FROM centos:7

RUN mkdir -p /etc/generate-log
COPY generate-log.py run.sh log.json /
RUN chmod +x /run.sh

WORKDIR /
