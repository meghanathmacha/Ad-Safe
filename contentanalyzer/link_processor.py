import expression
import hashlib

from BeautifulSoup import BeautifulSoup
from BeautifulSoup import SoupStrainer

class LinkProcessor:
    def __init__(self, content):
        self.content = content

    def links(self):
        self.links = []

        for link in BeautifulSoup(self.content, parseOnlyThese=SoupStrainer('a')):
            if link.has_key('href'):
                self.links.append(link['href'])

        return self.links

    def canonical_links(self):        
        self.canonical_links = []

        for link in self.links():
            try:
                gen = expression.ExpressionGenerator(link)
                exprs = list(gen.Expressions())
                for e in exprs:
                    self.canonical_links.append(str(e))
            except:
                pass

        return self.canonical_links

    def link_hash(self, links):
        link_array = []

        for l in links:
            link_array.append(hashlib.md5(l).hexdigest())

        return link_array
