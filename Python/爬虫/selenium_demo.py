#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : Zhaifg (zhaifengguo@foxmail.com)
# @Link    : http://htop.me

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from lxml import etree

from pyvirtualdisplay import Display
xephyr = Display(visible=1, size=(320, 240)).start()


driver = webdriver.Firefox()
driver.get('https://v.qq.com/x/cover/qwvcfzl987ydm63.html')
elem = driver.find_element_by_xpath(
    "//*[@id=\"video_scroll_wrap\"]/div[4]/div[1]/div")
all_tab = elem.find_elements_by_tag_name('a')

all_jj_a = []
for tab in all_tab:
    tab.send_keys(Keys.ENTER)
    html = etree.HTML(driver.page_source)
    div = html.xpath('//*[@id="video_scroll_wrap"]/div[4]/div[2]')[0]
    all_jj_a.extend(div.xpath("//span[@class='item']/a/@href"))

driver.close()

print(len(all_jj_a))
print(all_jj_a)
