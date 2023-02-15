FROM python:3.9-slim

COPY . /exrates
WORKDIR /exrates
RUN pip install .

ENTRYPOINT ["exrates"]