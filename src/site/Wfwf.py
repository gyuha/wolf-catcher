from util.Config import Config
from util.SeleniumWorker import SeleniumWorker
from src.site.SiteBase import SiteBase
from selenium.webdriver.common.by import By

@SiteBase.register
class Wfwf(SiteBase):
    def __init__(self, seleniumWorker: SeleniumWorker,  config: Config):
        SiteBase.__init__(self, seleniumWorker, config)
    
    def get_chapter_info(self, url:str):
        self.seleniumWorker.get_with_retry(
            url, 
            self.url_format["list"]["visible_condition"]["type"],
            self.url_format["list"]["visible_condition"]["text"]
        )
        browser = self.seleniumWorker.browser
        title = browser.find_element(
            'xpath', 
            "//*[@id=\"content\"]/div[2]/div[3]/h1").text
        print('📢[Wfwf.py:20]: ', title)
        # print('📢[Wfwf.py:18]', self.seleniumWorker.page_source)

    
    def get_chapter_list(self, url):
        print('📢[Wfwf.py:14]: ', url)
    
    def get_img_list(self, url):
        print('📢[Wfwf.py:17]: ', url)


