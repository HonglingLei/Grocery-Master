"""
Name    : pre_process.py
Author  : Hongliang Liu, Jing Li, Hongling Lei, Aishwarya Kura
Contact : See README
Time    : 2021/9/11 15:57
"""

# We didn't use beautifulsoup because our target websites hide their html code with javascript. Instead, we chose selenium to handle this
from tkinter.constants import N, NO
from selenium import webdriver
import os
import re
option = webdriver.ChromeOptions()
option.add_argument('headless') # 设置option


def process_query(query):
    '''
    :param query: String, query from users
    :return: String, replace 'space' with '+',for url scraping
    '''
    q=query.replace(" ","+")
    return q


class chrome():
    '''
    a browser used for scraping
    '''
    def __init__(self,selection):
        if selection == "Y":
            self.driver = webdriver.Chrome()
        else:
            self.driver = webdriver.Chrome(options=option)

    def get_driver(self):
        '''
        :return: a browser
        '''
        return self.driver

    
class Scrapeongo():
    '''
    desc: used for store the item on going and the error
    '''
    def __init__(self) -> None:
        self.onitem = 0
        self.error = None
        self.total_list = []
    
    def push_ongoing(self, label, content):   
        label.configure(text=content)
          
        
class Scrape_TJ(Scrapeongo):
    '''
    desc:used for scraping data from traderjoes
    '''
    def __init__(self):
        '''
        desc:url format like:https://www.traderjoes.com/home/search?q=apple+juice
        '''
        super().__init__()
        self.url_pre = "https://www.traderjoes.com/home/search?q="
        

    def set_chrome(self,driver):
        '''
        desc: set scraper's browser to driver
        :param driver: browser
        :return:
        '''
        self.driver=driver
        
        
    def get_table(self,query,gui):
        '''
        desc:get all product information that is being searching
        :param query: String, product being searching
        :return:
        '''
        # get all item's url that is being searched
        self.get_item_url(query)

        # get all data of item (i forget item name)
        flag=0
       
        for i in self.item_url_list:
            flag+=1
            self.push_ongoing(gui.label2, "Scraping traderjoe's {} item, error: {}".format(flag, None))
            line = {
                    'name': None,
                    'website': 'traderjoe'
                }
            try:
                table = self.get_item_table(i)
                line['name'] = self.driver.find_element_by_xpath('//h2[@class="ProductDetails_main__title__14Cnm"]').text
                head = list(table.values())[1]
                Facts = list(table.values())[2]
                Facts_2 = list(table.values())[3]
                
                for index,headname in enumerate(head):
                    if headname:
                        line[headname] = [Facts[index] if Facts[index] else 'NULL', Facts_2[index] if Facts_2[index] else 'NULL']

                self.total_list.append(line)
                #以{营养名称: [含量, 百分比]}形式储存
            except Exception as e:
                self.total_list.append(line)
                self.push_ongoing(gui.label2, "Scraping traderjoe's {} item, error: {}".format(flag, e))

                
    def get_html(self,url):
        '''
        desc: let the browser scraping url
        :param url: String, item url
        :return:
        '''
        self.driver.get(url)

        
    def get_item_url(self,query):
        '''
        desc: get all the url of items that are being scraped
        :param query: String, searched items
        :return:
        '''      
        # get searching url
        url=self.url_pre+process_query(query)

        # get items url list
        self.item_url_list=[]
        self.get_html(url)
        self.driver.implicitly_wait(20)
        mid=self.driver.find_elements_by_xpath("//a[@class='Link_link__1AZfr SearchResultCard_searchResultCard__titleLink__2nz6x']")
        if mid:
            for i in mid:
                self.item_url_list.append(i.get_attribute("href"))
        self.item_url_list = self.item_url_list[0:3]


    def get_item_table(self,url):
        '''
        desc: get all nutrition data of item from its url
        :param url: product's url which is being scraping
        :return: table, dictionary, nutrition data of
        '''
        self.get_html(url)
        self.driver.implicitly_wait(20)
        table={}

        # scrape head of the table
        head = self.driver.find_elements_by_xpath("//div[@class='Item_characteristics__3rZUg']")
        table['heads']=head

        # scrape table content
        i=0
        flag=True
        while(flag):
            i += 1
            column=self.driver.find_elements_by_xpath("//td["+str(i)+"]")
            if column:
                list = []
                for j in range(len(column)):
                    list.append(column[j].text)
                table[column[0]] = list
            else:
                flag=False
        return table


class Scrape_walmart(Scrapeongo):
    '''
    desc:used for scraping data from walmart
    '''
    def __init__(self):
        '''
        desc:url format like:https://www.walmart.com/search?q=apple+juice
        '''
        super().__init__()
        self.url_pre = "https://www.walmart.com/search?q="

        
    def set_chrome(self, driver):
        '''
        desc: set scraper's browser to driver
        :param driver: browser
        :return:
        '''
        self.driver = driver

        
    def get_table(self, query, gui):
        '''
        desc:get all product information that is being searching
        :param query: String, product being searching
        :return:
        '''

        # get all item's url that is being searched
        self.get_item_url(query)

        # get all data of item (i forget item name)
        self.item = []
        flag=0
        for i in self.item_url_list:
            
            flag+=1
            self.push_ongoing(gui.label3, "Scraping walmart {} item, error: {}".format(flag, None))
            lines = {
                'name': None,
                'website': 'walmart'
            }
            
            try:
                table = self.get_item_table(i)
                lines['name'] = self.driver.find_element_by_xpath('//h1[@class="f3 b lh-copy dark-gray mt1 mb2"]').text
                for index, line in enumerate(table):
                    result = re.findall(r'[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)', line)
                    if len(result)==2: #参数存在
                        k = result[0][0]
                        if '{}g'.format(k) in line:
                            k = '{}g'.format(k)
                        elif '{}mg'.format(k) in line:
                            k = '{}mg'.format(k)
                        else:
                            k = '{}mcg'.format(k)
                        loc = '{}%'.format(result[1][0])
                        name = line.replace(k,'').replace(loc, '').strip()
                        lines[name] = [k, loc]
                self.total_list.append(lines)
                
            except Exception as e:
                self.total_list.append(lines)
                self.push_ongoing(gui.label3, "Scraping walmart {} item, error: {}".format(flag, e))
          

    def get_html(self, url):
        '''
        desc: let the browser scraping url
        :param url: String, item url
        :return:
        '''
        self.driver.get(url)

        
    def get_item_url(self, query):
        '''
        desc: get all the url of items that are being scraped
        :param query: String, searched items
        :return:
        '''
        # get searching url
        url = self.url_pre + process_query(query)

        # get items url list
        self.item_url_list = []
        self.get_html(url)
        self.driver.implicitly_wait(40)

        mid = self.driver.find_elements_by_xpath("//a[@class='absolute w-100 h-100 z-1']")
        if mid:
            for i in mid:
                self.item_url_list.append(i.get_attribute("href"))


    def get_item_table(self, url):
        '''
        desc: get all nutrition data of item from its url
        :param url: product's url which is being scraping
        :return: table, dictionary, nutrition data of
        '''
        self.get_html(url)
        self.driver.implicitly_wait(20)
        table = []

        # scrape table content        
        t = self.driver.find_elements_by_xpath("//table")
        if t:
            table=t[0].text.split("\n")
        return table


class Scrape_target(Scrapeongo):
    '''
    desc:used for scraping data from target
    '''
    def __init__(self):
        '''
        desc:url format like:https://www.target.com/s?searchTerm=apple+juice
        '''
        super().__init__()
        self.url_pre = "https://www.target.com/s?searchTerm="

        
    def set_chrome(self,driver):
        '''
        desc: set scraper's browser to driver
        :param driver: browser
        :return:
        '''
        self.driver=driver
        
        
    def get_table(self,query, gui):
        '''
        desc:get all product information that is being searching
        :param query: String, product being searching
        :return:
        '''
        # get all item's url that is being searched
        self.get_item_url(query)
        print(self.item_url_list)
        # get all data of item (i forget item name)
        self.item=[]
        flag=0
        lines = {
                'name': None,
                'website': 'target'
            }
        for index, i in enumerate(self.item_url_list):
            flag+=1
            self.push_ongoing(gui.label4, "Scraping target {} item, error: {}".format(flag, None))
            try:
                table = self.get_item_table(i)
                lines['name'] = self.driver.find_element_by_xpath('//h1[@class="Heading__StyledHeading-sc-1mp23s9-0 dkHWUj h-margin-b-none h-margin-b-tiny h-text-bold"]//span').text
                for index, line in enumerate(table):
                    result = re.findall(r'[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)', line)
                    if result:
                        if '{}g'.format(result[0][0]) in line:
                            k = '{}g'.format(result[0][0])
                        elif '{}mg'.format(result[0][0]) in line:
                            k = '{}mg'.format(result[0][0])
                        elif '{}mcg'.format(result[0][0]) in line:
                            k = '{}mcg'.format(result[0][0])
                        else:
                            k = None
                        
                        try:
                            if '%' in table[index+1]:
                                loc = table[index+1]
                            else:
                                loc = None
                        except Exception:
                            loc = None
                            
                        if k:
                            name = line.replace(k, '')
                            lines[name] = [k, loc]
                self.total_list.append(lines)

            except Exception as e:
                self.total_list.append(lines)
                self.push_ongoing(gui.label4, "Scraping target {} item, error: {}".format(flag, e))
                pass

            
    def get_html(self,url):
        '''
        desc: let the browser scraping url

        :param url: String, item url
        :return:
        '''
        self.driver.get(url)

        
    def get_item_url(self,query):
        '''
        desc: get all the url of items that are being scraped
        :param query: String, searched items
        :return:
        '''
        # get searching url
        url=self.url_pre+process_query(query)

        # get items url list
        self.item_url_list=[]
        self.get_html(url)
        self.driver.implicitly_wait(20)
        mid=self.driver.find_elements_by_xpath("//a[@class='Link__StyledLink-sc-4b9qcv-0 styles__StyledTitleLink-h3r0um-1 iBIqkb rwewC h-display-block h-text-bold h-text-bs']")
        if mid:
            for i in mid:
                self.item_url_list.append(i.get_attribute("href"))


    def get_item_table(self,url):
        '''
        desc: get all nutrition data of item from its url
        :param url: product's url which is being scraping
        :return: table, dictionary, nutrition data of
        '''
        self.get_html(url)
        self.driver.implicitly_wait(20)
        table=[]

        # scrape table content
        button = self.driver.find_elements_by_xpath("//*[@id=\"tab-Labelinfo\"]/div")
        self.driver.execute_script("arguments[0].click();",button[0])
        t=self.driver.find_elements_by_xpath("//div[@class='styles__DailyValues-sc-10lpfph-1 czsSkr']")
        if t:
            table=t[0].text.split("\n")

        return table

#***************** test code *******************

# print("what do you want to buy?")
# print("do you want to turn on the browser?")
# print("if you open the browser, you will see the website you are scpraping, but this")
# print("process is much slower.")
# print("if you do not open the browser, this process will be faster but, you can not handle")
# print("exceptions like verification, and you will not see the website you are scraping.")
# print("we will handle the automatic verification problem in future version.")
# print("Y/N")
# driver = browser.get_driver()

# print("start processing...")
# #this is where we store information from every website
# total_list=[]

# test.set_chrome(driver)
# result=test.get_table(test_case)
# list_TJ=[]
# for i in test.item:
#     list_TJ.append(i)
# total_list.append(list_TJ)

# test=Scrape_walmart()
# test.set_chrome(driver)
# result=test.get_table(test_case)
# list_walmart=[]
# for i in test.item:
#     list_walmart.append(i)
# total_list.append(list_walmart)

# test=Scrape_target()
# test.set_chrome(driver)
# result=test.get_table(test_case)
# list_target=[]
# for i in test.item:
#     list_target.append(i)
# total_list.append(list_target)
# print("scraping finished!")
# print(total_list)


#***************** test code *******************

# class scrape_B():
#     def __init__(self):
#
# class scrape_C():
#     def __init__(self):
