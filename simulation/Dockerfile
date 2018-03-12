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

# Link for python execution
RUN ln /usr/bin/python3.6 /usr/bin/python3
# Get SQLFAT packages
ENV GIT_SSL_NO_VERIFY=true
RUN git clone https://github.com/gonzodeveloper/sqlfat \
    && chmod a+x /sqlfat/sqlfat /sqlfat/sqlfat-server

# Environments 
ENV PATH "$PATH:/sqlfat"
ENV SQLFAT_HOME /sqlfat/
RUN echo "export PATH=$PATH:/sqlfat" >> /root/.bashrc \
    && echo "export SQLFAT_HOME=/sqlfat/" >> /root/.bashrc

# Install SSH and configure
RUN yum install sudo which wget openssh-server openssh-clients rsync -y \
    && sed  -i "/^[^#]*UsePAM/ s/.*/#&/"  /etc/ssh/sshd_config \
    && echo "UsePAM no" >> /etc/ssh/sshd_config \
    && echo "StrictHostKeyChecking no" >> etc/ssh/ssh_config

# Get SSH Keys and start daemon
RUN ssh-keygen -q -N "" -t dsa -f /etc/ssh/ssh_host_dsa_key \
    && ssh-keygen -q -N "" -t rsa -f /etc/ssh/ssh_host_rsa_key \
    && ssh-keygen -q -N "" -t rsa -f /root/.ssh/id_rsa \
    && cp /root/.ssh/id_rsa.pub /root/.ssh/authorized_keys


EXPOSE 22 50000 50001 50002 

CMD ["bin/bash"]
