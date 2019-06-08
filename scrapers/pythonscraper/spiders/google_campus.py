import scrapy
import textwrap
import json
import calendar
from pprint import pprint
from urllib.parse import urlparse, parse_qs
from scrapy.spiders import CrawlSpider
from pythonscraper.items import Event
from dateutil.parser import parse

class GoogleCampusSpyder(CrawlSpider):

    name = 'google_campus'
    allowed_domains = ['campus.co']
    start_urls = ['https://www.campus.co/api/campuses/madrid/events/v2']

    def parse(self, response):
        resp_formateada = response.body_as_unicode()[6:] # elimina )]}', al principio del json
        jsonresponse = json.loads(resp_formateada)

        for obj in jsonresponse['objects']:
            event = Event()
            event['title'] = obj['name']
            event['group'] = obj['host_company_name']
            event['source'] = 'google_campus'
            event['abstract'] = obj['description_preview']
            event['datetime'] =  self.getTimeStamp(obj['local_start_str'])#obj['local_start_str'].split('T')[0]
            event['location'] = {}
            event['location']['address'] = 'Calle Moreno Nieto, 2, 28005 Madrid'
            event['location']['lat'] = '40.4124265'
            event['location']['lng'] = '-3.7204109'
            yield event

    def getTimeStamp(self, date_str): 
        if (date_str is None):
            return None
        date  = parse(date_str)#datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
        date_str = str(calendar.timegm(date.utctimetuple()))
        return date_str+'000'