from selenium import webdriver
from bs4 import BeautifulSoup
import winsound
import time

class BrowserCheck:
    def __init__(self,app,url,size):
        self.application = app
        self.browser = None
        self.setupBrowser()
        self.url = url
        self.size = size

    def setupBrowser(self):
        if self.application == 'chrome':
            #set webbrowser options
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--mute-audio")
            #open website
            self.browser = webdriver.Chrome(chrome_options=chrome_options, executable_path='./chromedriver.exe')
        elif self.application == 'firefox':
            #set webbrowser options
            profile = webdriver.FirefoxProfile()
            profile.set_preference("media.volume_scale", "0.0")
            profile.set_preference('browser.download.folderList', 2) # custom location
            profile.set_preference('browser.download.manager.showWhenStarting', False)
            profile.set_preference('browser.download.dir', './data/')
            profile.set_preference('browser.helperApps.neverAsk.saveToDisk', "image/png,image/jpeg")
            #open website
            self.browser = webdriver.Firefox(firefox_profile=profile, executable_path='./geckodriver.exe')
        return None

    def test4size(self):
        #get web data
        self.browser.get(self.url)
        source_data = self.browser.page_source
        page_source = BeautifulSoup(source_data,features="lxml")
        
        #search for entry, test if product available
        tags = page_source.find('label',text=self.size)
        if tags!= None:
            tags = str( tags.previousSibling )
            print(time.ctime(time.time()),end=" - ")
            if "disabled=" not in tags:
                print('available')
                for k in range(10):
                    winsound.PlaySound(r'air_horn.wav', winsound.SND_FILENAME)
                    #winsound.Beep(440,500)
                    #winsound.PlaySound(None, winsound.SND_PURGE)
            else:
                print('sold out')
        else:
            print('unavailable')
        return None

    def quit(self):
        self.browser.quit()
        return None

if __name__ == "__main__":

    app='firefox' #'chrome'
    url="https://www.nike.com/de/t/zoomx-dragoy-laufspike-fkGKx0" #url to product
    size='EU 45' #shoe size
    Tperiod = 300 # waiting time in seconds before recheck
    ItemCheck = BrowserCheck(app,url,size)

    loop_forever = True
    while loop_forever:
        
        ItemCheck.test4size()

        try:
            time.sleep(Tperiod)
        except KeyboardInterrupt:
            ItemCheck.quit()
            loop_forever = False
