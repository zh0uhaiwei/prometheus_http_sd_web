# <p align="center">Prometheus_http_sd_targets</p>
# <p align="center">是一个为<a href="https://prometheus.io/docs/prometheus/latest/http_sd/">Prometheus HTTP SD</a>的web服务</p>

[English](README_zh.md) | 简体中文

## Python3组件
- <a href="https://flask.palletsprojects.com/en/2.3.x/">Flask</a>
- <a href="https://pypi.org/project/redis/">redis-py</a>

## 开始
### 1、启动<a href="https://redis.io/docs/getting-started/">Redis</a>实例
### 2、启动app
```shell
git clone https://github.com/zh0uhaiwei/prometheus_http_sd_targets.git prom_http_sd
cd prom_http_sd
#Edit redis instance config in app.config
pip3 install -r requirments.txt
python3 app.py
```
### 3、浏览器打开http://localhost:8099
## License

This software is free to use under the MIT License [MIT license](/LICENSE).
