import warnings #GetAptUrls() Supresses warning
warnings.filterwarnings('ignore') #GetAptUrls() Supresses warning
from bs4 import BeautifulSoup #GetAptUrls() GetAptInfo(AptUrls)
import requests #GetAptUrls()
import re #GetAptInfo(AptUrls) MakeRentInt(df)
import pandas as pd #Everything
import time #MakeCurrentTimeString()

def Hood_Url_List_to_Apt_Urls(Hood_Url_List):
    Apt_Urls = []
    for i in range(0,len(Hood_Url_List)):
        OldUrl = Hood_Url_List[i]
        Oldsoup=BeautifulSoup(requests.get(OldUrl).content, "lxml")
        ArchiveHrefs = Oldsoup.select('a.placardTitle.js-placardTitle')
        if len(ArchiveHrefs) == 0:
            ArchiveHrefs = Oldsoup.select('a.placardTitle')
        #Each href for each separate ArchiveHref
        for j in range(0, len(ArchiveHrefs)):
            Current_href = ArchiveHrefs[j]['href']
            #Don't forget that this append must be outside the loop, or else we're just adding the last one
            Apt_Urls.append(Current_href)
    assert len(Apt_Urls) != 0, "Apt_Urls is empty in Snapshot_Url_List_to_Archive_Apt_Urls"
    return Apt_Urls


def From_Webarchive_Get_Snapshot(HoodUrl):
    # https://hackernoon.com/guide-to-handling-internet-archives-cdx-server-api-response-c469df5b81f4
    # This article lays out the method for this function
    class Snapshot(dict):
        def __init__(self, urlkey=None, timestamp=None, original=None, mimetype=None, statuscode=None, digest=None,
                     length=None):
            super(Snapshot, self).__init__()
            self['urlkey'] = urlkey
            self['timestamp'] = timestamp
            self['original'] = original
            self['mimetype'] = mimetype
            self['statuscode'] = statuscode
            self['digest'] = digest
            self['length'] = length
            self['snapshot_url'] = 'http://web.archive.org/web/%s/%s/' % (timestamp, original)

    res = requests.get(HoodUrl)
    snapshots = res.text.split('\n')
    snapshot_list = []
    for snapshot in snapshots:
        snapshot_items = snapshot.split(' ')
        if len(snapshot_items) == 7:
            snap = Snapshot(snapshot_items[0], snapshot_items[1], snapshot_items[2], snapshot_items[3],
                            snapshot_items[4], snapshot_items[5], snapshot_items[6])
            snapshot_list.append(snap)
            # print(len(snapshot_list))
    # print(snapshot_list[0]['snapshot_url'])
    # len returns 0 even though there is content
    assert len(snapshot_list) != 0, "snapshot_list is empty in From_Webarchive_Get_Snapshot()"
    # Snapshot Urls to list
    Snapshot_Url_List = []
    for i in range(0, len(snapshot_list)):
        if snapshot_list[i]['statuscode'] == '200':
            # print('Got here')
            Current_Snapshot_Url = snapshot_list[i]['snapshot_url']
            # print(Current_Snapshot_Url)
            Snapshot_Url_List.append(Current_Snapshot_Url)

    # set() gets unique values from my list, list() converts back to a list object
    Snapshot_Url_List = list(set(Snapshot_Url_List))
    assert len(Snapshot_Url_List) != 0, "Snapshot_Url_List is empty in From_Webarchive_Get_Snapshot()"
    return Snapshot_Url_List


def From_Webarchive_Get_Snapshot(HoodUrl):
    # https://hackernoon.com/guide-to-handling-internet-archives-cdx-server-api-response-c469df5b81f4
    # This article lays out the method for this function
    class Snapshot(dict):
        def __init__(self, urlkey=None, timestamp=None, original=None, mimetype=None, statuscode=None, digest=None,
                     length=None):
            super(Snapshot, self).__init__()
            self['urlkey'] = urlkey
            self['timestamp'] = timestamp
            self['original'] = original
            self['mimetype'] = mimetype
            self['statuscode'] = statuscode
            self['digest'] = digest
            self['length'] = length
            self['snapshot_url'] = 'http://web.archive.org/web/%s/%s/' % (timestamp, original)

    res = requests.get(HoodUrl)
    snapshots = res.text.split('\n')
    snapshot_list = []
    for snapshot in snapshots:
        snapshot_items = snapshot.split(' ')
        if len(snapshot_items) == 7:
            snap = Snapshot(snapshot_items[0], snapshot_items[1], snapshot_items[2], snapshot_items[3],
                            snapshot_items[4], snapshot_items[5], snapshot_items[6])
            snapshot_list.append(snap)
            # print(len(snapshot_list))
    # print(snapshot_list[0]['snapshot_url'])
    # len returns 0 even though there is content
    assert len(snapshot_list) != 0, "snapshot_list is empty in From_Webarchive_Get_Snapshot()"
    # Snapshot Urls to list
    Snapshot_Url_List = []
    for i in range(0, len(snapshot_list)):
        if snapshot_list[i]['statuscode'] == '200':
            # print('Got here')
            Current_Snapshot_Url = snapshot_list[i]['snapshot_url']
            # print(Current_Snapshot_Url)
            Snapshot_Url_List.append(Current_Snapshot_Url)

    # set() gets unique values from my list, list() converts back to a list object
    Snapshot_Url_List = list(set(Snapshot_Url_List))
    assert len(Snapshot_Url_List) != 0, "Snapshot_Url_List is empty in From_Webarchive_Get_Snapshot()"
    return Snapshot_Url_List

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException

def waitForLoad(driver):
    elem = driver.find_element_by_tag_name("html")
    count = 0
    while True:
        count += 1
        if count > 10:
            #print("Timing out after 10 seconds and returning")
            return
        time.sleep(.1)
        try:
            elem == driver.find_element_by_tag_name("html")
        except StaleElementReferenceException:
            return

def Get_Apt_Info(Apt_Urls, Archive):
    df =[]
    assert len(Apt_Urls) != 0, "Apt_Urls is empty in Get_Apt_Info(Apt_Urls)"
    for i in range(0, len(Apt_Urls)):
        print(i)
        try:
            r = requests.get(Apt_Urls[i])
        except:
            continue
        print(r.status_code)
        #Write code that counts how many of my batch of Urls turns out to be bad for one reason or another, 0 rows, not 200 HTTTP ode
        if r.status_code != 200:
            continue
        #URL to AptName by rsplit()
        #HARDCODE: Pull Date
        if Archive == 1:
            #print("Archive works")
            Date = Apt_Urls[i].rsplit('/')[4]
            AptName = Apt_Urls[i].rsplit('/')[8]
            driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs')
            driver.get(Apt_Urls[i])
            waitForLoad(driver)
            html = driver.page_source
            soup = BeautifulSoup(html, "lxml")
            rows = soup.select('tr.rentalGridRow')
            if len(rows) == 0:
                continue
        if Archive == 0:
            #print("Archive does not works")
            Date = time.strftime("%Y%m%d-%H%M%S")
            AptName = Apt_Urls[i].rsplit('/')[3]
            soup=BeautifulSoup((r).content, "lxml")
            rows = soup.select('tr.rentalGridRow')
            if len(rows) == 0:
                continue
        Year = Date[:4]
        Month = Date[4:6]
        a,b,c = [], [], []
        #Uses the findChildren method to move through a page
        count = 0
        #This continue says, once I get back to the first Apt don't loop through again
        for j in range(0,len(rows)):
            if rows[j].get('data-rentalkey') == None:
                continue
            if rows[j].get('data-rentalkey') == rows[0].get('data-rentalkey'):
                count+=1
            if count >= 2:
                continue
            current_type = rows[j].findChildren()[0].findChildren()[0].text.strip()
            current_rent = rows[j].findChildren()[8].text.strip()
            current_sqft = rows[j].findChildren()[11].text.strip()
            #current_sqft_numberonly = int(re.sub("[^0-9]", "", current_sqft))
            a.append(current_type)
            b.append(current_rent)
            c.append(current_sqft)
        #Adds each df to a list of dfs
        df_child = pd.DataFrame({'type': a, 'rent': b, 'sqft': c, 'apt': AptName, 'Year': Year,'Month':Month})
        df.append(df_child)
    assert len(df) != 0, "df is empty in Get_Apt_Info(Apt_Urls)"
    #Creates one data frame from many
    df = pd.concat(df).reset_index(drop=True)
    return df



def main():
    Hood_Url = ['https://www.apartments.com/roseville-ca/']
    #Apt_Urls_New = Hood_Url_List_to_Apt_Urls(Hood_Url)
    #df_live = Get_Apt_Info(Apt_Urls_New, 0)
    Hood_Url_Webarchive = 'http://web.archive.org/cdx/search/cdx?url='+ Hood_Url[0]
    Snapshot_Url_List = From_Webarchive_Get_Snapshot(Hood_Url_Webarchive)
    #Apt_Urls_Old = Hood_Url_List_to_Apt_Urls(Snapshot_Url_List)
    #df_archive = Get_Apt_Info(Apt_Urls_Old, 1)
    #df = []
    #df.append(df_live)
    #df.append(df_archive)
    #Creates one data frame from many
    #df = pd.concat(df).reset_index(drop=True)
#     timestr = Make_Current_Time_String()
#     #Exports to Excel, Time is current run time, not when the apartments are from
#     DF_to_Excel(df, 'Denver'+timestr)
    return Snapshot_Url_List

Snapshot_Url_List = main()

print(Snapshot_Url_List)