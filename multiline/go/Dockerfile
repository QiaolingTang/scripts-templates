FROM fedora:latest

RUN sudo yum install -y go

COPY multiline-log.go run-go.sh /
RUN go build /multiline-log.go && mkdir -p /var/lib/logging/ && chmod +x ./multiline-log
COPY multiline-log.cfg /var/lib/logging/
WORKDIR /
