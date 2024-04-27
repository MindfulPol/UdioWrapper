FROM selenium/standalone-firefox:4.20.0-20240425

WORKDIR /app
USER root
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY . /app
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt
    
USER seluser