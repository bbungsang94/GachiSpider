import time
from urllib.request import Request, urlopen
from urllib.parse import urlparse, urljoin

def get_default_header(**kwargs):
    default_dict =  {'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                     'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
                     'Priority': 'u=0, i',
                     'Sec-Ch-Ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
                     'Sec-Ch-Ua-Mobile': '?0',
                     'Sec-Ch-Ua-Platform': '"Windows"',
                     'Sec-Fetch-Dest': 'document',
                     'Sec-Fetch-Mode': 'navigate',
                     'Sec-Fetch-Site': 'none',
                     'Sec-Fetch-User': '?1',
                     'Upgrade-Insecure-Requests': '1',
                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'}
    
    for key, value in kwargs.items():
        default_dict[key] = value
    
    return default_dict

def get_base_url(url):
    parsed = urlparse(url)
    base_url = f'{parsed.scheme}://{parsed.netloc}'
    return base_url

def get_unwrapped_url(url, agent_name="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"):
    time.sleep(2.0) # for webmaster
    req = Request(url, headers=get_default_header(**{"User-Agent": agent_name}))
    unwrapped_url = None
    try:
        context = urlopen(req)
        if context.status == 200:
            unwrapped_url = context.url
            contents = context.read()
        return contents, unwrapped_url
    
    except Exception as e:
        return None, None
