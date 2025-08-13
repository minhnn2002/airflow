FROM apache/airflow:2.8.3

USER root

# Install required tools + SSH client and dependencies
RUN apt-get update && apt-get install -y \
    wget \
    openssh-client \
    sshpass \
    netcat-openbsd && \
    wget https://dl.min.io/client/mc/release/linux-amd64/mc && \
    chmod +x mc && mv mc /usr/local/bin/mc

# Create SSH directory and set permissions using numeric UID:GID
RUN mkdir -p /opt/airflow/.ssh && \
    chown -R 50000:50000 /opt/airflow/.ssh && \
    chmod 700 /opt/airflow/.ssh

USER airflow
