from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.parse import urlsplit
from urllib.parse import urlparse
from collections import deque
import pandas as pd
from urllib.request import Request, urlopen
import re

def isValidURL(str):

    print("is valid ", str)
    regex = ("((http|https)://)(www.)?" +
             "[a-zA-Z0-9@:%._\\+~#?&//=]" +
             "{2,256}\\.[a-z]" +
             "{2,6}\\b([-a-zA-Z0-9@:%" +
             "._\\+~#?&//=]*)")
     
    p = re.compile(regex)
    if (str == None):
        return False
    if(re.search(p, str)):
        return True
    else:
        return False

def createSiteMap (url):
  new_urls = deque([url])
  processed_urls = set()
  local_urls = set()
  static_assets = set()
  site_map = {}

  while len(new_urls):
    # move url from the queue to processed url set
    url = new_urls.popleft()
    processed_urls.add(url)
    # print the current url
    print('Processing %s' % url)
    # response = requests.get(url)
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    byte_response = urlopen(req, timeout=10).read()
    response = byte_response.decode('utf-8')
    local_urls = set()
    static_assets = set()

    parts = urlsplit(url)
    base = '{0.netloc}'.format(parts)
    strip_base = base.replace('www.', '')
    base_url = '{0.scheme}://{0.netloc}'.format(parts)
    path = url[:url.rfind("/")+1] if "/"in parts.path else url
    print("base_url ", base_url)
    print("path ", path)
    print("strip_base ", strip_base)

    soup = BeautifulSoup(response, "lxml")

    for image in soup.find_all("img"):
        img_url = image.get("src")
        if "/static" in img_url:
          static_assets.add(img_url)


    for link in soup.find_all("a"):
        anchor = link.attrs["href"] if "href" in link.attrs else ''
        if anchor.startswith("/"):
            local_link = base_url + anchor
            if (isValidURL(local_link)):
              local_urls.add(local_link)
        elif strip_base in anchor:
            if (isValidURL(local_link)):
                local_urls.add(anchor)
        elif not anchor.startswith("http"):
            local_link = path + anchor
            if (isValidURL(local_link)):
                local_urls.add(local_link)
        elif "support.sedna.com" in anchor:
            continue
        else:
            continue
    site_map[url] = {"static_assets": static_assets, "links": local_urls}    
    for i in local_urls:
      if not i in new_urls and not i in processed_urls:
        new_urls.append(i)

  site_map_df = pd.DataFrame.from_dict(site_map).T
  print("data frame ", site_map_df.T)
  site_map_df.to_csv("/Users/sadiaali/Desktop/sitemap.csv")

if __name__=="__main__":
    createSiteMap("https://scrapethissite.com")
