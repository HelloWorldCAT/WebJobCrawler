import urlparse
import re
import urllib2
import robotparser

def download(url, userAgent = 'chrome', num_retries = 2):
    print 'Downloading:', url
    headers = {'User-agent': userAgent}
    request = urllib2.Request(url, headers=headers)
    try:
        html = urllib2.urlopen(request).read()
    except urllib2.URLError as e:
        print 'Download error:', e.reason
        html = None
        if num_retries > 0:
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
        else:
            print 'blocked by robots.txt', url


link_crawler('http://example.webscraping.com', '.*/(index|view)')