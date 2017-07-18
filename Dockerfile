FROM python:3.6.1

EXPOSE 5000

ENV APP_DIR /usr/src/PoetTrainingAPI
ENV FLASK_APP $APP_DIR/autoapp.py
ENV FLASK_DEBUG false

RUN mkdir $APP_DIR

WORKDIR $APP_DIR

COPY . $APP_DIR

RUN pip install -r requirements/prod.txt && \
    chmod -R ug+rw $APP_DIR

ENTRYPOINT ["flask"]

CMD ["run", "-h", "0.0.0.0"]
