import logging
from typing import List


class Transformer:
    def __init__(self, **kwargs):
        self.logger = logging.getLogger(name="Transformer")
        
    def run(self, urls: List[str]):
        # html을 통해서
        # 매칭되는 이미지, 비디오, 텍스트를 확인하고
        # 이미지, 비디오는 다운로드 후 링크를 가지고 있는다.
        # 그 링크를 html과 대체한다.
        # # 이 때 필요한 text, image, video 태그는 정해져있다. 그러므로 태그대체식을 사용한다.
        # 이게 완료되면 freshness는 프리즈(-1)로 변경된다.
        pass