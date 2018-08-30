import helper,cmc
import sys,datetime,time,requests

cmc_helper = cmc.ApiKeysHelper()
cmc_helper.load()

def fetch_data():
  api_key = cmc_helper.pick_api_key()
  if api_key is None:
    print datetime.datetime.now(), 'No available api key'
    return None
  url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
  h = {'X-CMC_PRO_API_KEY':api_key}
  p = {'symbol':'BTC,ETH,LTC,XRP,EOS,USDT'}
  r = requests.get(url, params=p, headers=h)
  if r.status_code != 200:
    print  '[%s]Fail to fetch data from pro api, status code=%s' % (datetime.datetime.now(), r.status_code)
    return None
  if r.status_code == 200:
    cmc_helper.consume(api_key)
  record = payload2record(r.json())
  helper.add(record, 'scheduled-cmc-pro-api.%s' % datetime.datetime.now().strftime('%Y%m%d'), None, '/out')
  return record

def payload2record(payload):
  record = {}
  record['local_timestamp'] = datetime.datetime.now().isoformat()
  record['local_change_minute'] = datetime.datetime.now().isoformat()[14:16]
  record['local_change_second'] = datetime.datetime.now().isoformat()[17:19]
  record['remote_timestamp'] = payload['status']['timestamp']
  record['remote_change_minute'] = datetime.datetime.now().isoformat()[14:16]
  record['remote_change_second'] = datetime.datetime.now().isoformat()[17:19]
  for symbol in payload['data']:
    record[symbol] = {}
    record[symbol]['tradingVolume'] = payload['data'][symbol]['quote']['USD']['volume_24h']
    record[symbol]['lastUpdated'] = payload['data'][symbol]['quote']['USD']['last_updated']
    record[symbol]['changeMinute'] = int(payload['data'][symbol]['quote']['USD']['last_updated'][14:16])
    record[symbol]['changeSecond'] = int(payload['data'][symbol]['quote']['USD']['last_updated'][17:19])
  return record

def main(given_interval=None):
  start_time = (datetime.datetime.now() + datetime.timedelta(0,120)).replace(second=0, microsecond=0)
  print 'start time:%s' % start_time
  time.sleep((start_time - datetime.datetime.now()).total_seconds())
  interval = cmc_helper.interval()
  while True:
    try:
      current = datetime.datetime.now()
      if current.second == 0:
        interval = cmc_helper.interval()
        if given_interval is not None:
          interval = given_interval # using given frequently period
      if fetch_data() is None:
        print 'Cannot fetch data'
        interval = ((datetime.datetime.now() + datetime.timedelta(0,3600)).replace(minute=0, second=0, microsecond=0) - datetime.datetime.now()).total_seconds()
        print interval
      print 'interval time:%s' % interval
      sleep_time = -1
      while sleep_time < 0:
        next_loop = (current + datetime.timedelta(0,interval)).replace(microsecond=0)
        d = next_loop - datetime.datetime.now()
        if d.days < 0:
          sleep_time = d.days
          current = datetime.datetime.now()
        else:
          sleep_time = d.total_seconds()
      print 'sleep time:%s' % sleep_time
      time.sleep(sleep_time)
    except Exception as e:
      print e
      break

if __name__ == '__main__':
  interval = cmc_helper.interval()
  if len(sys.argv) > 1:
    try:
      interval = int(sys.argv[1])
    except Exception as e:
      pass

  if interval < 2:
    interval = 2
  elif interval > 60:
    interval = None
  main(interval)
  # TODO:change prediction
