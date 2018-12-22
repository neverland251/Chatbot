#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver import ActionChains as AC

from pandas import Series,DataFrame
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import urllib.request as request
import requests


from time import sleep
import re


# In[ ]:


browser = webdriver.Chrome("chromedriver.exe")


# In[609]:


#로그인 부분

login = browser.find_element_by_name("username")
login.send_keys(ids)

password = browser.find_element_by_name("password")
password.send_keys(password)

submit = browser.find_elements_by_xpath("//*[@id='react-root']/section/main/div/article/div/div[1]/div/form/div[3]/button")

AC(browser).move_to_element(submit[0]).click().perform()


# In[587]:


#검색어 입력
def search(keyword)

    browser.get("https://www.instagram.com/")
    search = browser.find_elements_by_xpath("//*[@id='react-root']/section/nav/div[2]/div/div/div[2]/input")
    search[0].send_keys(keyword)
    button = browser.find_elements_by_xpath("//*[@id='react-root']/section/nav/div[2]/div/div/div[2]/span")
    AC(browser).move_to_element(button[0]).click().perform()
    for i in browser.find_elements_by_tag_name("span"):
        if i.text == "#"+str(keyword):
            print("true")
            AC(browser).move_to_element(i).click().perform()
            break
        else : pass


# In[467]:


'''
for i in browser.find_elements_by_tag_name("span"):
    if i.text == "#"+str(keyword):
        print("true",i.text)
        break


for i in browser.find_elements_by_tag_name("span"):
    try:
        if i.find_elements_by_xpath("..")[0].find_elements_by_xpath("..")[0].find_elements_by_xpath("..")[0].find_elements_by_xpath("..")[0].tag_name == "li":
            datalist.append(i.text.replace("\n","").replace("#"," "))
    except : pass

try:
    browser.find_elements_by_tag_name("span")[0].find_elements_by_xpath("..")[0].find_elements_by_xpath("..")[0].find_elements_by_xpath("..")[0].find_elements_by_xpath("..")[0].tag_name

except (InvalidSelectorException):
    pass
''''''


# In[298]:


'''
for i in browser.find_elements_by_tag_name("button"):
    if i.text.rstrip().lstrip() == "더 보기":
        AC(browser).move_to_element(i).click().perform()
        sleep(0.5)
    else : pass

for i,j in zip(browser.find_elements_by_tag_name("span"),browser.find_elements_by_tag_name("button")):
    #span 태그를 가진 요소 중 그 부모요소가 div인 요소들만 고른다.(이 요소들은 텍스트 요소를 담고 있다.)
    try:
        if i.find_elements_by_xpath("..")[0].find_elements_by_xpath("..")[0].find_elements_by_xpath("..")[0].find_elements_by_xpath("..")[0].tag_name == "li":
            if j.text.lstrip().rstrip() == b:
                AC(browser).move_to_element(j).click().perform()
                sleep(0.2)
            print(i.text)
        else : pass
    except :
        pass
'''

