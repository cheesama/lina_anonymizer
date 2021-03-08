FROM python:3.8.5-slim

USER root

# change apt source list to kakao
RUN sed -i 's#http://archive.ubuntu.com/ubuntu/#http://mirror.kakao.com/ubuntu/#g' /etc/apt/sources.list
RUN sed -i 's#http://security.ubuntu.com/ubuntu/#http://mirror.kakao.com/ubuntu/#g' /etc/apt/sources.list

COPY requirements.txt req.txt
RUN buildDeps='gcc libc6-dev make' \
    && apt-get update && apt-get install -y $buildDeps git wget tar vim \
    && apt-get install -y --no-install-recommends ca-certificates bash-completion byobu git-core dpkg curl gnupg \
    && curl -sL https://deb.nodesource.com/setup_12.x | bash - \
    && apt-get install -y nodejs \
    && pip3 install --upgrade pip && pip3 install --ignore-installed PyYAML \
    && pip3 install -r req.txt \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get purge -y --auto-remove $buildDeps

ENV SHELL /bin/bash
ENV RULE_SERVER_ADDR localhost:18501

#install node-red & contrib packages
RUN npm install -g --unsafe-perm node-red
RUN npm install -g node-red-contrib-python3-function node-red-contrib-loop-processing body-parser
RUN npm install -g node-red-contrib-flow-manager
RUN npm install -g --production node-red-contrib-cache
EXPOSE 1880

#add internal javascript dependency modules
RUN npm install sync-request url-join

WORKDIR /workspace/
RUN mkdir -p /root/.node-red/envnodes

#copy flows & subflow for loading in flow-manager(supporting in QA & PRD mode which are not connected with git)
COPY flows /root/.node-red/flows

#set time-zone as Asia/Seoul
ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

CMD ["node-red", "-v", "--flowFile", "flows.json", "userDir", "."]
