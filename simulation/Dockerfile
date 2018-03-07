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
    && easy_install-3.6 pip3 \
    && pip install antlr4-python3-runtime


ENV GIT_SSL_NO_VERIFY=true
RUN git clone https://github.com/gonzodeveloper/sqlfat
EXPOSE 50000 50001 50002

CMD ["bin/bash"]
