import os, signal, time, datetime, threading


class ApiKeysHelper:
  def __init__(self, filename='/cmc/api_keys.txt'):
    self.calls_limit = {
      'cpm':10, # calls per minute
      'cpd':200, # calls per day
      'cpmo':6000 # calls per month
    }
    self.api_keys = {}
    
    self.filename = filename

    self.t = threading.Thread(target=self.run)
    self.t.daemon = True
    self.t.start()

  def run(self):
    while True:
      curr = datetime.datetime.now()
      #print curr, self.api_keys.values()
      if curr.second == 0:
        self.set_calls(cpm=0)
        if curr.hour == 0 and curr.minute == 0:
          self.set_calls(cpd=0)
          if curr.day == 1:
            self.set_calls(cpmo=0)
      else:
        self.load(False)
      sleep_time = -1
      while sleep_time < 0:
        next_sec = (curr + datetime.timedelta(0,1)).replace(microsecond=0)
        delta = next_sec - datetime.datetime.now()
        if delta.days >= 0:
          sleep_time = delta.total_seconds()
          break
      time.sleep(sleep_time)

  def load(self, need_print=True):
    if not os.path.exists(self.filename) or not os.path.isfile(self.filename):
      print 'file not found, init [%s]' % filename
      with open(self.filename,'w+') as f:
        f.write('<api_key>,<cpm>,<cpd>,<cpmo>\n')
      return False
    try:
      with open(self.filename,'r') as f:
        for line in f:
          if '\n' in line:
            line = line[:-1]
          payload = line.split(',')
          if len(payload) > 1:
            self.api_keys[payload[0]] = {}
            self.api_keys[payload[0]]['cpm'] = int(payload[1])
            self.api_keys[payload[0]]['cpd'] = int(payload[2])
            self.api_keys[payload[0]]['cpmo'] = int(payload[3])
            self.api_keys[payload[0]]['desc'] = payload[4]
        if need_print:
          print 'CMC api keys loaded'
        return True
    except Exception as e:
      print 'cannot load cmc api keys'
      return False

  def set_calls(self, api_key=None, cpm=None, cpd=None, cpmo=None,need_save=True):
    try:
      if api_key != None and api_key not in self.api_keys:
        print '[%s] not found' & api_key
        return False

      if api_key == None:
        for k in self.api_keys:
          self.set_calls(k,cpm,cpd,cpmo,False)
      else:
        if cpm != None:
          self.api_keys[api_key]['cpm'] = cpm
        if cpd != None:
          self.api_keys[api_key]['cpd'] = cpd
        if cpmo != None:
          self.api_keys[api_key]['cpmo'] = cpmo
      if(need_save):
        return self.save()
    except Exception as e:
      return False

  def consume(self, api_key):
    try:
      if api_key not in self.api_keys:
        print 'api key[%s] not found' % api_key
        return False
      self.api_keys[api_key]['cpm'] = self.api_keys[api_key]['cpm'] + 1
      self.api_keys[api_key]['cpd'] = self.api_keys[api_key]['cpd'] + 1
      self.api_keys[api_key]['cpmo'] = self.api_keys[api_key]['cpmo'] + 1
      return self.save()
    except Exception as e:
      return False

  def pick_api_key(self):
    valid_keys = [k for k in self.api_keys if self.api_keys[k]['cpm'] < self.calls_limit['cpm'] and self.api_keys[k]['cpd'] < self.calls_limit['cpd'] and self.api_keys[k]['cpmo'] < self.calls_limit['cpmo']]
    if len(valid_keys) == 0:
      return None
    return sorted(valid_keys, key=lambda x:self.api_keys[x]['cpm'] + self.api_keys[x]['cpd'] + self.api_keys[x]['cpmo'])[0]

  def save(self):
    try:
      with open(self.filename,'w') as f:
        for k in self.api_keys:
          f.write('%s,%d,%d,%d,%s\n' % (k, self.api_keys[k]['cpm'], self.api_keys[k]['cpd'], self.api_keys[k]['cpmo'], self.api_keys[k]['desc']))
      return True
    except Exception as e:
      return False
    finally:
      print '==========[%s]=========' % datetime.datetime.now()
      for row in self.api_keys.values():
        print row
      print '================================================'

  def interval(self):
    valid_keys = [k for k in self.api_keys if self.api_keys[k]['cpm'] < self.calls_limit['cpm'] and self.api_keys[k]['cpd'] < self.calls_limit['cpd'] and self.api_keys[k]['cpmo'] < self.calls_limit['cpmo']]
    raw = 60 // (len(valid_keys) * 193 // 1440)
    divisors = [2,3,4,5,6,10,12,15,20,30]
    for d in divisors:
      if d >= raw:
        return d
    return 60
if __name__ == '__main__':
  obj = ApiKeysHelper()

  obj.load()
  while True:
    obj.consume(obj.pick_api_key())
    time.sleep(1)
