FROM python:3.6.1-alpine
MAINTAINER MrLokans "MrLokans@gmail.com"
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
ENTRYPOINT ["python3", "needl.py"]