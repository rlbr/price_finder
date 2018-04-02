import urllib
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as BS
import re
import datetime

user_agent = UserAgent().chrome
re_words = lambda n: re.compile(r"( ?[^ ]+ ?)"+"{0,"+str(n-1)+"}"+r"[^ ]+")
debug = None
def get_page(url):
    page = None
    while not page:
        page = urllib.request.Request(url,headers = {"User-Agent":user_agent})
        page = str(urllib.request.urlopen(page).read())
        
    return page

def get_BS(url):
    return BS(get_page(url),"lxml")

class price_finder:
    page_funcs = {
    "www.amazon.com":{
        "name":lambda page: re.sub(r"( {2,}|\n|\\n)","",page.find("span",id="productTitle").text),
        "price":lambda page: page.find(name = "span",id = re.compile("priceblock.*")).text
        },
    "www.banggood.com":{
        "name":lambda page: page.find("h1",attrs = {"itemprop":"name"}).text,
        "price":lambda page: page.find("div",attrs = {"class":"now"}).get("oriprice")
        },
    "www.dalprops.com":{
        "name":lambda page: page.find("h1",attrs = {"class":"product_title"}).text,
        "price":lambda page: page.find("meta",attrs = {"itemprop":"price"}).get("content")
        },
    "www.gearbest.com":{
        "name":lambda page: page.find("div",attrs = {"class":"goods-info-top"}).find("h1").text,
        "price":lambda page: page.find(id="unit_price").get("data-orgp")
        },
    "hobbyking.com":{
        "name":lambda page: page.find("h1",attrs={"class":"product-name"}).text,
        "price":lambda page: page.find("span",id = re.compile(r"product-price.*")).find("span",attrs={"class":"price"}).text
        }
    }
    def __init__(self,url,space_seperated_categories = 7,bs=None):
        self.url=url
        self.info_url = urllib.parse.urlparse(url)
        if self.info_url.netloc not in price_finder.page_funcs.keys():
            raise NotImplementedError("Not implemented for {}".format(self.info_url.netloc))
        if bs:
            self.bs= bs
        else:
            self.bs = get_BS(url)
        self.words = re_words(space_seperated_categories)
        self.time = datetime.datetime.today()
        self.info_product = self._get_product_info_()

            
    def _get_product_info_(self):
        funcs = price_finder.page_funcs[self.info_url.netloc]
        print(self.url)
 
        return {
            "product_name":self.words.match(
                funcs["name"](self.bs)
                ).group(0),
            "price":funcs["price"](self.bs).replace("$",""),
            }
    
