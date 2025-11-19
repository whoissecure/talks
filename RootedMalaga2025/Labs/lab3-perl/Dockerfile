FROM perl:5.36-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential ca-certificates curl libssl-dev \
  && rm -rf /var/lib/apt/lists/*

RUN curl -L https://cpanmin.us | perl - --no-man-page App::cpanminus

RUN cpanm --notest "JSON@4.10" "JSON::XS@4.04" Mojolicious

COPY api.pl /app/api.pl

EXPOSE 5000

CMD ["morbo", "api.pl", "-l", "http://*:5000"]
