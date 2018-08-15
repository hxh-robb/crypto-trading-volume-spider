import json
from os import path

def json_path(source_name='', interval=1, base_dir='/tmp'):
  file_name = str(interval) + 's.json'
  file_name = '.'.join([source_name,file_name]) if len(source_name) > 0 else file_name
  file_path = path.abspath(path.join(base_dir, file_name))
  return file_path

def add(data, source_name='', interval=1, base_dir='/tmp'):
  with open(json_path(source_name, interval, base_dir), 'a') as f:
    json.dump(data,f)
    f.write('\n')

def list(source_name='',interval=1,base_dir='/tmp'):
  rt = []
  with open(json_path(source_name, interval, base_dir), 'r') as f:
    for line in f:
      rt.append(json.loads(line[:-1]))
  return rt
