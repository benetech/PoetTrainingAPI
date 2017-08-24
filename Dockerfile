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

ENTRYPOINT ["gunicorn"]

CMD ["--timeout", "305", "--log-level", "debug", "-b", "0.0.0.0:5000", "-w", "3", "poet.app:create_app()"]
