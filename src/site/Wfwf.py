from src.site.SiteBase import SiteBase

@SiteBase.register
class Wfwf(SiteBase):
    def __init__(self, config):
        SiteBase.__init__(self, config)

    @property
    def site_name(self):
        return self.name

    def get_chapter_list(self, url):
        print('📢[Wfwf.py:14]: ', url)
    
    def get_imgs(self, url):
        print('📢[Wfwf.py:17]: ', url)


