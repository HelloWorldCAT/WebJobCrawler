import urlparse
import time
import datetime

class Throttle:
    """Add delay between two scrapy to same domain
    """
    def __init__(self, delay):
        self.delay = delay
        self.domain = {}
    
    def wait(self, url):
        domain = urlparse.urlparse(url).netloc
        lastVisistTime = self.domain.get(domain)
        if self.delay > 0 and lastVisistTime is not None:
            gap = (datetime.datetime.now() - lastVisistTime).seconds
            if self.delay > gap:
                time.sleep(self.delay - gap)
        self.domain[domain] = datetime.datetime.now()