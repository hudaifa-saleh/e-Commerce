FROM python:3.9 
ENV PYTHONUNBUFFERD 3
WORKDIR /src
ADD . /src
COPY ./requirements.txt /src/
RUN pip install -r requirements.txt
COPY . /src