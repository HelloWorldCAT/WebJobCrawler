import urlparse
import re
import urllib2
import robotparser

def download(url, userAgent = 'chrome', proxy=None, num_retries = 2):
    print 'Downloading:', url
    headers = {'User-agent': userAgent}
    request = urllib2.Request(url, headers=headers)
    
    opener = urllib2.build_opener()
    # add proxy support
    if proxy:
        proxy_params = {urlparse.urlparse(url).scheme: proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))
        
    try:
        html = opener.open(request).read()
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
        if num_retries > 0:
            #for server error, retry twice by default
            if hasattr(e, 'code') and 500< e.code < 600:
                download(url, userAgent, num_retries-1)
    return html

def get_link(html):
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webpage_regex.findall(html)

def link_crawler(seed_url, link_regex):
    crawlQueue = [seed_url]
    seen = set(crawlQueue)
    rp = robotparser.RobotFileParser()
    rp.set_url(seed_url + '/robots.txt')
    rp.read()
    while crawlQueue:
        url = crawlQueue.pop()
        if rp.can_fetch("", url):
            html = download(url)
            for link in get_link(html):
                if re.match(link_regex, link):
                    link = urlparse.urljoin(seed_url, link)
                    if link not in seen:
                        seen.add(link)
                        crawlQueue.append(link)
                        print link
        else:
            print 'blocked by robots.txt', url


link_crawler('http://example.webscraping.com', '.*/(index|view)')