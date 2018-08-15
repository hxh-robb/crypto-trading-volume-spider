import sys,helper
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

class CoinmarketcapSpider(scrapy.Spider):
  name = 'coinmarketcap-spider'
  start_urls = [
    'https://coinmarketcap.com/zh/'
  ]
  tracking = ['id-bitcoin','id-ethereum','id-eos','id-litecoin','id-tether', 'id-ripple']

  def parse(self, response):
    if 200 != response.status:
      return
    record = {}
    record['timestamp'] = datetime.datetime.now().isoformat()[0:22]
    for row in response.xpath('//table/tbody/tr'):
      cc_id = row.xpath('@id').extract_first()
      if cc_id not in self.tracking:
        continue
      
      columns = row.xpath('td')
      cc_name = columns[1].xpath('a/text()').extract_first()
      record[cc_name] = {}
      record[cc_name]['tradingVolume'] = columns[4].xpath('a/text()').extract_first()
      record[cc_name]['percentChange'] = columns[6].xpath('text()').extract_first()
    helper.add(record,'coinmarketcap', interval, '/out')

def run_spider():
  def f(q):
    try:
      runner = crawler.CrawlerRunner()
      deferred = runner.crawl(CoinmarketcapSpider)
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
    run_spider()
    time.sleep(interval)

if __name__ == '__main__':
  main()
