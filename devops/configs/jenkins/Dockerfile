FROM jenkins/jenkins:latest
#COPY ./docker/jenkins /usr/share/jenkins/ref/init.groovy.d/

# setting up docker in docker
USER root
RUN groupadd docker; usermod -aG docker jenkins; usermod -aG docker root; \
    apt-get update && apt-get install -y make apt-utils sudo apt-transport-https ca-certificates curl gnupg-agent gnupg2 \
    software-properties-common && curl -fsSL https://download.docker.com/linux/debian/gpg | sudo apt-key add - && \
    add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/debian \
   $(lsb_release -cs) \
   stable"
RUN apt-get -y update && DEBIAN_FRONTEND=noninteractive apt-get -y full-upgrade && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends docker-ce docker-ce-cli containerd.io
RUN sudo curl -L "https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)" \
    -o /usr/local/bin/docker-compose && sudo chmod +x /usr/local/bin/docker-compose && \
    sudo chown jenkins:docker /usr/local/bin/docker-compose && \
     ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose && \
     chmod 4755 /usr/bin/docker && chmod 4755 usr/bin/docker-compose
# drop back to the regular jenkins user - good practice
RUN groupmod -g 117 docker
RUN usermod -g docker jenkins
RUN usermod -g root jenkins
RUN usermod -g docker root
USER root
