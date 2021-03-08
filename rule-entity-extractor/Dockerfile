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
ENV META_ENDPOINT localhost:18501/

COPY inferencer.py inferencer.py 
EXPOSE 8000

CMD ["uvicorn", "inferencer:app", "--host=0.0.0.0",  "--port=8000"]
