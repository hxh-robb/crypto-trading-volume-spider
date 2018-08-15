import sys
import datetime,time,scrapy
import scrapy.crawler as crawler
from multiprocessing import Process, Queue
from twisted.internet import reactor

interval = 1
if len(sys.argv) > 1:
  try:
    interval = int(sys.argv[1])
  except Exception as e:
    pass

class CrypocurrenciesMarketSpider(scrapy.Spider):
  name = 'crypocurrencies-market-spider'
  start_urls = [
    'https://coinmarketcap.com/zh/'
  ]
  tracking = ['id-bitcoin','id-ethereum','id-eos','id-litecoin','id-tether', 'id-ripple']

  def parse(self, response):
    with open('/out/tracking.txt.' + str(interval) + 's', 'a') as f:
      if 200 != response.status:
        return
      record = {}
      record['timestamp'] = datetime.datetime.now().isoformat()[0:22]
      record['names'] = []
      for row in response.xpath('//table/tbody/tr'):
        cc_id = row.xpath('@id').extract_first()
        if cc_id not in self.tracking:
          continue
        
        columns = row.xpath('td')
        cc_name = columns[1].xpath('a/text()').extract_first()
        if cc_name not in record['names']:
          record['names'].append(cc_name)
        trade_volume = columns[4].xpath('a/text()').extract_first()
        percent_change = columns[6].xpath('text()').extract_first()
        record[cc_name] = (trade_volume[1:].replace(',',''),percent_change)
      f.write(record['timestamp'] + '|')
      for name in record['names']:
        f.write(name + (':(%s,%s)' % record[name]))
        if record['names'][-1] != name:
          f.write('|')
      f.write('\n')

def run_spider():
  def f(q):
    try:
      runner = crawler.CrawlerRunner()
      deferred = runner.crawl(CrypocurrenciesMarketSpider)
      deferred.addBoth(lambda _: reactor.stop())
      reactor.run()
      q.put(None)
    except Exception as e:
      q.put(e)
  q = Queue()
  p = Process(target=f,args=(q,))
  p.start()
  result = q.get()
  p.join()
  if result is not None:
    raise result

def main():
  while True:
    #fetch_data()
    run_spider()
    time.sleep(interval)

if __name__ == '__main__':
  main()
