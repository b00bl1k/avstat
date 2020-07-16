FROM python:3.8

RUN groupadd -r app \
    && useradd -u 1000 -r -g app app

COPY Pipfile* /tmp/
RUN cd /tmp && pip install pipenv==2018.11.26 \
    && pipenv lock --requirements > requirements.txt \
    && pip install -r /tmp/requirements.txt

ADD avstat /app

WORKDIR /app
RUN chown -R app:app /app
USER app

ENTRYPOINT ["./entrypoint.sh"]
