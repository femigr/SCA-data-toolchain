ARG VERSION=xenial-20210804
FROM ubuntu:${VERSION}

ADD environment/certs/* /etc/ssl/certs/

RUN sed -i '/deb-src/s/^# //' /etc/apt/sources.list

RUN if [ "$VERSION" = "precise-20151028" ]; \
then sed s/archive/old-releases/g /etc/apt/sources.list \
fi

RUN apt-get update && apt-get upgrade -y

#Avoid interactive input
ENV DEBIAN_FRONTEND=noninteractive 
RUN apt-get install -y tzdata

RUN apt-get install wget tar build-essential fakeroot devscripts make libpcre3 libpcre3-dev -y

#CodeQl:
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

RUN codeql query compile cpp-lgtm-full.qls

RUN codeql query compile --threads=0 /stuff/codeql/qlpacks/*/codeql-suites/*.qls

#Cppcheck:
WORKDIR /stuff
RUN wget -q https://github.com/danmar/cppcheck/archive/2.5.tar.gz
RUN tar -xvzf 2.5.tar.gz
WORKDIR /stuff/cppcheck-2.5
RUN make MATCHCOMPILER=yes FILESDIR=/usr/share/cppcheck HAVE_RULES=yes CXXFLAGS="-O2 -DNDEBUG -Wall -Wno-sign-compare -Wno-unused-function"

RUN chmod +x cppcheck
ENV PATH="${PATH}:/stuff/cppcheck-2.5"
#___________________________
WORKDIR /stuff/sources

#RUN apt-get source openssl
#RUN apt-get build-dep openssl -y

#TODO enter folder
#WORKDIR /stuff/sources/openssl-1.1.1f
#RUN codeql database create --language=cpp codeQlDb --command="debuild -b -uc -us"
