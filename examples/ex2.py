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
chap_url = 'https://truyenfull.vn/chay-tron-khap-dia-cau/chuong-1/'


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
    print(chapdriver.find_element(by=By.XPATH, value='//*[@id="chapter-c"]').text)

# parser_chapter_truyenfull(chap_url)
txt = """
Vào tháng 10, Ngân Thành đã bước vào đầu mùa đông.

Cơn gió lạnh còn chưa hoàn toàn xâm nhập vào. Sự trì trệ của giá lạnh giống như một lớp kẹo đường ngưng tụ trên mặt đất nhưng không thể tan được.

Bên ngoài trời rất lạnh và khắc nghiệt nhưng khu thương mại kéo dài từ đại lộ Champs Élysées lại ấm áp tựa như mùa xuân – một sự khởi đầu của bốn mùa.

Các cửa sổ lớn từ sàn đến trần được dát bằng những lá vàng vụn nhỏ từ trên xuống dưới mang theo ánh sáng trên đường phố.
"""
print(len(txt))