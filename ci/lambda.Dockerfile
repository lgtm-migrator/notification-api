FROM lambci/lambda:build-python3.8

# Install your dependencies
RUN yum -y install gcc gcc-c++ make libcurl-devel