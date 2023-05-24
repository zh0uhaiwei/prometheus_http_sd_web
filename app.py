#!/usr/bin/env python3
import sys
import flask
from flask import request,Flask,render_template,current_app
import json
import logging
import redis
import time
logging.basicConfig(filename='/var/log/prom_http_sd.log',level=logging.INFO,
                    format="%(asctime)s %(name)s %(levelname)s %(message)s",
                    datefmt = '%Y-%m-%d  %H:%M:%S %a')
import socket
app = Flask(__name__)
app.config['REDIS_HOST'] = "127.0.0.1"
app.config['REDIS_PORT'] = 6379
app.config['REDIS_DB'] = 9
app.config['REDIS_PASSWORD'] = ""

app.debug = False

@app.route('/prom/api/v1/<opt>/targets', methods=['post'])
def prom_targets_opt(opt):
    request_data = request.get_data(as_text=True)
    logging.info(f'this request data:{request_data}')
    resp_json = json.loads(request_data)
    requestIP = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    logging.info(f"request from {requestIP}")
    resp_keys = resp_json.keys()
    if 'prom' not in resp_keys:
      return 'no prom server'
    prom = resp_json["prom"]
    if 'job' not in resp_keys:
      return 'no job'
    job = resp_json["job"]
    if 'labels' not in resp_keys:
      return 'no labels'
    labels = resp_json["labels"]
    if 'targets' not in resp_keys:
      return 'no targets'
    try:
      resp ={}
      resp['err'] = 0
      resp['msg'] = 'success'
      pool = redis.ConnectionPool(host=current_app.config['REDIS_HOST'],port=current_app.config['REDIS_PORT'],db=current_app.config['REDIS_DB'],password=current_app.config['REDIS_PASSWORD'],decode_responses=True)
      r = redis.Redis(connection_pool=pool)
      pipe=r.pipeline()
      var_date = time.strftime('%Y%m%d')
      if opt == "add":
        unsortedLabels=labels.split(',')
        unsortedLabels.sort()
        labels=','.join(unsortedLabels)
        for target in resp_json['targets'].split(','):
            pipe.sadd(f'/prom/{prom}/job/{job}/targets',target)
            pipe.sadd(f'/prom/{prom}/job/{job}/labels/{labels}/targets',target)
            pipe.set(f'/prom/{prom}/job/{job}/target/{target}/date/{var_date}/add', labels)
            logging.info(f'add {prom} {job} {labels} {target}')
        pipe.sadd(f'/prom/proms',prom)
        pipe.sadd(f'/prom/{prom}/jobs',job)
        pipe.sadd(f'/prom/{prom}/job/{job}/labels',f'{labels}')
      if opt == "del":
        for target in resp_json['targets'].split(','):
            logging.info(f'delete {prom} {job} {labels} {target}')
            pipe.srem(f'/prom/{prom}/job/{job}/targets',target)
            pipe.srem(f'/prom/{prom}/job/{job}/labels/{labels}/targets',target)
            pipe.set(f'/prom/{prom}/job/{job}/target/{target}/date/{var_date}/del', labels)
      pipe.execute()
      resp['msg'] = f'{opt} targets {resp_json["targets"]} with labels {labels} success.'
    except Exception as exerr:
      resp['err'] = 1
      logging.info(exerr)
      resp['msg'] = f'{exerr}'
    return json.dumps(resp,indent=4),200,{"Content-Type": "application/json"}

@app.route('/prom/overview', methods=['get'])
def prom_overview():
    requestIP = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    logging.info(f"request from {requestIP} for overview")
    pool = redis.ConnectionPool(host=current_app.config['REDIS_HOST'],port=current_app.config['REDIS_PORT'],db=current_app.config['REDIS_DB'],password=current_app.config['REDIS_PASSWORD'],decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    proms = r.smembers('/prom/proms')
    results = []
    for prom in proms:
      result = {}
      result['prom'] = prom
      result['labels'] = []
      jobs = r.smembers(f'/prom/{prom}/jobs')
      for job in jobs:
        labels = r.smembers(f'/prom/{prom}/job/{job}/labels')
        for label in labels:
          targets = r.smembers(f'/prom/{prom}/job/{job}/labels/{label}/targets')
          if len(targets)>0:
            result['labels'].append(';'.join([job,label,','.join(targets)]))
          else:
            result['labels'].append(';'.join([job,label,'']))
      results.append(result)
    q = request.args.get("format",default="html",type=str)
    if q == 'json':
      return json.dumps(results,ensure_ascii=False,indent=4),200,{"Content-Type": "application/json"}
    return render_template('overview.html', results=results)

@app.route('/prom/query', methods=['get'])
def prom_query():
    requestIP = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    logging.info(f"request from {requestIP} for query")
    prom = request.args.get("prom",default="*",type=str)
    job = request.args.get("job",default="*",type=str)
    labels = request.args.get("labels",default="*",type=str)
    pool = redis.ConnectionPool(host=current_app.config['REDIS_HOST'],port=current_app.config['REDIS_PORT'],db=current_app.config['REDIS_DB'],password=current_app.config['REDIS_PASSWORD'],decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    daten = time.strftime('%Y%m%d')
    query_keys = r.keys(f"\/prom\/{prom}/job\/{job}\/labels\/{labels}\/targets")
    result = {}
    for query_key in query_keys:
        prom_keys = query_key.split('/')
        prom = prom_keys[2]
        if prom not in result:
          result[prom]={}
        job = prom_keys[4]
        if job not in result[prom]:
          result[prom][job]={}
        labels = prom_keys[6]
        if labels not in result[prom][job]:
          result[prom][job][labels]={}
        result[prom][job][labels] = ','.join(r.smembers(query_key))
    return json.dumps(result,ensure_ascii=False,indent=4),200,{"Content-Type": "application/json"}


@app.route('/prom/http_sd/<prom_server>/<job_name>', methods=['get'])
def prom_http_sd(prom_server,job_name):
    requestIP = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    logging.info(f"request from {requestIP} for {prom_server} and {job_name}")
    pool = redis.ConnectionPool(host=current_app.config['REDIS_HOST'],port=current_app.config['REDIS_PORT'],db=current_app.config['REDIS_DB'],password=current_app.config['REDIS_PASSWORD'],decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    daten = time.strftime('%Y%m%d')
    result = []
    originLabels = r.smembers(f'/prom/{prom_server}/job/{job_name}/labels')
    for originLabel in originLabels:
        targets = r.smembers(f'/prom/{prom_server}/job/{job_name}/labels/{originLabel}/targets')
        labels = {}
        for label in originLabel.split(','):
          labelKey,labelValue = label.split('=')
          labels[labelKey] = labelValue
        result.append({"targets": [target for target in targets],"labels": labels})
    return json.dumps(result,ensure_ascii=False,indent=4),200,{"Content-Type": "application/json"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8099, debug=True)
