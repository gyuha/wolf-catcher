from src.site.SiteBase import SiteBase

@SiteBase.register
class Wfwf(SiteBase):
    def __init__(self, config):
        SiteBase.__init__(self, config)

    @property
    def site_name(self):
        return self.name
    
    def get_chapter_info(self, url:str):
        print('📢[Wfwf.py:13]: ', id)
    
    def get_chapter_list(self, url):
        print('📢[Wfwf.py:14]: ', url)
    
    def get_img_list(self, url):
        print('📢[Wfwf.py:17]: ', url)


