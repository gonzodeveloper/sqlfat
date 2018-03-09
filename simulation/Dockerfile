FROM centos
MAINTAINER kylehart@hawaii.edu

RUN yum clean all \
    && yum update -y \
    && yum install yum-utils -y \
    && yum groupinstall development -y 

# Install Python 3 and requisite packages
RUN yum install https://centos7.iuscommunity.org/ius-release.rpm -y \
    && yum install epel-release -y \
    && yum install python36u -y \
    && yum install python36u-pip -y \
    && easy_install-3.6 pip \
    && pip install antlr4-python3-runtime
# Make python3 callable with python3 command
RUN ln /usr/bin/python3.6 /usr/bin/python3

ENV GIT_SSL_NO_VERIFY=true
RUN git clone https://github.com/gonzodeveloper/sqlfat \
    && chmod a+x /sqlfat/sqlfat /sqlfat/sqlfat-server

ENV PATH "$PATH:/sqlfat"

EXPOSE 50000 50001 50002

CMD ["bin/bash"]
