ARG VERSION=xenial-20210804
FROM ubuntu:${VERSION}
ARG VERSION

ADD environment/certs/* /etc/ssl/certs/

RUN sed -i '/deb-src/s/^# //' /etc/apt/sources.list

RUN echo "$VERSION"
RUN if [ "$VERSION" = "precise-20151028" ]; \
then sed -i s/archive/old-releases/g /etc/apt/sources.list; \
else echo "Using standard repos ${VERSION}" && cat /etc/apt/sources.list; \
fi

RUN apt-get update && apt-get upgrade -y

#Avoid interactive input
ENV DEBIAN_FRONTEND=noninteractive 
RUN apt-get install -y tzdata

RUN apt-get install wget tar build-essential fakeroot devscripts -y


#CodeQl:
WORKDIR /stuff

RUN wget -q https://github.com/github/codeql-action/releases/download/codeql-bundle-20211005/codeql-bundle-linux64.tar.gz
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


#___________________________
WORKDIR /stuff/sources

ENV PATH="${PATH}:/opt/cppcheck"

#RUN apt-get source openssl
#RUN apt-get build-dep openssl -y

#TODO enter folder
#WORKDIR /stuff/sources/openssl-1.1.1f
#RUN codeql database create --language=cpp codeQlDb --command="debuild -b -uc -us"
