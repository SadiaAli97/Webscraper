from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.parse import urlsplit
from collections import deque
import pandas as pd
from urllib.request import Request, urlopen
from urllib.parse import urlparse
import re
import urllib
import socket

# Update the location to the location where you want the csv to be downloaded
filename = "sitemap.csv"
def uri_validator(x):
    print("url validating ", x)
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except:
        return False

def isValidURL(str):

    regex = ("((http|https)://)(www.)?" +
             "[a-zA-Z0-9@:%._\\+~#?&//=]" +
             "{2,256}\\.[a-z]" +
             "{2,6}\\b([-a-zA-Z0-9@:%" +
             "._\\+~?&//=]*)")
     
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
  site_map = {}
  broken_urls = set()

  while len(new_urls):
    # move url from the queue to processed url set
    url = new_urls.popleft()
    processed_urls.add(url)
    # print the current url
    print('Processing %s' % url)
    isValid = uri_validator(url)
    if (not isValid):
      print("invalid url ", url)
      continue
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    try:
      req = Request(url, headers={'User-Agent': user_agent, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
      byte_response = urlopen(req, timeout=100).read()
    except(requests.exceptions.MissingSchema, requests.exceptions.ConnectionError, requests.exceptions.InvalidURL, requests.exceptions.InvalidSchema, urllib.error.HTTPError, urllib.error.URLError):    
      # add broken urls to it’s own set, then continue  
      print("exception occured while requesting url, continuing")  
      broken_urls.add(url)    
      continue
    except socket.timeout:
      print("read operation timed out")
      continue

    response = byte_response.decode('utf-8')
    local_urls = set()
    static_assets = set()

    parts = urlsplit(url)
    base = '{0.netloc}'.format(parts)
    strip_base = base.replace('www.', '')
    base_url = '{0.scheme}://{0.netloc}'.format(parts)
    path = url[:url.rfind("/")+1] if "/"in parts.path else url

    soup = BeautifulSoup(response, "lxml")

    for image in soup.find_all("img"):
        img_url = image.get("src")
        if len(img_url) > 0:
          static_assets.add(img_url)


    for link in soup.find_all("a"):
        anchor = link.attrs["href"] if "href" in link.attrs else ''
        anchor_parts = urlsplit(anchor)
        anchor_base = '{0.netloc}'.format(anchor_parts)
        if anchor_base not in base:
          print('not local url ', anchor_base)
          continue
        elif anchor.startswith("/"):
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
        else:
            continue
    site_map[url] = {"static_assets": static_assets, "links": local_urls}    
    for i in local_urls:
      if not i in new_urls and not i in processed_urls:
        new_urls.append(i)

  site_map_df = pd.DataFrame.from_dict(site_map).T
  site_map_df.to_csv(filename)

if __name__=="__main__":
    createSiteMap("https://sedna.com/")
