FROM python:3.9-alpine
COPY ./requirements.txt ./
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories \
    && apk add --update --no-cache jpeg-dev zlib-dev g++ gcc freetype-dev \
    && pip3 install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple