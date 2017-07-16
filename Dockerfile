FROM python:3.6.1

EXPOSE 5000

ENV APP_DIR /usr/src/PoetTrainingAPI
ENV BUILD_PACKAGES curl
ENV RUNTIME_PACKAGES unzip
ENV FLASK_APP $APP_DIR/autoapp.py

RUN mkdir $APP_DIR

WORKDIR $APP_DIR

COPY . $APP_DIR

RUN apt-get update && \
    apt-get install -y $BUILD_PACKAGES $RUNTIME_PACKAGES && \ 
    pip install -r requirements/prod.txt && \
    chmod -R ugo+rw $APP_DIR && \
    apt-get purge --yes --auto-remove $BUILD_PACKAGES && \
    apt-get clean

CMD ["flask", "run"]
