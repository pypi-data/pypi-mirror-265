import requests
from lxml import etree

import warnings
warnings.filterwarnings("ignore")

__all__ = ['hySpider']

class HySpider(object):
  def __init__(self) -> None:
    self.base_url = "https://movie.douban.com"
    self.headers = {
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
      "Accept-Language": "zh-CN,zh;q=0.9,en-CN;q=0.8,en;q=0.7",
      "Cache-Control": "max-age=0",
      "Connection": "keep-alive",
      "Referer": "https://movie.douban.com/",
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    }

  def get_request(self, url) -> requests.Response:
    return requests.get(self.base_url + url, headers=self.headers)
  
  def get_douban(self) -> list:
    resp = self.get_request("/chart")
    if resp.status_code != 200:
      return []
    
    # 解析resp
    html = resp.content
    element = etree.HTML(html)
    nodes = element.xpath("//div[@class='article']//td/div/a[string(.)]")

    results = [self.__handle_text(node.text) for node in nodes]
    return results
  
  def __handle_text(self, text) -> str:
    return text.strip() \
              .replace(" ", '') \
              .replace('\n', '') \
              .replace('/', '')

hySpider = HySpider()
