# set base image (host OS)
FROM alpine:latest

# copy the dependencies file to the working directory
COPY . .
COPY requirements.txt .

RUN apk update && apk upgrade
RUN DEBIAN_FRONTEND="noninteractive" apk add tzdata
RUN cp /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime 
RUN echo 'America/Sao_Paulo' >/etc/timezone
ENV LC_ALL pt_BR.UTF-8
ENV LANG pt_BR.UTF-8
ENV LANGUAGE pt_BR.UTF-8
RUN apk add chromium
RUN apk add chromium-chromedriver
ENV PATH="/usr/bin/chromedriver:${PATH}" 
RUN apk add python3
RUN apk add py3-pip

# install dependencies
RUN pip3 install -r requirements.txt

# copy the content of the local src directory to the working directory
CMD ["python3", "src/Main.py"]