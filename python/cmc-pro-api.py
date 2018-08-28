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
  if r.status_code == 200:
    cmc_helper.consume(api_key)
  record = payload2record(r.json())
  helper.add(record, 'scheduled-cmc-pro-api', None, '/out')
  return record

def payload2record(payload = {u'status': {u'timestamp': u'2018-08-27T09:43:49.131Z', u'credit_count': 1, u'error_code': 0, u'error_message': None, u'elapsed': 5}, u'data': {u'EOS': {u'last_updated': u'2018-08-27T09:42:27.000Z', u'quote': {u'USD': {u'market_cap': 4654536548.788471, u'last_updated': u'2018-08-27T09:42:27.000Z', u'percent_change_7d': -0.297575, u'price': 5.13606800014, u'percent_change_24h': 4.34755, u'volume_24h': 443304153.009327, u'percent_change_1h': -0.0171373}}, u'symbol': u'EOS', u'num_market_pairs': 152, u'cmc_rank': 5, u'date_added': u'2017-07-01T00:00:00.000Z', u'slug': u'eos', u'name': u'EOS', u'id': 1765, u'total_supply': 1006245119.9339, u'max_supply': None, u'circulating_supply': 906245117.6}, u'LTC': {u'last_updated': u'2018-08-27T09:43:01.000Z', u'quote': {u'USD': {u'market_cap': 3348578638.5940404, u'last_updated': u'2018-08-27T09:43:01.000Z', u'percent_change_7d': 1.98695, u'price': 57.7078924471, u'percent_change_24h': 1.53742, u'volume_24h': 200259267.899616, u'percent_change_1h': -0.107422}}, u'symbol': u'LTC', u'num_market_pairs': 548, u'cmc_rank': 7, u'date_added': u'2013-04-28T00:00:00.000Z', u'slug': u'litecoin', u'name': u'Litecoin', u'id': 2, u'total_supply': 58026354.7427873, u'max_supply': 84000000, u'circulating_supply': 58026354.7427873}, u'BTC': {u'last_updated': u'2018-08-27T09:42:25.000Z', u'quote': {u'USD': {u'market_cap': 115768477164.00072, u'last_updated': u'2018-08-27T09:42:25.000Z', u'percent_change_7d': 3.84123, u'price': 6717.54925609, u'percent_change_24h': 0.716309, u'volume_24h': 3409605525.41909, u'percent_change_1h': -0.101384}}, u'symbol': u'BTC', u'num_market_pairs': 5921, u'cmc_rank': 1, u'date_added': u'2013-04-28T00:00:00.000Z', u'slug': u'bitcoin', u'name': u'Bitcoin', u'id': 1, u'total_supply': 17233737, u'max_supply': 21000000, u'circulating_supply': 17233737}, u'ETH': {u'last_updated': u'2018-08-27T09:42:31.000Z', u'quote': {u'USD': {u'market_cap': 28168341518.14573, u'last_updated': u'2018-08-27T09:42:31.000Z', u'percent_change_7d': -5.93063, u'price': 277.294403098, u'percent_change_24h': 1.12875, u'volume_24h': 1280611536.77734, u'percent_change_1h': -0.134968}}, u'symbol': u'ETH', u'num_market_pairs': 4055, u'cmc_rank': 2, u'date_added': u'2015-08-07T00:00:00.000Z', u'slug': u'ethereum', u'name': u'Ethereum', u'id': 1027, u'total_supply': 101582798.6553, u'max_supply': None, u'circulating_supply': 101582798.6553}, u'USDT': {u'last_updated': u'2018-08-27T09:42:27.000Z', u'quote': {u'USD': {u'market_cap': 2797836955.6048694, u'last_updated': u'2018-08-27T09:42:27.000Z', u'percent_change_7d': -0.111191, u'price': 1.00204023412, u'percent_change_24h': 0.110159, u'volume_24h': 2074310322.36387, u'percent_change_1h': 0.0899876}}, u'symbol': u'USDT', u'num_market_pairs': 1272, u'cmc_rank': 8, u'date_added': u'2015-02-25T00:00:00.000Z', u'slug': u'tether', u'name': u'Tether', u'id': 825, u'total_supply': 3080109502.1043, u'max_supply': None, u'circulating_supply': 2792140335.6243}, u'XRP': {u'last_updated': u'2018-08-27T09:43:04.000Z', u'quote': {u'USD': {u'market_cap': 13012304334.326565, u'last_updated': u'2018-08-27T09:43:04.000Z', u'percent_change_7d': -2.74204, u'price': 0.329221151079, u'percent_change_24h': 1.81139, u'volume_24h': 187711279.569359, u'percent_change_1h': 0.0230347}}, u'symbol': u'XRP', u'num_market_pairs': 194, u'cmc_rank': 3, u'date_added': u'2013-08-04T00:00:00.000Z', u'slug': u'ripple', u'name': u'XRP', u'id': 52, u'total_supply': 99991865246, u'max_supply': 100000000000, u'circulating_supply': 39524508956}}}):
  record = {}
  record['local_timestamp'] = datetime.datetime.now().isoformat()[0:19]
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

def main():
  while True:
    try:
      delay = 20
      if fetch_data() is None:
        delay = 86400

      sleep_time = -1
      while sleep_time < 0:
        current = datetime.datetime.now()
        next_sec = (current + datetime.timedelta(0,delay)).replace(microsecond=0)
        d = next_sec - current
        if d.days < 0:
          sleep_time = d.days
        else:
          sleep_time = d.total_seconds()
      time.sleep(sleep_time)
    except Exception as e:
      break

if __name__ == '__main__':
  main()
  # TODO:change prediction
