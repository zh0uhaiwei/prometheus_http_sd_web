# <p align="center">Prometheus_http_sd_targets</p>
# <p align="center">is a web service for<a href="https://prometheus.io/docs/prometheus/latest/http_sd/">Prometheus HTTP SD</a></p>

English | [简体中文](README_zh.md)

## Python3 Requirements
- <a href="https://flask.palletsprojects.com/en/2.3.x/">Flask</a>
- <a href="https://pypi.org/project/redis/">redis-py</a>

## GetStarted
### 1、Start a <a href="https://redis.io/docs/getting-started/">Redis</a> instance
### 2、Start app
```shell
git clone https://github.com/zh0uhaiwei/prometheus_http_sd_targets.git prom_http_sd
cd prom_http_sd
#Edit redis instance config in app.config
pip3 install -r requirments.txt
python3 app.py
```
### 3、Browse http://localhost:8099

## License

This software is free to use under the MIT License [MIT license](/LICENSE).
