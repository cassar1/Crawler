__author__ = 'Jurgen'
from BeautifulSoup import BeautifulSoup
import mechanize
from mechanize import Browser
import urllib
import urllib2
import unicodedata
import cookielib

def get_court_values():
    soup2 = BeautifulSoup(browser.response().read())
    court_element = soup2.find("select")
    option_list = list()
    options = court_element.findChildren()
    options = options[1:]
    for option in options:
        print option['value']
        option_list.append(option['value'])
    return option_list

def get_pages():
    soup2 = BeautifulSoup(browser.response().read())
    table = soup2.find("table",{'class': 'gridViewJudgementsResults'})
    rows = table.find("tr")
    if(rows.has_key("class")):
        print "nopaginations"
    else:
        print rows

browser = Browser()
cj = cookielib.LWPCookieJar()
browser.set_cookiejar(cj)
browser.set_handle_equiv(True)
browser.set_handle_gzip(True)
browser.set_handle_redirect(True)
browser.set_handle_referer(True)
browser.set_handle_robots(False)

browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

url = 'http://www.justiceservices.gov.mt/courtservices/Judgements/search.aspx?func=all'
r = browser.open(url)
browser.select_form(nr=0)
court_list = get_court_values()
#for option in court_list:
browser.form['ctl00$ContentPlaceHolderMain$search_judgement_panel$dd_court']= ['126']
browser.submit()#.submit is used to press the submit button on the form
    #print browser.response().read()
pages_list = get_pages()
browser.select_form(nr=0)
browser.form.set_all_readonly(False)
browser.form['__EVENTARGUMENT']= 'Page$5'
browser.form['__EVENTTARGET']= 'ctl00$ContentPlaceHolderMain$result_panel$gv_judgements_results'

soup = BeautifulSoup(browser.response().read())
inputs = soup.findAll('input')

for input in inputs:
    if(input['name'] == '__VIEWSTATE'):
        viewstate = input['value']
    if(input['name'] == '__VIEWSTATEENCRYPTED'):
        viewStateEnc = input['value']
    if(input['name'] == '__EVENTVALIDATION'):
        eventvalid = input['value']


parameters = {'__EVENTARGUMENT' : 'Page$5',
              '__EVENTTARGET' : 'ctl00$ContentPlaceHolderMain$result_panel$gv_judgements_results',
              '__VIEWSTATE' : viewstate,
              '__VIEWSTATEENCRYPTED' : viewStateEnc,
              '__EVENTVALIDATION' : eventvalid
             }
data = urllib.urlencode(parameters)
browser.open(url,data)#open is used to loop through pages, so that the data that we want is passed as param
newpage = browser.response()
#print browser.response().read()


