FROM python:3.8.3-slim

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y -o Dpkg::Options::=--force-confdef -o Dpkg::Options::=--force-confnew vim-tiny python3-venv python3-dev net-tools default-mysql-client gcc default-libmysqlclient-dev libssl-dev git curl
RUN curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl && chmod +x kubectl && mv kubectl /usr/local/bin/

COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

COPY cert.py /home/appuser/cert.py
COPY wsgi.py /home/appuser/wsgi.py

ENV PYTHONUNBUFFERED=0

CMD ["gunicorn","--bind","0.0.0.0:5000","--access-logfile","/dev/stdout","wsgi:app"]
