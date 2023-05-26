#!/usr/bin/env python3
import sys
from flask import request,Flask,render_template,current_app,url_for
import json
import logging
import redis
import time
import pymysql
import atexit
logging.basicConfig(filename='prom_http_sd.log',level=logging.INFO,
                    format="%(asctime)s %(name)s %(levelname)s %(message)s",
                    datefmt = '%Y-%m-%d  %H:%M:%S %a')
import socket
app = Flask(__name__,
            static_url_path='/prom',
            static_folder='static',
            template_folder='templates')
app.config['REDIS_HOST'] = ""
app.config['REDIS_PORT'] = 6379
app.config['REDIS_DB'] = 9
app.config['REDIS_PASSWORD'] = ""
app.config['MYSQL_HOST'] = ""
app.config['MYSQL_USER'] = ''
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DATABASE'] = ''
app.config['DATABASE_BACKEND'] = 'mysql'   #mysql or redis
app.debug = False
def pymysql_query(var_pipe):
  var_result = []
  for i in var_pipe:
    var_result.append(i[0])
  return var_result
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
      if current_app.config['DATABASE_BACKEND'] == 'redis':
        pool = redis.ConnectionPool(host=current_app.config['REDIS_HOST'],port=current_app.config['REDIS_PORT'],db=current_app.config['REDIS_DB'],password=current_app.config['REDIS_PASSWORD'],decode_responses=True)
        r = redis.Redis(connection_pool=pool)
        atexit.register(redis.Redis.close,r)
        pipe=r.pipeline()
      elif current_app.config['DATABASE_BACKEND'] == 'mysql':
        db=pymysql.connect(host=current_app.config['MYSQL_HOST'],port=current_app.config['MYSQL_PORT'],db=current_app.config['MYSQL_DATABASE'],user=current_app.config['MYSQL_USER'],password=current_app.config['MYSQL_PASSWORD'])
        pipe=db.cursor()
        atexit.register(pymysql.connect.close,db)
      else:
        return "NO DATABASE_BACKEND FOUND"
      var_date = time.strftime('%Y%m%d')
      if opt == "add":
        unsortedLabels=labels.split(',')
        unsortedLabels.sort()
        labels=','.join(unsortedLabels)
        if current_app.config['DATABASE_BACKEND'] == 'redis':
          for target in resp_json['targets'].split(','):
              pipe.sadd(f'/prom/{prom}/job/{job}/targets',target)
              pipe.sadd(f'/prom/{prom}/job/{job}/labels/{labels}/targets',target)
              logging.info(f'add {prom} {job} {labels} {target}')
          pipe.sadd(f'/prom/proms',prom)
          pipe.sadd(f'/prom/{prom}/jobs',job)
          pipe.sadd(f'/prom/{prom}/job/{job}/labels',f'{labels}')
          pipe.execute()
        if current_app.config['DATABASE_BACKEND'] == 'mysql':
          try:
            for target in resp_json['targets'].split(','):
              target_ip,target_port = target.split(':')
              logging.info(f'{appGroup} {var_app} {group} {target_ip} {target_port}')
              pipe.execute(f'insert into target (prom_ip,job,labels,target_ip,target_port) values ("{prom}","{job}","{labels}","{target_ip}",{target_port});')
              logging.info(f'add {prom} {job} {labels} {target}')
              db.commit()
          except Exception as exerr:
            db.rollback()
            logging.info(exerr)
            
      if opt == "del":
        if current_app.config['DATABASE_BACKEND'] == 'redis':
          for target in resp_json['targets'].split(','):
              logging.info(f'delete {prom} {job} {labels} {target}')
              pipe.srem(f'/prom/{prom}/job/{job}/targets',target)
              pipe.srem(f'/prom/{prom}/job/{job}/labels/{labels}/targets',target)
          pipe.execute()
        if current_app.config['DATABASE_BACKEND'] == 'mysql':
          try:
            for target in resp_json['targets'].split(','):
                logging.info(f'delete {prom} {job} {labels} {target}')
                target_ip,target_port = target.split(':')
                pipe.execute(f"delete from target where prom_ip='{prom}' and job='{job}' and labels='{labels}' and target_ip='{target_ip}' and target_port={target_port};")
            db.commit()
          except Exception as exerr:
            db.rollback()
            logging.info(exerr)
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
    if current_app.config['DATABASE_BACKEND'] == 'redis':
      pool = redis.ConnectionPool(host=current_app.config['REDIS_HOST'],port=current_app.config['REDIS_PORT'],db=current_app.config['REDIS_DB'],password=current_app.config['REDIS_PASSWORD'],decode_responses=True)
      r = redis.Redis(connection_pool=pool)
      atexit.register(redis.Redis.close,r)
    elif current_app.config['DATABASE_BACKEND'] == 'mysql':
      db=pymysql.connect(host=current_app.config['MYSQL_HOST'],port=current_app.config['MYSQL_PORT'],db=current_app.config['MYSQL_DATABASE'],user=current_app.config['MYSQL_USER'],password=current_app.config['MYSQL_PASSWORD'])
      pipe=db.cursor()
      atexit.register(pymysql.connect.close,db)
    else:
      return "NO DATABASE_BACKEND FOUND"
    results = []
    if current_app.config['DATABASE_BACKEND'] == 'redis':
      proms = r.smembers('/prom/proms')
      for prom in proms:
        result = {}
        result['prom'] = prom
        jobs = r.smembers(f'/prom/{prom}/jobs')
        for job in jobs:
          labels = r.smembers(f'/prom/{prom}/job/{job}/labels')
          result['job']=job
          for label in labels:
            result['labels'] = label
            targets = r.smembers(f'/prom/{prom}/job/{job}/labels/{label}/targets')
            if len(targets)>0:
              result['targets'] = (','.join(targets))
            else:
              result['targets'] = ''
          results.append(result)
    if current_app.config['DATABASE_BACKEND'] == 'mysql':
      pipe.execute("select prom_ip,job,labels,group_concat(concat(target_ip,':',target_port)) as targets from target group by prom_ip,job,labels;")
      qResults = pipe.fetchall()
      results = []
      for qResult in qResults:
        result = {}
        result['prom'] = qResult[0]
        result['job'] = qResult[1]
        result['labels'] = qResult[2]
        result['targets'] = qResult[3]
    q = request.args.get("format",default="html",type=str)
    if q == 'json':
      return json.dumps(results,ensure_ascii=False,indent=4),200,{"Content-Type": "application/json"}
    return render_template('overview.html', results=results)

@app.route('/prom/api/v1/query', methods=['get'])
def prom_query():
    requestIP = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    logging.info(f"request from {requestIP} for query")
    if current_app.config['DATABASE_BACKEND'] == 'redis':
      pool = redis.ConnectionPool(host=current_app.config['REDIS_HOST'],port=current_app.config['REDIS_PORT'],db=current_app.config['REDIS_DB'],password=current_app.config['REDIS_PASSWORD'],decode_responses=True)
      r = redis.Redis(connection_pool=pool)
      atexit.register(redis.Redis.close,r)
    elif current_app.config['DATABASE_BACKEND'] == 'mysql':
      db=pymysql.connect(host=current_app.config['MYSQL_HOST'],port=current_app.config['MYSQL_PORT'],db=current_app.config['MYSQL_DATABASE'],user=current_app.config['MYSQL_USER'],password=current_app.config['MYSQL_PASSWORD'])
      pipe=db.cursor()
      atexit.register(pymysql.connect.close,db)
    else:
      return "NO DATABASE_BACKEND FOUND"
    if current_app.config['DATABASE_BACKEND'] == 'redis':
      prom = '*'
      job = '*'
      labels = []
      for k,v in request.args.items():
        if k == 'prom':
          prom = v
        elif k == 'job':
          job = v
        else:
          labels.append(f'{k}={v}')
      query_keys = r.keys(f"/prom/{prom}/job/{job}/labels/*{'*'.join(labels)}*/targets")
      results = []
      for query_key in query_keys:
          result = {}
          prom_keys = query_key.split('/')
          result['prom'] = prom_keys[2]
          result['job'] = prom_keys[4]
          result['labels'] = prom_keys[6]
          result['targets']=','.join(r.smembers(query_key))
          results.append(result)
    if current_app.config['DATABASE_BACKEND'] == 'mysql':
      q = []
      labels = []
      for k,v in request.args.items():
        if k == 'prom' or k == 'job':
          q.append(f"{k}='{v}'")
        else:
          labels.append(f'{k}={v}')
      iLabels = ','.join(labels)
      q.append(f"labels='{iLabels}'")
      qwhere = ' and '.join(q)
      pipe.execute("select prom_ip,job,labels,group_concat(concat(target_ip,':',target_port)) as targets from target where {qwhere} group by prom_ip,job,labels;")
      qResults = pipe.fetchall()
      results = []
      for qResult in qResults:
        result = {}
        result['prom'] = qResult[0]
        result['job'] = qResult[1]
        result['labels'] = qResult[2]
        result['targets'] = qResult[3]
        results.append(result)
    return json.dumps(results,ensure_ascii=False,indent=4),200,{"Content-Type": "application/json"}


@app.route('/prom/http_sd/<prom_server>/<job_name>', methods=['get'])
def prom_http_sd(prom_server,job_name):
    requestIP = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    logging.info(f"request from {requestIP} for {prom_server} and {job_name}")
    if current_app.config['DATABASE_BACKEND'] == 'redis':
      pool = redis.ConnectionPool(host=current_app.config['REDIS_HOST'],port=current_app.config['REDIS_PORT'],db=current_app.config['REDIS_DB'],password=current_app.config['REDIS_PASSWORD'],decode_responses=True)
      r = redis.Redis(connection_pool=pool)
      atexit.register(redis.Redis.close,r)
    elif current_app.config['DATABASE_BACKEND'] == 'mysql':
      db=pymysql.connect(host=current_app.config['MYSQL_HOST'],port=current_app.config['MYSQL_PORT'],db=current_app.config['MYSQL_DATABASE'],user=current_app.config['MYSQL_USER'],password=current_app.config['MYSQL_PASSWORD'])
      pipe=db.cursor()
      atexit.register(pymysql.connect.close,db)
    else:
      return "NO DATABASE_BACKEND FOUND"
    daten = time.strftime('%Y%m%d')
    result = []
    if current_app.config['DATABASE_BACKEND'] == 'redis':
      originLabels = r.smembers(f'/prom/{prom_server}/job/{job_name}/labels')
      for originLabel in originLabels:
          targets = r.smembers(f'/prom/{prom_server}/job/{job_name}/labels/{originLabel}/targets')
          labels = {}
          for label in originLabel.split(','):
            labelKey,labelValue = label.split('=')
            labels[labelKey] = labelValue
          result.append({"targets": [target for target in targets],"labels": labels})
    if current_app.config['DATABASE_BACKEND'] == 'mysql':
      pipe.execute(f"select prom_ip,job,labels,group_concat(concat(target_ip,':',target_port)) as targets from target where prom_ip='{prom_server}' and job='{job_name}' group by prom_ip,job,labels;")
      qResults = pipe.fetchall()
      for qResult in qResults:
        originLabels = qResult[2]
        targets = qResult[3]
        labels = {}
        for label in originLabels.split(','):
          labelKey,labelValue = label.split('=')
          labels[labelKey] = labelValue
        result.append({"targets": [target for target in targets.split(',')],"labels": labels})

    return json.dumps(result,ensure_ascii=False,indent=4),200,{"Content-Type": "application/json"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
