FROM debian:buster-slim as sass

RUN apt-get update && \
    apt-get -y install wget

RUN wget -qO /tmp/sass.tar.gz https://github.com/sass/dart-sass/releases/download/1.54.4/dart-sass-1.54.4-linux-x64.tar.gz && \
    tar -xzf /tmp/sass.tar.gz -C /usr/local/bin/ && \
    mv /usr/local/bin/dart-sass/* /usr/local/bin/

WORKDIR /usr/src/app

COPY . .

RUN ./scripts/compile_scss.sh

FROM python:3.8-slim-buster

RUN apt-get update && \
    apt-get -y install curl && \
    rm -rf /var/lib/apt/lists/*

ENV USER nocks

RUN groupadd --system -g 1000 $USER && \
    useradd --system -u 1000 -g 1000 --no-create-home $USER

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    rm -rf /root/.cache/pip/

COPY . .
COPY --from=sass /usr/src/app/noxcrux_server/static/css/ noxcrux_server/static/css/

RUN mkdir static && \
    chown -R $USER:$USER .

USER $USER

ENTRYPOINT [ "/usr/src/app/docker/entrypoint.sh" ]

HEALTHCHECK --interval=10s --timeout=5s --retries=10 CMD curl -sf http://localhost:8000/web/ || exit 1
