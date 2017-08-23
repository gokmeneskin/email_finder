from selenium import webdriver


global driver
driver = webdriver.Chrome()

def dont_render_images():
    global driver
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images":2}
    chromeOptions.add_experimental_option("prefs",prefs)
    driver.quit()
    driver = webdriver.Chrome(chrome_options=chromeOptions)


def render(url):
    driver.get(url)
    return driver.page_source

def quit():
    driver.quit()

# import sys
# from PyQt4.QtGui import QApplication
# from PyQt4.QtCore import QUrl
# from PyQt4.QtWebKit import QWebPage
# import requests

# class Client(QWebPage):
#     def __init__(self, url):
#         self.app = QApplication(sys.argv)
#         QWebPage.__init__(self)
#         self.loadFinished.connect(self.on_page_load)
#         self.mainFrame().load(QUrl(url))
#         self.app.exec_()
    
#     def on_page_load(self):
#         self.app.quit()


# def render(url):
#     client_response = Client(url)
#     # client_response.quit()
#     return client_response.mainFrame().toHtml().encode('utf-8')

# # source_html = requests.get('http://www.marsalatextile.com/iletisim').text.encode('utf-8')
# # print(render('http://www.marsalatextile.com/iletisim'))

# import sys
# from PyQt4.QtCore import *
# from PyQt4.QtGui import *
# from PyQt4.QtWebKit import *

# class Render(QWebPage):  
#   def __init__(self, urls, cb):
#     self.app = QApplication(sys.argv)  
#     QWebPage.__init__(self)
#     self.settings().setAttribute(QWebSettings.AutoLoadImages, False)
#     self.settings().setAttribute(QWebSettings.PluginsEnabled, False)
#     self.loadFinished.connect(self._loadFinished)  
#     self.urls = urls  
#     self.cb = cb
#     self.crawl()  
#     self.app.exec_()  
      
#   def crawl(self):  
#     if self.urls:  
#       url = self.urls.pop(0)  
#       print('Downloading', url)
#       self.mainFrame().load(QUrl(url))  
#     else:  
#       self.app.quit()  
        
#   def _loadFinished(self, result):  
#     frame = self.mainFrame()  
#     url = str(frame.url().toString())  
#     html = frame.toHtml()  
#     self.cb(url, html)
#     self.crawl()  


# def scrape(url, html):
#     pass # add scraping code here


# urls = ['http://www.marsalatextile.com/', 'http://www.marsalatextile.com/iletisim']  
# r = Render(urls, cb=scrape)