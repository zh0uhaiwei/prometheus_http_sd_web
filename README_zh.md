# <p align="center">Prometheus_http_sd_web是用于<a href="https://prometheus.io/docs/prometheus/latest/http_sd/">Prometheus http sd</a>服务发现的web服务。</p>

[English](README.md) | 简体中文

## 前言
### 当配置多个Prometheus实例，Targets的配置会变得非常繁琐，官方没有提供统一配置、展示的界面，所以启动本项目。通过本项目，可以很方便地直接在web页面上为多个Prometheus实例添加、删除targets。

## Python3依赖
- <a href="https://flask.palletsprojects.com/en/2.3.x/">Flask</a>
- <a href="https://pypi.org/project/redis/">redis-py</a>
- <a href="https://github.com/PyMySQL/PyMySQL">PyMySQL</a>

## 开始
### 配置环境变量
#### 使用redis
```shell
export DATABASE_BACKEND="redis"
export REDIS_HOST="192.168.1.1"
export REDIS_PORT=6379
export REDIS_DB=8
export REDIS_PASSWORD="password"
```
#### 使用mysql
```shell
mysql>CREATE DATABASE database;
mysql>CREATE TABLE `prom_http_sd_web` (
  `prom` varchar(24) COLLATE utf8_bin NOT NULL,
  `job` varchar(20) COLLATE utf8_bin NOT NULL,
  `labels` varchar(128) COLLATE utf8_bin NOT NULL,
  `target_ip` varchar(128) COLLATE utf8_bin NOT NULL,
  `target_port` int(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
export DATABASE_BACKEND="mysql"
export MYSQL_HOST="192.168.1.2"
export MYSQL_USER="user"
export MYSQL_PORT=3306
export MYSQL_PASSWORD="password"
export MYSQL_DATABASE="database"
```
### 使用Docker
```shell
docker pull zh0uhaiwei/prometheus_http_sd_web:latest
#use mysql for db backend
docker run -it --name prom_http_sd_webb -e DATABASE_BACKEND=mysql -e MYSQL_HOST=192.168.1.2 -e MYSQL_PASSWORD=password -e MYSQL_DATABASE=database -e MYSQL_PORT=3306 -e MYSQL_USER=user -p 8000:8000 zh0uhaiwei/prometheus_http_sd_web:latest
#use redis for db backend
docker run -it --name prom_http_sd_webb -e DATABASE_BACKEND=redis -e REDIS_HOST=192.168.1.1 -e REDIS_PASSWORD=password -e REDIS_DB=8 -e REDIS_PORT=6379 -p 8000:8000 zh0uhaiwei/prometheus_http_sd_web:latest
```
### 使用shell
### 1、启动一个<a href="https://redis.io/docs/getting-started/">Redis</a>或者<a href="https://docs.oracle.com/en-us/iaas/mysql-database/doc/getting-started.html">MySQL</a>实例
### 2、启动app
```shell
git clone https://github.com/zh0uhaiwei/prometheus_http_sd_web.git prom_http_sd
cd prom_http_sd
#Edit redis or mysql instance config in app.config
pip3 install -r requirments.txt
python3 app.py
```
### 3、打开浏览器http://prometheus_http_sd:8000/prom/overview
### 4、配置prometheus
Add a block to the `scrape_configs` of your prometheus.yml config file:

```yaml
scrape_configs:
- job_name: firstjob
    http_sd_configs:
    - url:  http://prometheus_http_sd:8000/prom/http_sd/prom_server1/firstjob
      refresh_interval: 1h
```
### 5、API接口
- http://prometheus_http_sd:8000/prom/api/v1/query #for json output
- http://prometheus_http_sd:8000/prom/api/v1/add/targets #for add targets
- http://prometheus_http_sd:8000/prom/api/v1/del/targets #for del targets

### 6、<a href="https://github.com/zh0uhaiwei/prometheus_http_sd_web/docs/Examples.md">文档和示例</a>

## License

This software is free to use under the MIT License [MIT license](/LICENSE).
