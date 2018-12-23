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
def login_seq(ids,passwords):
    try:
        browser.get("https://www.instagram.com/accounts/login/?source=auth_switcher")
        login = browser.find_element_by_name("username")
        login.send_keys(ids)

        password = browser.find_element_by_name("password")
        password.send_keys(passwords)

        submit = browser.find_elements_by_xpath("//*[@id='react-root']/section/main/div/article/div/div[1]/div/form/div[3]/button")

        AC(browser).move_to_element(submit[0]).click().perform()
    except:
        pass


# In[587]:


#검색어 입력
def search(keyword):

    browser.get("https://www.instagram.com/")
    search = browser.find_elements_by_xpath("//*[@id='react-root']/section/nav/div[2]/div/div/div[2]/input")
    search[0].send_keys(keyword)
    button = browser.find_elements_by_xpath("//*[@id='react-root']/section/nav/div[2]/div/div/div[2]/span")
    AC(browser).move_to_element(button[0]).click().perform()
    sleep(2)
    for i in browser.find_elements_by_tag_name("span"):
        if i.text == "#"+str(keyword):
            print("true")
            AC(browser).move_to_element(i).click().perform()
            break
        else : pass


#엔진 부분
def engine(lastpage):
    datalist = []
    currentpage = 0
    
    while currentpage <= lastpage:
        j = len(browser.find_elements_by_xpath("/html/body/div[3]/div/div[1]/div/div/a"))      
        for i in browser.find_elements_by_xpath("/html/body/div[3]/div/div[1]/div/div/a"):

            if j == 2:
                if i.text == "다음" :
                    sleep(1)
                    ab = browser.find_element_by_xpath("/html/body/div[3]/div/div[2]/div/article/div[2]/div[1]/ul/li[1]/div/div/div/span")
                    datalist.append(ab.text.replace("\n","").replace("#"," "))
                    AC(browser).move_to_element(i).click().perform()
                    currentpage += 1
            if j == 1:
                if i.text == "다음":
                    sleep(1)
                    ab = browser.find_element_by_xpath("/html/body/div[3]/div/div[2]/div/article/div[2]/div[1]/ul/li[1]/div/div/div/span")
                    datalist.append(ab.text.replace("\n","").replace("#"," "))
                    AC(browser).move_to_element(i).click().perform()
                    currentpage += 1
                else :
                    sleep(1)
                    ab = browser.find_element_by_xpath("/html/body/div[3]/div/div[2]/div/article/div[2]/div[1]/ul/li[1]/div/div/div/span")
                    datalist.append(ab.text.replace("\n","").replace("#"," "))
                    exit = browser.find_element_by_xpath("/html/body/div[3]/div/button")
                    AC(browser).move_to_element(exit).click().perform()
                    return datalist  
  
#껍데기
def main(ids,passwords,keyword,lastpage):
    datum = list()
    
    login_seq(ids,passwords)
    sleep(1)
    
    search(keyword)
    sleep(2)
    
    test = browser.find_elements_by_xpath("//*[@id='react-root']/section/main/article/div[1]/div/div/div[1]/div[1]/a/div/div[2]")
    AC(browser).move_to_element(test[0]).click().perform()
    sleep(0.5)
    
    datum.append(engine(lastpage))
    return datum

#작동 시연
browser = webdriver.Chrome("chromedriver.exe")

html = main("아이디","비밀번호","검색 키워드",50(검색페이지))

html


