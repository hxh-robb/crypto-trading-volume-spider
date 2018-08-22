import sys,helper
import datetime,time,requests,schedule

tracking = ['BTC', 'ETH', 'XRP', 'EOS', 'LTC', 'USDT']

interval = 1
if len(sys.argv) > 1:
  try:
    interval = int(sys.argv[1])
  except Exception as e:
    pass

if interval < 60:
  interval = 60

def fetch_data():
  record = {}
  record['timestamp'] = datetime.datetime.now().isoformat()[0:19]
  r = requests.get('https://coin-api.bitcoin.com/v1/ticker')
  payload = r.json()
  for symbol in tracking:
    record[symbol] = {}
    record[symbol]['tradingVolume'] = payload['data']['byId'][symbol]['24hVolumeUsd']
  helper.add(record,'scheduled-bitcoincom',interval,'/out', True)

def next_schedule_job(need_run_job=True, schedule_interval=interval):
  if need_run_job:
    try:
      fetch_data()
    except Exception as e:
      #helper.add(,'scheduled-bitcoincom',interval,'/out', True)
      print datetime.datetime.now().isoformat()[0:19], 'ERROR', e

  t = (datetime.datetime.now() + datetime.timedelta(0,schedule_interval)).strftime('%H:%M')
  print datetime.datetime.now().isoformat()[0:22] + ":next bitcoin.com data fetching run will start at " + t

  schedule.every().day.at(t).do(next_schedule_job)
  return schedule.CancelJob

def main():
  next_schedule_job(False,60)
  while True:
    schedule.run_pending()
    time.sleep(0.01)

if __name__ == '__main__':
  main()
