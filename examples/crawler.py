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
driver = webdriver.Chrome(options=chrome_options, service=service)

TEXT = ''
VOICE = 'zh-CN-YunxiNeural'
OUTPUT_FILE = ''
WEBVTT_FILE = ''

async def amain() -> None:
    global TEXT, VOICE, OUTPUT_FILE, WEBVTT_FILE
    """Main function"""
    communicate = edge_tts.Communicate(TEXT, VOICE, rate='-20%')
    submaker = edge_tts.SubMaker()
    with open(OUTPUT_FILE, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.create_sub((chunk["offset"], chunk["duration"]), chunk["text"])

    with open(WEBVTT_FILE, "w", encoding="utf-8") as file:
        file.write(submaker.generate_subs())
loop = asyncio.get_event_loop_policy().get_event_loop()
NAME = '我的超能力每周刷新'
ROOT = 'data'
STORE = os.path.join(ROOT, NAME)

if not os.path.exists(STORE):
    os.makedirs(STORE)

url = 'https://www.69shu.pro/book/52914/'
driver.get(url)
search = driver.find_element(by=By.XPATH,value='//*[@id="catalog"]/ul')
sub_elements = search.find_elements(by=By.TAG_NAME, value="a")
chap_content = []
chap_full = ''
for idx, se in enumerate(sub_elements):
    nchapter = idx + 1
    tochap = os.path.join(STORE, str(nchapter))
    if not os.path.exists(tochap):
        os.makedirs(tochap)

    totxt = os.path.join(tochap, 'content.txt')
    tomp3 = os.path.join(tochap, 'content.mp3')
    print(se.get_attribute('href'), se.text)
    slink = se.get_attribute('href')
    sdriver = webdriver.Chrome(options=chrome_options, service=service)
    sdriver.get(slink)
    time.sleep(2)

    scontent = sdriver.find_elements(by=By.CLASS_NAME, value='txtnav') 
    print('===========================')
    txt = scontent[0].text.replace('\n', '')

    writer = open(totxt, 'w', encoding="utf-8")
    writer.write(txt)
    writer.close()

    OUTPUT_FILE = tomp3
    TEXT = txt
    WEBVTT_FILE = os.path.join(tochap, 'content.vtt')
    
    try:
        loop.run_until_complete(amain())
    except:
        pass

    time.sleep(2)