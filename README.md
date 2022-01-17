# Webscraper
Uses python to parse web pages and create a csv file to depict the links from a given page as well as the static assets present on a page


The python program does the following -

- Implemented a create a site map function
- This takes in a url and initialises a local_urls and static_assets set.
- The processing of the url consists of using the Request from urllib module which deals with url related work and it allows passing of headers as part of the request.
- The urlopen is used to open a url, this returns a byte response, which is then decoded.
- The urlsplit method is used to create a named tuple which divides the url into parts - `<scheme>://<netloc>/<path>;<params>?<query>#<fragment>`
- The network location will be the base url which includes the domain itself (and subdomain if present), the port number.
- Beautiful Soup is a Python library that is used for web scraping purposes to pull the data out of HTML and XML files. This is used to to parse the response.
- The first for loop finds all the static assets for a given url. In this case it retrieves all the images.
- The second for loop finds all the `a` tags and uses the href attribute to find the link. This is used to populate local_urls set after validating that the url is correct. A validator method is written for this use case.
- A dict is used to with key as the url and it consists of static assets and the local links
- Once all the urls are traversed, pandas module is used to convert the dict to a dataframe.
- The dataframe is then converted to csv.

Imports required for this program
- pip install beautifulsoup4
- python -m pip install requests
- pip install pandas
