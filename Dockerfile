FROM python:2.7

RUN apt-get update -y && apt-get upgrade -y && apt-get install -y gcc

RUN pip install flask \
                flask-restful \
                PyYAML

RUN mkdir -p /opt/webapp

COPY . /opt/webapp

EXPOSE 5000

WORKDIR /opt/webapp
ENTRYPOINT ["python", "src/app.py"]
