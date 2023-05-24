# <p align="center">Prometheus_http_sd_targets</p>
# <p align="center">is a web service for <a href="https://prometheus.io/docs/prometheus/latest/http_sd/">Prometheus HTTP SD</a></p>

English | [简体中文](README_zh.md)

## Preface
### When configuring multiple Prometheus instances, the configuration of Targets becomes cumbersome, and the official does not provide a unified display interface, so this project is launched.

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
### 3、Browse http://prometheus_http_sd:8099/overview
### 4、Configure Prometheus
Add a block to the `scrape_configs` of your prometheus.yml config file:

```yaml
scrape_configs:
- job_name: firstjob
    http_sd_configs:
    - url:  http://prometheus_http_sd:8099/http_sd/prom_server1/firstjob
      refresh_interval: 1h
```
### 5、Convenient APIs
- http://prometheus_http_sd:8099/api/v1/query #for json output
- http://prometheus_http_sd:8099/api/v1/add/targets #for add targets
- http://prometheus_http_sd:8099/api/v1/del/targets #for del targets

## License

This software is free to use under the MIT License [MIT license](/LICENSE).
