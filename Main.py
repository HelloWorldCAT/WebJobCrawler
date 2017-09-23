import urlparse
import re
import urllib2
import robotparser
import Throttle

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


def normalize(seed_url, link):
    """Normalize this URL by removing hash and adding domain
    """
    link, _ = urlparse.urldefrag(link) # remove hash to avoid duplicates
    return urlparse.urljoin(seed_url, link)

def link_crawler(seed_url, link_regex, delay=5, max_depth=2):
    throttle = Throttle.Throttle(delay)
    crawlQueue = [seed_url]
    #avoid scrap trap
    seen = {seed_url: 0}
    rp = robotparser.RobotFileParser()
    rp.set_url(seed_url + '/robots.txt')
    rp.read()
    while crawlQueue:
        url = crawlQueue.pop()
        if rp.can_fetch("", url):
            throttle.wait(url)
            html = download(url)

            depth = seen[url]
            if depth < max_depth:
                for link in get_link(html):
                    if re.match(link_regex, link):
                        link = normalize(seed_url, link)
                        if link not in seen:
                            seen[link] = depth + 1
                            crawlQueue.append(link)
                            print link
        else:
            print 'blocked by robots.txt', url


link_crawler('http://example.webscraping.com', '.*/(index|view)')