import warnings #GetAptUrls() Supresses warning
warnings.filterwarnings('ignore') #GetAptUrls() Supresses warning
from bs4 import BeautifulSoup #GetAptUrls() GetAptInfo(AptUrls)
import requests #GetAptUrls()
import re #GetAptInfo(AptUrls) MakeRentInt(df)
import pandas as pd #Everything
import time #MakeCurrentTimeString()

# from selenium import webdriver
# import time
# from selenium.webdriver.remote.webelement import WebElement
# from selenium.common.exceptions import StaleElementReferenceException

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

# def waitForLoad(driver):
#     elem = driver.find_element_by_tag_name("html")
#     count = 0
#     while True:
#         count += 1
#         if count > 10:
#             #print("Timing out after 10 seconds and returning")
#             return
#         time.sleep(.1)
#         try:
#             elem == driver.find_element_by_tag_name("html")
#         except StaleElementReferenceException:
#             return

def Get_Apt_Info(Apt_Urls, Archive):
    df =[]
    assert len(Apt_Urls) != 0, "Apt_Urls is empty in Get_Apt_Info(Apt_Urls)"
    print(len(Apt_Urls))
    for i in range(0, len(Apt_Urls)):
        try:
            r = requests.get(Apt_Urls[i])
        except:
            continue
        # Write code that counts how many of my batch of Urls turns out to be bad for one reason or another, 0 rows, not 200 HTTTP ode
        if r.status_code != 200:
            continue

        # URL to AptName by rsplit()
        # if Archive == 2:
        #     # print("Archive works")
        #     Date = Apt_Urls[i].rsplit('/')[4]
        #     AptName = Apt_Urls[i].rsplit('/')[8]
        #     driver = webdriver.PhantomJS(executable_path='/usr/local/bin/phantomjs')
        #     driver.get(Apt_Urls[i])
        #     waitForLoad(driver)
        #     html = driver.page_source
        #     soup = BeautifulSoup(html, "lxml")
        #     tab = soup.select('div[data-tab-content-id="all"]')
        #     if len(tab) == 0:
        #         continue
        #     apts = tab[0].select('.rentalGridRow')
        if Archive == 1:
            # print("Archive works")
            Date = Apt_Urls[i].rsplit('/')[4]
            AptName = Apt_Urls[i].rsplit('/')[8]
            soup = BeautifulSoup((r).content, "lxml")
            tab = soup.select('div[data-tab-content-id="all"]')
            if len(tab) == 0:
                continue
            print(i)
            apts = tab[0].select('.rentalGridRow')

        if Archive == 0:
            # print("Archive does not works")
            Date = time.strftime("%Y%m%d-%H%M%S")
            AptName = Apt_Urls[i].rsplit('/')[3]
            soup=BeautifulSoup((r).content, "lxml")
            tab = soup.select('div[data-tab-content-id="all"]')
            if len(tab) == 0:
                continue
            apts = tab[0].select('.rentalGridRow')

        Year = Date[:4]
        Month = Date[4:6]
        a,b,c, d = [], [], [], []
        for apt in apts:
            type = apt.select('.shortText')[0].text.strip()
            rent = apt.select('.rent')[0].text.strip()
            sqft = apt.select('.sqft')[0].text.strip()
            available = apt.select('.available')[0].text.strip()
            a.append(type)
            b.append(rent)
            c.append(sqft)
            d.append(available)

        df_child = pd.DataFrame({'type': a, 'rent': b, 'sqft': c, 'available': d, 'apt': AptName, 'Year': Year, 'Month': Month})
        df.append(df_child)
    assert len(df) != 0, "df is empty in Get_Apt_Info(Apt_Urls)"
    # Creates one data frame from many
    df = pd.concat(df).reset_index(drop=True)
    return df

def Make_Current_Time_String():
    timestr = time.strftime("%Y%m%d-%H%M%S")
    return timestr

def DF_to_Excel(df, path):
    #Pass a dataframe and a string of name for the excel file
    import pandas as pd
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(path, engine='xlsxwriter')
    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Sheet1')
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    return

def main():

    # New
    Hood_choices = ['https://www.apartments.com/belltown-seattle-wa/', 'https://www.apartments.com/midtown-nashville-nashville-tn/']
    Hood_Url = [Hood_choices[1]]
    Apt_Urls_New = Hood_Url_List_to_Apt_Urls(Hood_Url)
    df_live = Get_Apt_Info(Apt_Urls_New, 0)

    # Old
    Hood_Url_Webarchive = 'http://web.archive.org/cdx/search/cdx?url='+ Hood_Url[0]
    Snapshot_Url_List = From_Webarchive_Get_Snapshot(Hood_Url_Webarchive)
    Apt_Urls_Old = Hood_Url_List_to_Apt_Urls(Snapshot_Url_List)
    df_archive = Get_Apt_Info(Apt_Urls_Old, 1)

    # Combine
    df = []
    df.append(df_live)
    df.append(df_archive)
    # Creates one data frame from many
    df = pd.concat(df).reset_index(drop=True)

    Hood_Name = Hood_Url[0].split('/')[3]
    # Export
    timestr = Make_Current_Time_String()
    # If Hood_Name subfolder does not exist, makedir
    import os
    try:
        path = '/Users/Reed/PycharmProjects/akara/apt_get/data/data_unclean/' + Hood_Name + '/' + Hood_Name + "_clean" + timestr + '.xlsx'
        DF_to_Excel(df, path)
    except:
        os.mkdir(path = '/Users/Reed/PycharmProjects/akara/apt_get/data/data_unclean/' + Hood_Name)
        path = '/Users/Reed/PycharmProjects/akara/apt_get/data/data_unclean/' + Hood_Name + '/' + Hood_Name + "_clean" + timestr + '.xlsx'
        DF_to_Excel(df, path)

    return df

df = main()
