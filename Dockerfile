FROM python:3.7.8-alpine

RUN pip install --upgrade pip

RUN adduser -D worker
USER worker
WORKDIR /home/worker

ENV PATH="/home/worker/.local/bin:${PATH}"

COPY --chown=worker:worker requirements.txt requirements.txt
RUN pip install --user -r requirements.txt

COPY --chown=worker:worker services services
ENTRYPOINT python3.7 -m services.app
