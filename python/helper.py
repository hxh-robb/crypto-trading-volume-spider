import json
from os import path

def json_path(source_name='', interval=1, base_dir='/tmp'):
  file_name = str(interval) + 's.json'
  file_name = '.'.join([source_name,file_name]) if len(source_name) > 0 else file_name
  file_path = path.abspath(path.join(base_dir, file_name))
  return file_path

def legacy_add(data, source_name='', interval=1, base_dir='/tmp'):
  #print 'Adding record in legacy format'
  file_name = 'txt.' + str(interval) + 's'
  file_name = '.'.join([source_name,file_name]) if len(source_name) > 0 else file_name
  file_path = path.abspath(path.join(base_dir, file_name))
  with open(file_path, 'a') as f:
    f.write(data['timestamp'] + '|')
    f.write('Bitcoin:' + str(data['BTC']['tradingVolume']) + '|')
    f.write('Ethereum:' + str(data['ETH']['tradingVolume']) + '|')
    f.write('XRP:' + str(data['XRP']['tradingVolume']) + '|')
    f.write('EOS:' + str(data['EOS']['tradingVolume']) + '|')
    f.write('Litecoin:' + str(data['LTC']['tradingVolume']) + '|')
    f.write('Tether:' + str(data['USDT']['tradingVolume']))
    f.write('\n')
  #print 'Record in legacy format added'

def add(data, source_name='', interval=1, base_dir='/tmp', need_legacy=False):
  #print 'Adding record'
  with open(json_path(source_name, interval, base_dir), 'a') as f:
    json.dump(data,f)
    f.write('\n')
    if need_legacy:
      legacy_add(data, source_name, interval, base_dir)
  #print 'Record added'

def list(source_name='',interval=1,base_dir='/tmp'):
  rt = []
  with open(json_path(source_name, interval, base_dir), 'r') as f:
    for line in f:
      rt.append(json.loads(line[:-1]))
  return rt
