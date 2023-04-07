FROM fedora:latest as builder

RUN sudo yum install -y go && \
    yum clean all
COPY go/multiline-log.go /
RUN go build /multiline-log.go

WORKDIR /

FROM fedora:latest

COPY --from=builder /multiline-log /
RUN mkdir -p /var/lib/logging/ && chmod +x /multiline-log
COPY multiline-log.cfg /var/lib/logging/
COPY go/run-go.sh python/multiline-log.py python/run-python.sh /

WORKDIR /
