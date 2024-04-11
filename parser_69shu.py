#!/usr/bin/python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import time

service = Service(ChromeDriverManager().install())
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

class Shu69Parser():
    def __init__(self, url) -> None:
        self.url = url
        self.configurations()
        self.driver = webdriver.Chrome(options=chrome_options, service=service)
        self.driver.get(self.url)
        
    def configurations(self):
        self.xpath_parent = '/html/body/div[3]/ul/li/div/div[4]/ul'
        self.pages_xpath = '//*[@id="pagelink"]'
        self.list_content_id = 'article_list_content'
        self.infor_topics = {}
    
    def parser_mainpage(self):
        search = self.driver.find_element(by=By.XPATH, value=self.xpath_parent)
        sub_elements = search.find_elements(by=By.TAG_NAME, value="a")
        
        self.infor_topics['0'] = {}
        self.infor_topics['0']['url'] = str(self.url)
        self.infor_topics['0']['total'] = str(len(sub_elements))
        for idx, s in enumerate(sub_elements):
            self.infor_topics[f'{idx+1}'] = {}
            self.infor_topics[f'{idx+1}']['name'] = s.text
            self.infor_topics[f'{idx+1}']['link'] = s.get_attribute('href')
        
        # todo: store topics information
        for i in range(1, int(self.infor_topics['0']['total'])):
            topic = self.infor_topics[f'{i}']
            self.parser_topic(topic)
            time.sleep(1)

    def parser_topic(self, infor_topic):
        tdriver = webdriver.Chrome(options=chrome_options, service=service)
        tdriver.get(infor_topic['link'])
        npages = tdriver.find_elements(by=By.CLASS_NAME, value='pagelink')
        max_page = npages[-1].text.split('\n')[-1]
        for i in range(1, int(max_page)):
            page_url = infor_topic['link'] + f'/{i}/'
            self.parse_page(page_url=page_url)
            time.sleep(1)
    
    def parse_page(self, page_url):
        pdriver = webdriver.Chrome(options=chrome_options, service=service)
        pdriver.get(page_url)
        el = pdriver.find_element(by=By.ID, value=self.list_content_id)
        ct = el.find_elements(by=By.CSS_SELECTOR, value='li')
        total = len(ct)
        for t in range(total):
            c = ct[t]
            self.parse_content(c)
            time.sleep(.5)
            
    def parse_content(self, c):
        lurl = c.find_element(by=By.TAG_NAME, value='a').get_attribute('href')
        lsrc = c.find_element(by=By.TAG_NAME, value='a').find_element(by=By.TAG_NAME, value='img').get_attribute('data-src')
        ltxts = c.find_element(by=By.CLASS_NAME, value='newnav').text.split('\n')
        lnme, ltyp, ldet = ltxts[0], ltxts[2], ltxts[4]
        # print(lurl[:-4])
        # print(lsrc)
        print(lnme)
        # print(ltyp)
        # print(ldet)
        tic = time.time()
        self.parse_novel(lurl[:-4] + '/')
        toc = time.time()
        print('===========', toc - tic)

    def parse_novel(self, nurl):
        ndriver = webdriver.Chrome(options=chrome_options, service=service)
        ndriver.get(nurl)
        search = ndriver.find_element(by=By.XPATH,value='//*[@id="catalog"]/ul')
        sub_elements = search.find_elements(by=By.TAG_NAME, value="a")

        sdriver = webdriver.Chrome(options=chrome_options, service=service) 
        for idx, se in enumerate(sub_elements):
            tic = time.time()
            nchapter = idx + 1
            # print(se.get_attribute('href'), se.text)
            slink = se.get_attribute('href')
            sdriver.get(slink)
            # time.sleep(.5)
            scontent = sdriver.find_elements(by=By.CLASS_NAME, value='txtnav') 
            # print('$$$$$$$$$$$$$$$$$$$$$$$$$')
            txt = scontent[0].text.replace('\n', '')
            # print(nchapter)
            # print(txt)
            print(time.time() - tic)
            time.sleep(.5)

# if __name__ == 'main':
url = 'https://www.69shu.pro/'
parser = Shu69Parser(url=url)
parser.parser_mainpage()