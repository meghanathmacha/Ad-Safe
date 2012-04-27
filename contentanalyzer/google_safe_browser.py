from link_processor import LinkProcessor
import redis

class GoogleSafeBrowser:
    def __init__(self, content, redis_host='localhost', redis_port=6379):
        self.links = self.genhash(content)
        self.redis_host = redis_host
        self.redis_port = redis_port

    def malware(self):        
        malware = False
        client = redis.Redis(host=self.redis_host, port=self.redis_port)
        for h in self.links:
            if client.sismember('goog-malware-hash', h):
                malware = True
        return malware

    def phishing(self):
        phishing = False
        client = redis.Redis(host=self.redis_host, port=self.redis_port)
        for h in self.links:
            if client.sismember('goog-black-hash', h):
                phishing = True
        return phishing

    def genhash(self, content):
        processor = LinkProcessor(content)
        canonical_links = processor.canonical_links()
        return processor.link_hash(canonical_links)
