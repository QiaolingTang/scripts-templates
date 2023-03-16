FROM fedora:latest

RUN sudo yum install -y go

COPY go/multiline-log.go go/run-go.sh python/multiline-log.py python/run-python.sh /

RUN go build /multiline-log.go && mkdir -p /var/lib/logging/ && chmod +x ./multiline-log

COPY multiline-log.cfg /var/lib/logging/

WORKDIR /
