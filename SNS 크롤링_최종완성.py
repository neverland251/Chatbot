#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium.common.exceptions import WebDriverException
from selenium import webdriver
from selenium.webdriver import ActionChains as AC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from pandas import Series,DataFrame
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import random

import csv

from time import sleep
import re


# In[2]:


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


# In[161]:


#검색어 입력
def search(keyword,last,once):

    browser.get("https://www.instagram.com/")
    search = browser.find_elements_by_xpath("//*[@id='react-root']/section/nav/div[2]/div/div/div[2]/input")
    sleep(1)
    search[0].send_keys(keyword)
    button = browser.find_elements_by_xpath("//*[@id='react-root']/section/nav/div[2]/div/div/div[2]/span")
    AC(browser).move_to_element(button[0]).click().perform()
    sleep(2)
    for i in browser.find_elements_by_tag_name("div"):
        if i.text == "#"+str(keyword):
            print("true")
            iteration = round(int(i.find_element_by_xpath("..").find_elements_by_tag_name("span")[2].text.replace(",",""))/(last*once))
            AC(browser).move_to_element(i).click().perform()
            break
        else : pass
    return iteration

# In[401]:


# In[12]:


#블록 등 비정상상황 발생시 해당 게시물 위치부터 다시 시작

def fail_return(current):
    
    for ax in browser.find_elements_by_tag_name("a"):
        if ax.find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_xpath("..").tag_name == "article":
            tests = ax.get_attribute("href").split("/")[4]
            if current == tests:
                AC(browser).move_to_element(ax).click().perform()


# In[4]:


def engine(firstpage,lastpage,current,post):
    datalist = []
    kill_switch = 0
    log = list()
    
    while firstpage <= lastpage:
        sleep(random.randint(0,1))
        #kill_switch = 0, 즉 예외가 발생했던 적이 없는 경우
        try : 
            fail_return(current)
            log.append("소생 페이즈 성공")
            for i in range(0,post):
                if i < (post-2):
                    log.append("start,"+str(i))
                    j = len(browser.find_elements_by_xpath("/html/body/div[3]/div/div[1]/div/div/a"))
                    for k in browser.find_elements_by_xpath("/html/body/div[3]/div/div[1]/div/div/a"):
                        #만일 이전, 다음 버튼 두개가 존재하는 경우
                        if j == 2:
                            if k.text == "다음" :
                                sleep(1)
                                ab = browser.find_element_by_xpath("/html/body/div[3]/div/div[2]/div/article/div[2]/div[1]/ul/li[1]/div/div/div/span")
                                datalist.append(ab.text.replace("\n","").replace("#"," "))
                                log.append("append type1 완료")
                                AC(browser).move_to_element(k).click().perform()
                                current = browser.current_url.split("/")[4]

                        #만일 이전, 다음 버튼 중 하나만 존재하는 경우
                        if j == 1:
                            #다음 버튼만 존재하는 경우 : 첫 페이지를 의미
                            if k.text == "다음":
                                sleep(1)
                                ab = browser.find_element_by_xpath("/html/body/div[3]/div/div[2]/div/article/div[2]/div[1]/ul/li[1]/div/div/div/span")
                                datalist.append(ab.text.replace("\n","").replace("#"," "))
                                log.append("append type2 완료")
                                AC(browser).move_to_element(k).click().perform()
                                current = browser.current_url.split("/")[4]

                            #이전 버튼만 존재하는 경우 : 마지막 페이지를 의미
                            else :
                                sleep(1)
                                ab = browser.find_element_by_xpath("/html/body/div[3]/div/div[2]/div/article/div[2]/div[1]/ul/li[1]/div/div/div/span")
                                datalist.append(ab.text.replace("\n","").replace("#"," "))
                                log.append("append type3 완료")
                                exit = browser.find_element_by_xpath("/html/body/div[3]/div/button")
                                AC(browser).move_to_element(exit).click().perform()
                                current = browser.current_url.split("/")[4]
                if i >= (post-1): 
                    log.append("end,"+str(i))
                    log.append("종료 페이즈 시작")
                    exit = browser.find_element_by_xpath("/html/body/div[3]/div/button")
                    AC(browser).move_to_element(exit).click().perform()
                    AC(browser).send_keys(Keys.PAGE_DOWN).perform()
                    firstpage += 1
                    break
            
            #예외가 발생하면 일단 창의 X버튼을 누르고, kill_switch를 1로 켠다. 
        except :
            try:
                exit = browser.find_element_by_xpath("/html/body/div[3]/div/button")
                AC(browser).move_to_element(exit).click().perform()
            except : 
                AC(browser).send_keys(Keys.PAGE_DOWN).perform()
                pass
            log.append("오류 발생")
            sleep(1)

            
    return(datalist,current,log)


# In[5]:


def get_clear_browsing_button(browser):
    """Find the "CLEAR BROWSING BUTTON" on the Chrome settings page."""
    return browser.find_element_by_css_selector('* /deep/ #clearBrowsingDataConfirm')

def chrome_flush():
    log2 = list()
    
    browser.execute_script("window.open('');")
    browser.switch_to.window(browser.window_handles[-1])
    sleep(2)

    browser.get("chrome://settings/clearBrowserData");
    sleep(1)
    log2 = ["플러싱 시작"]
    wait = WebDriverWait(browser, 60)
    wait.until(get_clear_browsing_button)
    get_clear_browsing_button(browser).click()
    wait.until_not(get_clear_browsing_button)

    # close the active tab
    browser.close()
    sleep(1)
    log2 = log2+["플러싱 완료"]

    # Switch back to the first tab
    browser.switch_to.window(browser.window_handles[0])
    return log2


# In[6]:


def main(keyword,last,once):
    datum = list()
    logfile = DataFrame()

    login_seq("neverland251@gmail.com","cjswp12358")
    sleep(1)

    iterations = search(keyword,last,once)
    browser.implicitly_wait(10)
    print(iterations)

    cont = browser.find_element_by_xpath("//*[@id='react-root']/section/main/article/div[2]/div/div[1]/div[1]/a")
    current = cont.get_attribute("href").split("/")[4]
    fail_return(current)

    with open("crawlling.csv","w",encoding="UTF-8") as text:
        with open ("log.csv","w") as logtext:
            f = csv.writer(text, delimiter = " ")
            l = csv.writer(logtext,delimiter = " ")
            for i in range(0,iterations - 10):
                aaa,current,log = engine(1,last,current,once)    
                log2 = chrome_flush()
                log += log2
                for i,j in zip(aaa,log):
                    f.writerow([i])
                    l.writerow([j])
                for k in log2:
                    l.writerow([k])


# In[17]:


browser = webdriver.Chrome("chromedriver.exe")


# In[18]:


main("하이네켄",5,20)


# In[ ]:




