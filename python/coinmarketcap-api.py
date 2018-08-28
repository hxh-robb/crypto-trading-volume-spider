import sys,helper
import datetime,time,requests,schedule

interval = 1
if len(sys.argv) > 1:
  try:
    interval = int(sys.argv[1])
  except Exception as e:
    pass

if int(interval) <= 0:
  interval = 60

last_fetched = [-1,-1]

def fetch_data():
  record = {}
  record['timestamp'] = datetime.datetime.now().isoformat()[0:19]
  r = requests.get('https://api.coinmarketcap.com/v2/ticker/1/')
  payload = r.json()
  record['last_updated'] = payload['data']['last_updated']
  record['tradingVolume'] = payload['data']['quotes']['USD']['volume_24h']
  if last_fetched[0] == record['last_updated'] and last_fetched[1] == record['tradingVolume']:
    print "Ignore this fetching", last_fetched, record
    return
  
  print "Save this fetching", last_fetched, record
  last_fetched[0] = record['last_updated']
  last_fetched[1] = record['tradingVolume']
  helper.add(record,'scheduled-coinmarketcap-api-btc',interval,'/out')

def next_schedule_job(need_run_job=True, schedule_interval=interval):
  if need_run_job:
    try:
      fetch_data()
    except Exception as e:
      #helper.add(,'scheduled-bitcoincom',interval,'/out', True)
      print datetime.datetime.now().isoformat()[0:19], 'ERROR', e

  t = (datetime.datetime.now() + datetime.timedelta(0,schedule_interval)).strftime('%H:%M')
  print datetime.datetime.now().isoformat()[0:22] + ":next api.coinmarketcap.com data fetching run will start at " + t

  schedule.every().day.at(t).do(next_schedule_job)
  return schedule.CancelJob

def main():
  #next_schedule_job(False,60)
  while True:
    if( interval >= 60):
      schedule.run_pending()
      time.sleep(0.01)
    else:
      try:
        fetch_data()
      except Exception as e:
        print datetime.datetime.now().isoformat()[0:19], 'ERROR', e
      time.sleep(interval)

if __name__ == '__main__':
  main()
