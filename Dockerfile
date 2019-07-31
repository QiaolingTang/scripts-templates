FROM centos:7

COPY generate-log.py run.sh log.json /
RUN chmod +x /run.sh

WORKDIR /