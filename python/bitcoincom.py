import sys,helper
import datetime,time,requests

tracking = ['BTC', 'ETH', 'XRP', 'EOS', 'LTC', 'USDT']

interval = 1
if len(sys.argv) > 1:
  try:
    interval = int(sys.argv[1])
  except Exception as e:
    pass

def fetch_data():
  record = {}
  record['timestamp'] = datetime.datetime.now().isoformat()[0:22]
  r = requests.get('https://coin-api.bitcoin.com/v1/ticker')
  payload = r.json()
  for symbol in tracking:
    record[symbol] = {}
    record[symbol]['tradingVolume'] = payload['data']['byId'][symbol]['24hVolumeUsd']
  helper.add(record,'bitcoincom',interval,'/out', True)

def main():
  while True:
    fetch_data()
    time.sleep(interval)

if __name__ == '__main__':
  main()
