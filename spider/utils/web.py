from urllib.parse import urlparse

def get_base_url(url):
    parsed = urlparse(url)
    base_url = f'{parsed.scheme}://{parsed.netloc}'
    return base_url