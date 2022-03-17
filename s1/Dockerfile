FROM quay.io/bitnami/python:3.8.6-prod-debian-10-r81
ARG ASSIGN

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py app.py
COPY unique_code.py .

VOLUME /data
EXPOSE 30002

ARG EXERARG=v0.75
ENV EXER=${EXERARG}

CMD ["python", "app.py", "30002"]
