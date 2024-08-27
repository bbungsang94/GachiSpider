import requests
from spider.crawler.matcher.simple import Matcher

response = requests.get("https://www.linkedin.com/robots.txt")
matcher = Matcher(response.text, "googlebot")
print(matcher.allow_by(url="https://www.linkedin.com/company/hot-topic"))
