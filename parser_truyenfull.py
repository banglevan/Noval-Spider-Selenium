#!/usr/bin/python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import sys

import time
import os
import asyncio
import edge_tts

service = Service(ChromeDriverManager().install())
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

def check_exists_by_xpath(drv, xpath):
    try:
        drv.find_element(by=By.XPATH, value=xpath)
    except NoSuchElementException:
        return False
    return True

def parser_chapter_truyenfull(chap_url):
    chapdriver = webdriver.Chrome(options=chrome_options, service=service)
    chapdriver.get(chap_url)
    chap_title = chapdriver.find_element(by=By.XPATH, value='//*[@id="chapter-big-container"]/div/div/h2/a').text
    chap_c = chapdriver.find_element(by=By.XPATH, value='//*[@id="chapter-c"]')
    ads_divs = chap_c.find_element(by=By.XPATH, value="//*[contains(@id,'ads-chapter')]")
    chapdriver.execute_script("""
                        var element = arguments[0];
                        element.parentNode.removeChild(element);
                        """, ads_divs)
    content = chapdriver.find_element(by=By.XPATH, value='//*[@id="chapter-c"]').text
    return chap_title, content

class TruyenFullParser():
    def __init__(self, url) -> None:
        self.url = url
        self.configurations()
        self.driver = webdriver.Chrome(options=chrome_options, service=service)
        self.driver.get(self.url)

    def configurations(self):
        self.pages_list_xpath = '//*[@id="list-page"]/div[1]/div[3]/ul'
        self.page_novel_list_xpath = '//*[@id="list-page"]/div[1]/div[2]' # //*[@id="list-page"]/div[1]/div[2]
        self.novel_class_name = 'truyen-title'
        self.list_chapter_xpath = '//*[@id="list-chapter"]'
        self.stt = 'un-confirmed'
        self.text_content_only = 500

    def parser_mainpage(self):
        plist = self.driver.find_element(by=By.XPATH, value=self.pages_list_xpath)
        pages = plist.find_elements(by=By.TAG_NAME, value='a')
        max_page = int(pages[-2].get_attribute('href')[:-1].strip().split('/')[-1].split('-')[-1])
        for i in range(1, max_page+1):
            purl = self.url + f'trang-{i}/'
            self.parser_page(purl=purl)
    
    def parser_page(self, purl):
        pdriver = webdriver.Chrome(options=chrome_options, service=service)
        pdriver.get(purl)
        novel_list = pdriver.find_element(by=By.XPATH, value=self.page_novel_list_xpath).find_elements(by=By.CLASS_NAME, value='row')
        for n in novel_list:
            novel_ = n.find_element(by=By.XPATH, value=".//div[@class='col-xs-7']//div[1]//h3[@class='truyen-title']")
            novel_url = novel_.find_element(by=By.TAG_NAME, value='a').get_attribute('href')
            self.parser_novel(novel_url)
        
    def parser_novel(self, nurl):
        ndriver = webdriver.Chrome(options=chrome_options, service=service)
        ndriver.get(nurl)
        #todo: get basic infor
        search = ndriver.find_element(by=By.XPATH, value=self.list_chapter_xpath)
        nimage = ndriver.find_element(by=By.XPATH, value='//*[@id="truyen"]/div[1]/div[1]/div[2]/div[1]/div').find_element(by=By.TAG_NAME, value='img').get_attribute('src')
        ntitle = ndriver.find_element(by=By.XPATH, value='//*[@id="truyen"]/div[1]/div[1]/h3').text
        ninfor = ndriver.find_element(by=By.XPATH, value='//*[@id="truyen"]/div[1]/div[1]/div[2]/div[2]').text
        introd = ndriver.find_element(by=By.XPATH, value='//*[@id="truyen"]/div[1]/div[1]/div[3]/div[2]').text
        # print('=======================')

        chapter_engine = search.find_element(by=By.CLASS_NAME, value='row')
        chapters = chapter_engine.find_elements(by=By.TAG_NAME, value='li')
        for ch in chapters:
            chap_url = ch.find_element(by=By.TAG_NAME, value='a').get_attribute('href')
            chap_title, content = parser_chapter_truyenfull(chap_url=chap_url)
            if len(content) > self.text_content_only:
                self.stt = 'confirmed'

        #todo: check pagination
        pagi_xpath = '//*[@id="list-chapter"]/ul'
        if check_exists_by_xpath(search, pagi_xpath):
            pages = search.find_element(by=By.XPATH, value=pagi_xpath).find_elements(by=By.XPATH, value='.//li')
            churl = pages[-2].find_element(by=By.TAG_NAME, value='a').get_attribute('href')
            npage = churl.split('/')[-2].split('-')[-1]
            npage = int(npage)
            prefx = '/#list-chapter'
            chap_page_driver = webdriver.Chrome(options=chrome_options, service=service)
            for i in range(2, npage + 1):
                trans = len(''.join(churl[:len(''.join(prefx))].split('/')[-1].split('-')[-1])) + len(''.join(prefx))
                chap_page_url = churl[:-trans-2] + f'trang-{i}' + prefx
                chap_page_driver.get(chap_page_url)
                qr = chap_page_driver.find_element(by=By.XPATH, value=self.list_chapter_xpath)

                chapter_engine_ = qr.find_element(by=By.CLASS_NAME, value='row')
                chapters_ = chapter_engine_.find_elements(by=By.TAG_NAME, value='li')
                for ch in chapters_:
                    chap_url = ch.find_element(by=By.TAG_NAME, value='a').get_attribute('href')
                    chap_title, content = parser_chapter_truyenfull(chap_url=chap_url)
                    if len(content) > self.text_content_only:
                        self.stt = 'confirmed'
            sys.exit()

#//*[@id="chapter-c"]
#//*[@id="chapter-c"]/p[2]
url = 'https://truyenfull.vn/danh-sach/truyen-moi/'
parser = TruyenFullParser(url=url)
parser.parser_mainpage()