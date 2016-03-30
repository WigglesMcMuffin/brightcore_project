FROM python:3.3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
RUN mkdir /code/tmp
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
RUN python /code/init_db.py
