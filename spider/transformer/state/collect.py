import os
import uuid
from datetime import datetime
from spider.structure import Node, State
from spider.utils.web import download_media
from .format import Format
from .failed import Failed


class Collect(State):
    def __init__(self, node: Node, parent):
        super(Collect, self).__init__("collect", node=node, parent=parent)
        self.save_root = "/tmp/"
        self.bridge_directory = datetime.today().strftime("%Y/%m/%d")
        
    def run(self):
        self.node.cache = dict()
        data = self.node.data
        self.logger.info("Check media files in %s" % self.node.url)     
        for key, contents in data.items():
            self.logger.info("Try to download %s" % key)
            file_root = os.path.join(self.save_root, key, self.bridge_directory)
            self.node.cache[key] = dict()
            if os.path.exists(file_root) == False:
                os.makedirs(file_root)
            for content in contents:
                if 'attrs' in content and 'src' in content['attrs']:
                    self.logger.info("Detected media source: %s" % content['attrs']['src'])
                    filename = str(uuid.uuid1())
                    if key == "images":
                        if ".gif" in content['attrs']['src']:
                            filename += ".gif"
                        else:
                            filename += ".jpg"
                    elif key == "videos":
                        filename += ".mp4"
                    else:
                        self.logger.warning("Unrecognized file format")
                        continue
                    
                    try:       
                        self.logger.info("Request media source")
                        full_path = os.path.join(file_root, filename)
                        self.node.cache[key][content['attrs']['src']] = download_media(url=content['attrs']['src'], save_path=full_path)
                        if self.node.cache[key][content['attrs']['src']] == None:
                            raise RuntimeError
                        self.logger.info("Media source downloaded, saved to %s" % full_path)
                    except Exception as e:
                        self.logger.warning("Failed download file(%s) \n reason: %s" % (content['attrs']['src'], e))
                        self.node.cache[key][content['attrs']['src']] = None
                        self.node.label = "Download failed"
                        self.parent.transit(Failed(node=self.node, parent=self.parent))
                        return
            
            self.node.label = "Saved contents into S3"
            self.parent.transit(Format(node=self.node, parent=self.parent))
        
    def pause(self):
        pass
    
    def stop(self):
        pass
    