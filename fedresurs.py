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


def get_table(browser):
    return (browser.find_element_by_id("ctl00_cphBody_gvMessages")
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

def to_cells(row):
    return [Cell(e.text, find_href(e)) for e in elements(row)]

def pick_org(row):
    return to_cells(row)[4]
  

options = Options()
options.headless = True
browser = webdriver.Firefox(options=options)

if True:
    browser.get("https://bankrot.fedresurs.ru/TradeList.aspx")
    rows = get_rows(browser)
    save(browser, "output.txt")
    row = rows[1]    
    xs = [Cell(e.text, find_href(e)) for e in elements(row)]
    org = pick_org(row)
    print(org)
    print()

if True:
    browser.get('https://bankrot.fedresurs.ru/PrivatePersonCard.aspx?ID=CD47D44AAED1E028B004C4306C11B836')
    table=[to_cells(row) for row in get_table(browser)]
    for t in table:    
        if t and t[1].text == 'Объявление о проведении торгов':
            print (t)
    print()


if True:        
    browser.get("https://bankrot.fedresurs.ru/MessageWindow.aspx?ID=D536249DB6DDF368E904BDD916D413BB")
    ys = [to_cells(tr) for tr in browser.find_element_by_class_name("lotInfo").find_elements_by_tag_name("tr")]
    what, price = ys[1][1:3]
    print(what, price)
    print()    
