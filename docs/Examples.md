## Use Redis
```shell
redis-cli -h $REDIS_HOST -p $REDIS_PORT
>auth $REDIS_PASSWORD
>select $REDIS_DB
>keys *
1) "/prom/192.168.255.15/job/job1/labels/app=app1/targets"
 2) "/prom/192.168.19.15/job/job2/targets"
 3) "/prom/192.168.164.15/job/job1/targets"
 4) "/prom/192.168.19.15/job/job1/targets"
 5) "/prom/192.168.219.15/job/job1/labels/app=app6,group=group1/targets"
 6) "/prom/192.168.138.15/job/job1/labels"
 7) "/prom/192.168.255.15/job/job1/labels/app=app2,group=group1/targets"
 8) "/prom/192.168.164.15/job/job1/labels/app=app2,group=group1/targets"
 9) "/prom/192.168.255.15/job/job1/labels"
10) "/prom/192.168.19.15/job/job1/labels/app=app1,group=group1/targets"
11) "/prom/192.168.19.15/job/job1/labels"
12) "/prom/192.168.219.15/job/job1/labels/group=group1/targets"
13) "/prom/192.168.19.15/job/job1/labels/app=app6,group=group1/targets"
14) "/prom/192.168.255.15/job/job2/targets"
15) "/prom/192.168.164.15/job/job2/labels"
16) "/prom/192.168.164.15/job/job3/targets"
17) "/prom/192.168.138.15/job/job1/labels/app=app3,group=group1/targets"
18) "/prom/192.168.219.15/job/job4/targets"
19) "/prom/192.168.138.15/job/job1/targets"
20) "/prom/192.168.255.15/jobs"
21) "/prom/192.168.138.15/jobs"
22) "/prom/192.168.219.15/job/job1/labels"
23) "/prom/192.168.138.15/job/job2/labels"
24) "/prom/192.168.219.15/job/job1/labels/app=app2,group=group1/targets"
25) "/prom/192.168.255.15/job/job1/labels/app=app6,group=group1/targets"
26) "/prom/192.168.219.15/job/job1/labels/app=app2,group=group1,project=project1,zone=zone1/targets"
27) "/prom/192.168.225.15/job/job1/targets"
28) "/prom/192.168.219.15/job/job2/labels/app=app1,group=group1/targets"
29) "/prom/192.168.255.15/job/job3/labels/app=app3,group=group2/targets"
30) "/prom/192.168.164.15/job/job1/labels/app=app6,group=group1/targets"
31) "/prom/192.168.164.15/job/job2/labels/app=app8,group=group1/targets"
32) "/prom/192.168.219.15/job/job2/labels/app=app2,group=group1/targets"
33) "/prom/proms"
```

### use docker
```shell
docker run -it --name prom_http_sd_webb -e DATABASE_BACKEND=redis -e REDIS_HOST=192.168.1.1 -e REDIS_PASSWORD=password -e REDIS_DB=8 -e REDIS_PORT=6379 -p 8000:8000 zh0uhaiwei/prometheus_http_sd_web:latest
```

### use shell
```shell
export DATABASE_BACKEND="redis"
export REDIS_HOST="192.168.1.1"
export REDIS_PORT=6379
export REDIS_DB=8
export REDIS_PASSWORD="password"
```
## Use MySQL
### use docker
```shell
docker run -it --name prom_http_sd_webb -e DATABASE_BACKEND=mysql -e MYSQL_HOST=192.168.1.2 -e MYSQL_PASSWORD=password -e MYSQL_DATABASE=database -e MYSQL_PORT=3306 -e MYSQL_USER=user -p 8000:8000 zh0uhaiwei/prometheus_http_sd_web:latest
```
### use shell
```shell
mysql -h $MYSQL_HOST -u $MYSQL_USER -P $MYSQL_PORT -p $MYSQL_DATABASE
>CREATE TABLE `prom_http_sd_web` (
  `prom` varchar(18) COLLATE utf8_bin NOT NULL,
  `job` varchar(64) COLLATE utf8_bin NOT NULL,
  `labels` varchar(128) COLLATE utf8_bin NOT NULL,
  `target_ip` varchar(18) COLLATE utf8_bin NOT NULL,
  `target_port` int(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
export DATABASE_BACKEND="mysql"
export MYSQL_HOST="192.168.1.2"
export MYSQL_USER="user"
export MYSQL_PORT=3306
export MYSQL_PASSWORD="password"
export MYSQL_DATABASE="database"
>select * from prom_http_sd_web;
+----------------+------+---------------------------------------------------+-----------------+-------------+
| prom           | job  | labels                                            | target_ip       | target_port |
+----------------+------+---------------------------------------------------+-----------------+-------------+
| 192.168.164.15 | job1 | env=env1,group=group1                             | 192.168.164.15  |        9115 |
| 192.168.138.15 | job1 | env=env1,group=group1                             | 192.168.138.15  |        9115 |
| 192.168.225.15 | job1 | app=app1                                          | 192.168.225.15  |        9115 |
| 192.168.255.15 | job1 | app=app1                                          | 192.168.255.15  |        9115 |
| 192.168.19.15  | job1 | app=app1,group=group1                             | 192.168.19.15   |        9115 |
| 192.168.219.15 | job1 | group=group1                                      | 192.168.219.15  |        9115 |
| 192.168.219.15 | job1 | group=group1                                      | 192.168.219.25  |        3000 |
| 192.168.164.15 | job2 | app=app1,group=group1                             | 192.168.162.246 |        9100 |
| 192.168.164.15 | job2 | app=app1,group=group1                             | 192.168.162.247 |        9100 |
| 192.168.164.15 | job2 | app=app1,group=group1                             | 192.168.162.248 |        9100 |
| 192.168.164.15 | job2 | app=app1,group=group1                             | 192.168.162.249 |        9100 |
| 192.168.164.15 | job2 | app=app1,group=group1                             | 192.168.162.250 |        9100 |
| 192.168.164.15 | job2 | app=app8,group=group1                             | 192.168.162.219 |        9100 |
| 192.168.164.15 | job2 | app=app8,group=group1                             | 192.168.162.220 |        9100 |
| 192.168.164.15 | job2 | app=app8,group=group1                             | 192.168.162.29  |        9100 |
| 192.168.255.15 | job2 | app=app8,group=group1                             | 192.168.127.62  |        9100 |
| 192.168.255.15 | job2 | app=app8,group=group1                             | 192.168.200.161 |        9100 |
| 192.168.255.15 | job2 | app=app8,group=group1                             | 192.168.200.162 |        9100 |
| 192.168.255.15 | job2 | app=app8,group=group1                             | 192.168.200.61  |        9100 |
| 192.168.255.15 | job2 | app=app8,group=group1                             | 192.168.200.62  |        9100 |
| 192.168.255.15 | job2 | app=app8,group=group1                             | 192.168.99.141  |        9100 |
| 192.168.255.15 | job2 | app=app8,group=group1                             | 192.168.99.142  |        9100 |
| 192.168.225.15 | job2 | app=app8,group=group1                             | 192.168.137.158 |        9100 |
| 192.168.225.15 | job2 | app=app8,group=group1                             | 192.168.137.159 |        9100 |
| 192.168.225.15 | job2 | app=app8,group=group1                             | 192.168.137.168 |        9100 |
| 192.168.225.15 | job2 | app=app8,group=group1                             | 192.168.137.169 |        9100 |
| 192.168.225.15 | job2 | app=app8,group=group1                             | 192.168.137.178 |        9100 |
| 192.168.225.15 | job2 | app=app8,group=group1                             | 192.168.137.179 |        9100 |
| 192.168.225.15 | job2 | app=app8,group=group1                             | 192.168.137.61  |        9100 |
| 192.168.225.15 | job2 | app=app8,group=group1                             | 192.168.137.62  |        9100 |
| 192.168.225.15 | job2 | app=app8,group=group1                             | 192.168.227.61  |        9100 |
| 192.168.225.15 | job2 | app=app8,group=group1                             | 192.168.227.62  |        9100 |
| 192.168.225.15 | job2 | app=app8,group=group1                             | 192.168.227.70  |        9100 |
| 192.168.225.15 | job2 | app=app8,group=group1                             | 192.168.227.71  |        9100 |
| 192.168.225.15 | job2 | app=app8,group=group1                             | 192.168.227.80  |        9100 |
| 192.168.225.15 | job2 | app=app8,group=group1                             | 192.168.227.81  |        9100 |
| 192.168.225.15 | job2 | app=app8,group=group1                             | 192.168.231.1   |        9100 |
| 192.168.225.15 | job2 | app=app8,group=group1                             | 192.168.231.2   |        9100 |
| 192.168.225.15 | job2 | app=app8,group=group1                             | 192.168.191.61  |        9100 |
| 192.168.225.15 | job2 | app=app8,group=group1                             | 192.168.191.62  |        9100 |
| 192.168.219.15 | job2 | app=app1,group=group1                             | 192.168.212.125 |        9100 |
| 192.168.219.15 | job2 | app=app1,group=group1                             | 192.168.212.126 |        9100 |
| 192.168.164.15 | job2 | app=app5,group=group1                             | 192.168.164.15  |        9100 |
| 192.168.138.15 | job2 | app=app5,group=group1                             | 192.168.138.15  |        9100 |
| 192.168.225.15 | job2 | app=app5,group=group1                             | 192.168.225.15  |        9100 |
| 192.168.255.15 | job2 | app=app5,group=group1                             | 192.168.255.15  |        9100 |
| 192.168.19.15  | job2 | app=app5,group=group1                             | 192.168.19.15   |        9100 |
| 192.168.219.15 | job2 | app=app5,group=group1                             | 192.168.219.15  |        9100 |
| 192.168.219.15 | job2 | app=app5,group=group1                             | 192.168.219.25  |        9100 |
| 192.168.219.15 | job2 | app=app5,group=group1                             | 192.168.219.35  |        9100 |
| 192.168.219.15 | job2 | app=app5,group=group1                             | 192.168.219.36  |        9100 |
| 192.168.219.15 | job2 | app=app5,group=group1                             | 192.168.219.45  |        9100 |
| 192.168.219.15 | job2 | app=app5,group=group1                             | 192.168.219.55  |        9100 |
| 192.168.219.15 | job2 | app=app5,group=group1                             | 192.168.219.56  |        9100 |
| 192.168.164.15 | job1 | app=app6,group=group1                             | 192.168.164.15  |        9091 |
| 192.168.138.15 | job1 | app=app6,group=group1                             | 192.168.138.15  |        9091 |
| 192.168.225.15 | job1 | app=app6,group=group1                             | 192.168.225.15  |        9091 |
| 192.168.255.15 | job1 | app=app6,group=group1                             | 192.168.255.15  |        9091 |
| 192.168.19.15  | job1 | app=app6,group=group1                             | 192.168.19.15   |        9091 |
| 192.168.219.15 | job1 | app=app6,group=group1                             | 192.168.219.15  |        9091 |
| 192.168.164.15 | job3 | app=app3,group=group1                             | 192.168.164.13  |        9121 |
| 192.168.164.15 | job3 | app=app3,group=group1                             | 192.168.162.65  |        9121 |
| 192.168.164.15 | job3 | app=app3,group=group1                             | 192.168.162.65  |        9122 |
| 192.168.164.15 | job3 | app=app3,group=group1                             | 192.168.162.65  |        9123 |
| 192.168.164.15 | job3 | app=app3,group=group1                             | 192.168.162.65  |        9124 |
| 192.168.164.15 | job3 | app=app3,group=group1                             | 192.168.162.98  |        9121 |
| 192.168.164.15 | job3 | app=app3,group=group1                             | 192.168.162.98  |        9122 |
| 192.168.219.15 | job3 | app=app3,group=group1                             | 192.168.212.125 |        9121 |
| 192.168.219.15 | job3 | app=app3,group=group1                             | 192.168.212.126 |        9121 |
| 192.168.164.15 | job2 | app=app2,group=group1                             | 192.168.164.12  |        9100 |
| 192.168.225.15 | job2 | app=app2,group=group1                             | 192.168.136.12  |        9100 |
| 192.168.225.15 | job2 | app=app2,group=group1                             | 192.168.226.12  |        9100 |
| 192.168.225.15 | job2 | app=app2,group=group1                             | 192.168.242.12  |        9100 |
| 192.168.225.15 | job2 | app=app2,group=group1                             | 192.168.244.1   |        9100 |
| 192.168.225.15 | job2 | app=app2,group=group1                             | 192.168.244.2   |        9100 |
| 192.168.225.15 | job2 | app=app2,group=group1                             | 192.168.244.3   |        9100 |
| 192.168.225.15 | job2 | app=app2,group=group1                             | 192.168.244.4   |        9100 |
| 192.168.255.15 | job2 | app=app2,group=group1                             | 192.168.94.12   |        9100 |
| 192.168.19.15  | job2 | app=app2,group=group1                             | 192.168.18.12   |        9100 |
| 192.168.219.15 | job2 | app=app2,group=group1                             | 192.168.219.12  |        9100 |
| 192.168.219.15 | job1 | app=app2,group=group1                             | 192.168.219.45  |       10902 |
| 192.168.219.15 | job4 | app=app2,group=group1                             | 192.168.219.35  |        9090 |
| 192.168.219.15 | job1 | app=app2,group=group1                             | 192.168.219.36  |        9090 |
| 192.168.164.15 | job1 | app=app2,group=group1                             | 192.168.164.15  |       19191 |
| 192.168.138.15 | job1 | app=app3,group=group1                             | 192.168.138.15  |       19191 |
| 192.168.225.15 | job1 | app=app4,group=group1                             | 192.168.225.15  |       19191 |
| 192.168.255.15 | job1 | app=app2,group=group1                             | 192.168.255.15  |       19191 |
| 192.168.19.15  | job1 | app=app2,group=group1                             | 192.168.19.15   |       19191 |
| 192.168.219.15 | job1 | app=app2,group=group1,project=project1,zone=zone1 | 192.168.219.15  |       19191 |
| 192.168.219.15 | job1 | app=app2,group=group1,project=project1,zone=zone1 | 192.168.219.45  |       19191 |
| 192.168.255.15 | job2 | app=app1,group=group2                             | 192.168.96.22   |        9100 |
| 192.168.164.15 | job3 | app=app3,group=group2                             | 192.168.151.11  |        9121 |
| 192.168.255.15 | job3 | app=app3,group=group2                             | 192.168.108.1   |        9121 |
| 192.168.255.15 | job3 | app=app3,group=group2                             | 192.168.115.193 |        9121 |
| 192.168.255.15 | job3 | app=app3,group=group2                             | 192.168.254.11  |        9121 |
| 192.168.255.15 | job3 | app=app3,group=group2                             | 192.168.89.131  |        9121 |
+----------------+------+---------------------------------------------------+-----------------+-------------+
```
## Example
### /prom/overview.html
<p align="center">
    <img src="https://github.com/zh0uhaiwei/prometheus_http_sd_web/assets/113036309/f1b33368-1075-4842-abce-a3bb1a2fd8af"/>
</p>)

### /prom/http_sd/192.168.138.15/job1
<p align="center">
    <img src="https://github.com/zh0uhaiwei/prometheus_http_sd_web/assets/113036309/e2a07e33-faa5-4282-b9ab-b920d6ea6010"/>
</p>)

### /prom/api/v1/query?prom=192.168.138.15
<p align="center">
    <img src="https://github.com/zh0uhaiwei/prometheus_http_sd_web/assets/113036309/2b0d2d23-099d-48a7-84f0-b2ccf426fee2"/>
</p>)
