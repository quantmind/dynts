try:
    from urllib2 import urlopen, ProxyHandler, build_opener
except ImportError:
    from urllib.request import urlopen, ProxyHandler, build_opener
    
class HttpClientFallback:
    
    def __init__(self):
        from dynts.conf import settings
        self.opener = build_opener(ProxyHandler(settings.proxies))
        
    def get(self, url):
        res = self.opener.request(url)
        return res
    
    
def http_client():
    try:
        from pulsar.utils.httpurl import HttpClient
    except:
        HttpClient = HttpClientFallback
    return HttpClient()
    