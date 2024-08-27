from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as bs


def main(url):
    req = Request(url, headers={'User-Agent': "googling bot"})
    context = urlopen(req)
    soup = bs(context.read(), 'html.parser')
    #div_content h3.post_subject
    result = soup.select("h3.post_subject")
    pass

if __name__ == "__main__":
    main("https://www.ppomppu.co.kr/zboard/view.php?id=freeboard&no=8925278")