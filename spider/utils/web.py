from urllib.request import Request, urlopen
from urllib.parse import urlparse

def get_base_url(url):
    parsed = urlparse(url)
    base_url = f'{parsed.scheme}://{parsed.netloc}'
    return base_url

def get_unwrapped_url(url, agent_name="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"):
    req = Request(url, headers={'User-Agent': agent_name})
    unwrapped_url = None
    context = urlopen(req)
    if context.status == 200:
        unwrapped_url = context.url
    
    return context, unwrapped_url