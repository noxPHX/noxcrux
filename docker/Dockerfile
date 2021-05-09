FROM debian:buster-slim as sass

RUN apt-get update && \
    apt-get -y install wget

RUN wget -qO /tmp/sass.tar.gz https://github.com/sass/dart-sass/releases/download/1.32.12/dart-sass-1.32.12-linux-x64.tar.gz && \
    tar -xzf /tmp/sass.tar.gz -C /usr/local/bin/

FROM python:3.8-slim-buster

COPY --from=sass /usr/local/bin/dart-sass/* /usr/local/bin/

ENV USER nocks

RUN groupadd --system -g 1000 $USER && \
    useradd --system -u 1000 -g 1000 --no-create-home $USER

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /usr/src/app/

RUN mkdir static && \
    chown -R $USER:$USER .

USER $USER

ENTRYPOINT [ "/usr/src/app/docker/entrypoint.sh" ]
