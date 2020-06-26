from dataclasses import dataclass

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webelement import FirefoxWebElement as WebElement
from selenium.common.exceptions import NoSuchElementException


def save(browser, filename):
    from pathlib import Path    
    return Path(filename).write_bytes(browser.page_source.encode("utf-8"))
  

def get_rows(browser):
    return (browser.find_element_by_id("ctl00_cphBody_gvTradeList")
                   .find_elements_by_tag_name("tr"))

def elements(row: WebElement):
    return row.find_elements_by_tag_name("td")

def find_href(x: WebElement):
    try: 
       return x.find_element_by_tag_name("a").get_attribute("href")
    except NoSuchElementException: 
       return ""
  

@dataclass
class Cell:
    text: str
    link: str
    
def split_link(s):
    return s.split('?ID=')[1]


assert split_link('https://bankrot.fedresurs.ru/'
'TradePlaceCard.aspx?ID=9ff54c08-a553-4cb1-adba-37cfdad8dd53') \
    == '9ff54c08-a553-4cb1-adba-37cfdad8dd53'

  
# TODO: через organisation card 
# https://bankrot.fedresurs.ru/OrganizationCard.aspx?ID=7719307CE8C3B0A985341D1EF29291FA
# в список MessageWindow. Получить список MessageWindow

# TODO: разобрать https://bankrot.fedresurs.ru/MessageWindow.aspx?ID=DFCB8224776BE209EA64BF20482E5423
# на лот-цена

options = Options()
options.headless = True

browser = webdriver.Firefox(options=options)
browser.get("https://bankrot.fedresurs.ru/TradeList.aspx")
rows = get_rows(browser)
save(browser, "output.txt")
row = rows[1]    
xs = [Cell(e.text, find_href(e)) for e in elements(row)]
    
    