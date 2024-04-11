#!/usr/bin/python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

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

class NovelHallParser():
    def __init__(self, url) -> None:
        self.url = url
        self.configurations()
        self.driver = webdriver.Chrome(options=chrome_options, service=service)
        self.driver.get(self.url)
    
    def configurations(self):
        self.pages_layout_xpath = '//*[@id="main"]/div/div/div'
        self.pages_layout_clsn = 'type'
        self.pages_location_clsn = '//*[@id="main"]/div/div/div/div'
        self.table_body_xpath = '//*[@id="main"]/div/div/div/table/tbody/tr/td/ul'
        self.book_infor_xpath = '//*[@id="main"]/div/div[1]'
        self.chapter_list_xpath = '//*[@id="morelist"]/ul'
        self.chapter_content_class = 'entry-content'

    def parser_mainpage(self):
        self.max_page = self._get_npages()
        for i in range(1, self.max_page + 1):
            purl = f'{self.url[:-5]}-{i}.html'
            self.parser_page(purl)
            
    def parser_page(self, purl):
        pdriver = webdriver.Chrome(options=chrome_options, service=service)
        pdriver.get(purl)
        novels = pdriver.find_element(by=By.XPATH, value=self.table_body_xpath).find_elements(by=By.CLASS_NAME, value='btm')
        for n in novels:
            novel_url = n.find_element(by=By.TAG_NAME, value='a').get_attribute('href')
            self.parser_novel(novel_url)
    
    def parser_novel(self, nurl):
        ndriver = webdriver.Chrome(options=chrome_options, service=service)
        ndriver.get(nurl)
        book_infor = ndriver.find_element(by=By.XPATH, value=self.book_infor_xpath)
        img_src = book_infor.find_element(by=By.XPATH, value="//div[@class='book-img hidden-xs']").find_element(by=By.TAG_NAME, value='img')
        img_url = img_src.get_attribute('src')
        txts = book_infor.find_element(by=By.CLASS_NAME, value='book-info').text.split('\n')
        title = txts[0]
        intro = txts[2]

        ntype = txts[1][:int(txts[1].lower().find('author'))].strip()
        authr = txts[1][int(txts[1].lower().find('author')):int(txts[1].lower().find('status'))].strip()
        updat = txts[1][int(txts[1].lower().find('updatetime')):].strip()

        print(title)
        print(intro)
        print(ntype, authr, updat)
        print('====================')
        self._get_list_chapter(ndriver)

    def _get_list_chapter(self, drv):
        elem = drv.find_element(by=By.XPATH, value=self.chapter_list_xpath)
        kpt = 'post-11 post type-post status-publish format-standard hentry tag-wurulanghuai'
        chapters = elem.find_elements(by=By.TAG_NAME, value='a')
        for ch in chapters:
            curl = ch.get_attribute('href')
            cctn = ch.text
            chap_content = self.parser_chapter(curl=curl)
            time.sleep(2)

    def parser_chapter(self, curl):
        chdriver = webdriver.Chrome(options=chrome_options, service=service)
        chdriver.get(curl)
        content = chdriver.find_element(by=By.CLASS_NAME, value=self.chapter_content_class).text.replace('\n', '')
        return content

    def _get_npages(self):
        #target = self.driver.find_element(by=By.CLASS_NAME, value=self.pages_layout_clsn)
        pages = self.driver.find_element(by=By.XPATH, value=self.pages_location_clsn)
        ps = pages.find_elements(by=By.TAG_NAME, value='a')
        sub_url = ps[-1].get_attribute('href')
        max_page = sub_url.strip().split('/')[-1].split('.')[0].split('-')[1]
        return int(max_page)

url = 'https://www.novelhall.com/all2022.html'
parser = NovelHallParser(url=url)
parser.parser_mainpage()
