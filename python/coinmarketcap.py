import sys,helper
import schedule
import datetime,time,scrapy
import scrapy.crawler as crawler
#from scrapy import signals
#from scrapy.xlib.pydispatch import dispatcher
from multiprocessing import Process, Queue
from twisted.internet import reactor

interval = 1
if len(sys.argv) > 1:
  try:
    interval = int(sys.argv[1])
  except Exception as e:
    pass

if interval < 60:
  interval = 60

class CoinmarketcapSpider(scrapy.Spider):
  #scrapy.utils.log.configure_logging(install_root_handler=False)
  #logging.basicConfig(filename='/out/scheduled-coinmarketcap-spider-log.txt', format='%(levelname)s:%(message)s', level=logging.INFO)
  name = 'coinmarketcap-spider'
  #download_timeout = 5

  #def __init__(self):
  #  dispatcher.connect(self.spider_closed, signals.spider_closed)

  start_urls = [
    'https://coinmarketcap.com/zh/'
  ]
  
  tracking = ['id-bitcoin','id-ethereum','id-eos','id-litecoin','id-tether', 'id-ripple']
  cc_name_dict = {
    'Bitcoin':'BTC',
    'Litecoin':'LTC',
    'EOS':'EOS',
    'Ethereum':'ETH',
    'Tether':'USDT',
    'XRP':'XRP'
  }

  #def start_requests(self):
  #  yield scrapy.Request(self.start_urls[0], self.parse, errback=self.handle_error)

  def start_requests(self):
    self.record = {}
    self.record['timestamp'] = datetime.datetime.now().isoformat()[0:19]
    for url in self.start_urls:
      yield scrapy.Request(url, self.parse)

  def parse(self, response):
    if 200 != response.status:
      print datetime.datetime.now().isoformat()[0:22] + ":failure to fetch coinmarketcap",response.status
      return
    print datetime.datetime.now().isoformat()[0:22] + ":coinmarketcap is fetched"
    record = self.record 
    #record['timestamp'] = datetime.datetime.now().isoformat()[0:22]
    for row in response.xpath('//table/tbody/tr'):
      cc_id = row.xpath('@id').extract_first()
      if cc_id not in self.tracking:
        continue
      
      columns = row.xpath('td')
      cc_name = self.cc_name_dict[columns[1].xpath('a/text()').extract_first()]
      record[cc_name] = {}
      record[cc_name]['tradingVolume'] = int(columns[4].xpath('a/text()').extract_first()[1:].replace(',',''))
      record[cc_name]['percentChange'] = columns[6].xpath('text()').extract_first()
    helper.add(record,'scheduled-coinmarketcap', interval, '/out', True)

  def handle_error(self,failure):
    print datetime.datetime.now().isoformat()[0:22] + ":failure to fetch coinmarketcap",failure

  #def spider_closed(self, spider):
  #  print 'test - spider_closed'

def run_spider():
  print datetime.datetime.now().isoformat()[0:22] + ":fetching coinmarketcap"
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

def next_schedule_job():
  run_spider()
  
  t = (datetime.datetime.now() + datetime.timedelta(0,60)).strftime('%H:%M')
  schedule.every().day.at(t).do(next_schedule_job)

  return schedule.CancelJob

def main():
  t = (datetime.datetime.now() + datetime.timedelta(0,60)).strftime('%H:%M')
  print datetime.datetime.now().isoformat()[0:22] + ":coinmarketcap spider will start at " + t
  schedule.every().day.at(t).do(next_schedule_job)
  
  while True:
    schedule.run_pending()
    time.sleep(0.01)

    #run_spider()
    #time.sleep(interval)

if __name__ == '__main__':
  main()
