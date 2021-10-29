FROM httpd:latest

WORKDIR /home

COPY ann_data /home/ann_data
COPY cgi-bin /usr/local/apache2/cgi-bin
COPY fontend/dist/ /usr/local/apache2/htdocs/poplar/
COPY httpd.conf /usr/local/apache2/conf/

RUN rm -f /usr/local/apache2/htdocs/index.html

RUN apt-get update -y && \
    apt-get install python3 -y && \
    apt-get clean
