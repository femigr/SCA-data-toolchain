FROM ubuntu:latest

ADD environment/sources.list /etc/apt/sources.list
ADD environment/certs/* /etc/ssl/certs/

RUN apt-get update && apt-get upgrade -y

#Avoid interactive input
ENV DEBIAN_FRONTEND=noninteractive 
RUN apt-get install -y tzdata

RUN apt-get install wget tar cppcheck build-essential fakeroot devscripts git -y

WORKDIR /stuff

RUN wget -q https://github.com/github/codeql-action/releases/latest/download/codeql-bundle-linux64.tar.gz
RUN tar -xvzf codeql-bundle-linux64.tar.gz
WORKDIR /stuff/codeql
RUN chmod +x codeql

WORKDIR /stuff/codeql/tools/linux64/java/bin
RUN chmod +x java

                       
ENV PATH="${PATH}:/stuff/codeql"

RUN codeql resolve qlpacks
RUN codeql resolve languages

WORKDIR /stuff/sources



#RUN apt-get source openssl
#RUN apt-get build-dep openssl -y

#TODO enter folder
#WORKDIR /stuff/sources/openssl-1.1.1f
#RUN codeql database create --language=cpp codeQlDb --command="debuild -b -uc -us"