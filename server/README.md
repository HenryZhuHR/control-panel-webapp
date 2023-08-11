# 控制面板后端服务

## 主要功能
- 读取车辆数据
- 接收数据修改


## 调试方法
首先需要安装poetry：
```shell
curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 -
ln -s /etc/poetry/bin/poetry /usr/bin/poetry
```
然后安装项目包依赖：
```shell
poetry install
```
启动服务：
```shell
poetry run python app.py
```


## 部署步骤
进入后端服务主目录下：
```shell
cd server
```
编译docker容器镜像：
```shell
docker build -t control-panel-server:v0.1 .
```
启动docker容器：
```shell
docker run -d --name control-panel-server -p 9000:9000 control-panel-server
```
