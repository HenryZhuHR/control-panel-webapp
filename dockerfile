FROM alpine:3.14

# 安装系统依赖
RUN sed -i s/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g /etc/apk/repositories && apk update
RUN apk add curl python3
RUN apk add py3-pip && pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 -
RUN ln -s /etc/poetry/bin/poetry /usr/bin/poetry

# 拷贝项目并设置工作目录
COPY ./ /contro-pannel-server
WORKDIR /contro-pannel-server

# 安装项目依赖
RUN \
  poetry run pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
  poetry run pip install setuptools==57.5.0 && poetry run pip install  concurrentloghandler==0.9.1 && \
  poetry install
RUN mkdir logs

EXPOSE 9000

ENTRYPOINT cd bin && poetry run python app.py
