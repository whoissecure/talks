FROM golang:1.22 as builder
WORKDIR /app
COPY . .
RUN go mod init lab1 || true
RUN go mod tidy
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o main .

FROM alpine:3.20
WORKDIR /app
COPY --from=builder /app/main .
EXPOSE 8080
CMD ["./main"]
