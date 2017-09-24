import csv
import re
import lxml.html

class ScrapCallback:
    def __init__(self):
        self.writer = csv.writer(open('countries.csv', 'w+'))
        self.fields = ('area', 'population', 'iso', 'country', 'capital'
            , 'continent', 'tld', 'currency_code', 'currency_name', 'phone', 'postal_code_format', 'postal_code_regex', 'languages', 'neighbours')
        self.writer.writerow(self.fields)

    def __call__(self, url, html):
        if re.search('/view/', url):
            try:
                tree = lxml.html.fromstring(html)
                row = []
                for field in self.fields:
                    matchedEle = tree.cssselect('table > tr#places_{}__row > td.w2p_fw'.format(field))
                    if matchedEle:
                        row.append(matchedEle[0].text_content())
                self.writer.writerow(row)
            except Exception as e:
                print html 