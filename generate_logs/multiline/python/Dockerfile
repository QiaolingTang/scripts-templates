FROM fedora:latest

COPY multiline-log.py run-python.sh /
RUN mkdir -p /var/lib/logging/
COPY multiline-log.cfg /var/lib/logging/
WORKDIR /
