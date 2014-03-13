__author__ = 'Jurgen'
from BeautifulSoup import BeautifulSoup
import urllib2
import urllib
import mechanize
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def getResults(html):
    soup = BeautifulSoup(html)
    # a flag to decide whether the page has 'a' no pagination
    # 'b' less than 10
    # 'c' more than 10
    pagination = "a"
    rows = soup.findAll("td")
    rows = rows[2:]
    if(rows[1].find('&gt;') != -1):
        print "It has pagination more than 10"
    else:
        print "it is not int"
    for tag in rows:
        print tag.text


def loopCourtTypes(driver):
    element = driver.find_element_by_id("ctl00_ContentPlaceHolderMain_search_introduced_panel_dd_court")
    print element
    all_options = element.find_elements_by_tag_name("option")
    backButton = driver.current_url
    print all_options
    outcounter = 1
    #for option in all_options:
    for x in range(0,5):
        print "Value is: %s" % all_options[outcounter].get_attribute("value")
        all_options[outcounter].click() #click on option
        searchbutton = driver.find_element_by_id("ctl00_ContentPlaceHolderMain_search_introduced_panel_bt_search").click()
        html = driver.page_source #get the html of the site
        getResults(html)
        driver.get(backButton)
        element = driver.find_element_by_id("ctl00_ContentPlaceHolderMain_search_introduced_panel_dd_court")
        all_options = element.find_elements_by_tag_name("option")
        outcounter = outcounter + 1

    #result = driver.find_element_by_id("ctl00_ContentPlaceHolderMain_search_introduced_panel_bt_search").click() # clicks on submit
   # html = driver.page_source #get the html of the site
  #  getResults(html)



#method to get all types of cases in a list(intro,pending, ..)
def getAllCaseTypes(driver):
    #element = driver.find_element_by_class_name("menu")useless
    cTypeList = list() # list to keep cases types links
    x = 0 #will be used as a counter in loop
    html = driver.page_source
    soup = BeautifulSoup(html)
    menu = soup.findAll("div", { "class" : "menu" })#get all menus
    for onemenu in menu:
        #keep the menu that is selected (ie not empty)
        if(onemenu.text != ""):
                menu = onemenu
    #print menu for test
    for ul in menu:
        for li in ul:
            x = x + 1
            if((x == 1) or (x == 2) or (x == 3) or (x == 6)):#keep only required links
                cTypeList.append(li.a["href"])
                print li.a["href"]
    return cTypeList


def selectMenuItem(driver):#method to select civil cases
    html = driver.page_source
    soup = BeautifulSoup(html)
    allLinks = soup.findAll("a")
    for link in allLinks:
        if 'http://www.justiceservices.gov.mt/courtservices/CivilCases/default.aspx' in str(link):
            driver.get("http://www.justiceservices.gov.mt/courtservices/CivilCases/default.aspx")
            return driver
        else:
            continue

def connecttosite():
    driver = webdriver.Chrome()
    driver.get("http://www.justiceservices.gov.mt/courtservices/CivilCases/search.aspx?func=introduced")
    return driver

def mymain():
    driver = connecttosite()
   # driver = selectMenuItem(driver) # driver value is changed to civil cases
   # caseTypeList = getAllCaseTypes(driver)
    loopCourtTypes(driver)


mymain()