# <p align="center">Prometheus_http_sd_targets</p>
# <p align="center">是一个<a href="https://prometheus.io/docs/prometheus/latest/http_sd/">Prometheus HTTP SD</a>的web服务</p>

[English](README_zh.md) | 简体中文

## 一、前言
### 当配置多个Prometheus实例，Targets的配置会变得繁琐，官方没有提供统一展示的界面，所以启动本项目。

## 二、Python3组件
- <a href="https://flask.palletsprojects.com/en/2.3.x/">Flask</a>
- <a href="https://pypi.org/project/redis/">redis-py</a>

## 三、开始
### 1、启动<a href="https://redis.io/docs/getting-started/">Redis</a>实例
### 2、启动app
```shell
git clone https://github.com/zh0uhaiwei/prometheus_http_sd_targets.git prom_http_sd
cd prom_http_sd
#Edit redis instance config in app.config
pip3 install -r requirments.txt
python3 app.py
```
### 3、浏览器打开http://prometheus_http_sd:8099

### 4、配置Prometheus
Add a block to the `scrape_configs` of your prometheus.yml config file:

```yaml
scrape_configs:
- job_name: firstjob
    http_sd_configs:
    - url:  http://prometheus_http_sd:8099/http_sd/prom_server1/firstjob
      refresh_interval: 1h
```
### 5、API接口
- http://prometheus_http_sd:8099/api/v1/query #for json output
- http://prometheus_http_sd:8099/api/v1/add/targets #for add targets
- http://prometheus_http_sd:8099/api/v1/del/targets #for del targets

## 四、License

This software is free to use under the MIT License [MIT license](/LICENSE).
