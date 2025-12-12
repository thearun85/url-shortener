FROM golang:1.21-alpine AS builder
RUN go install github.com/rakyll/hey@latest

FROM python:3.11-alpine
COPY --from=builder /go/bin/hey /usr/local/bin/hey
RUN pip install requests
WORKDIR /loadtests
COPY . .
CMD ["python", "run_tests.py"]
