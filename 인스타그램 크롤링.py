#!/usr/bin/env python
# coding: utf-8

# In[134]:


from selenium import webdriver
from selenium.webdriver import ActionChains as AC

from pandas import Series,DataFrame
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import urllib.request as request
import requests
import random

from time import sleep
import re


# In[135]:


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
def search(keyword):

    browser.get("https://www.instagram.com/")
    search = browser.find_elements_by_xpath("//*[@id='react-root']/section/nav/div[2]/div/div/div[2]/input")
    sleep(1)
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


# In[137]:


#블록 등 비정상상황 발생시 해당 게시물 위치부터 다시 시작

def fail_return(current):
    for i in browser.find_elements_by_tag_name("a"):
        if i.find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_xpath("..").tag_name == "article":
            tests = i.get_attribute("href").split("/")[4]
            if current == tests:
                AC(browser).move_to_element(i).click().perform()
            


# In[156]:


#엔진 속 엔진. 실제 데이터들을 스크래핑하여 datus 변수로 이를 반환(return)함

def engine_engine():
    j = len(browser.find_elements_by_xpath("/html/body/div[3]/div/div[1]/div/div/a"))      
    for i in browser.find_elements_by_xpath("/html/body/div[3]/div/div[1]/div/div/a"):
        #만일 이전, 다음 버튼 두개가 존재하는 경우
        if j == 2:
            if i.text == "다음" :
                sleep(1)
                ab = browser.find_element_by_xpath("/html/body/div[3]/div/div[2]/div/article/div[2]/div[1]/ul/li[1]/div/div/div/span")
                datus = ab.text.replace("\n","").replace("#"," ")
                AC(browser).move_to_element(i).click().perform()
                current = browser.current_url.split("/")[4]
                return datus,current
        #만일 이전, 다음 버튼 중 하나만 존재하는 경우
        if j == 1:
            if i.text == "다음":
                sleep(1)
                ab = browser.find_element_by_xpath("/html/body/div[3]/div/div[2]/div/article/div[2]/div[1]/ul/li[1]/div/div/div/span")
                datus = ab.text.replace("\n","").replace("#"," ")
                AC(browser).move_to_element(i).click().perform()
                current = browser.current_url.split("/")[4]
                return datus,current
            #이전 버튼만 존재하는 경우 : 마지막 페이지를 의미
            else :
                sleep(1)
                ab = browser.find_element_by_xpath("/html/body/div[3]/div/div[2]/div/article/div[2]/div[1]/ul/li[1]/div/div/div/span")
                datus = ab.text.replace("\n","").replace("#"," ")
                exit = browser.find_element_by_xpath("/html/body/div[3]/div/button")
                AC(browser).move_to_element(exit).click().perform()
                current = browser.current_url.split("/")[4]
                return datus,current


# In[188]:


#엔진. 정상 진행과 예외 진행을 구분하여 예외 발생 시 이를 핸들링해준다.

def engine(lastpage):
    datalist = []
    currentpage = 0
    kill_switch = 0
    current = 0
    
    while currentpage <= lastpage:
        sleep(ramdom.randint(0,1))
        #kill_switch = 0, 즉 예외가 발생했던 적이 없는 경우
        if kill_switch == 0:
            try : 
                aa,current = engine_engine()
                datalist.append(aa)
                currentpage += 1
            #예외가 발생하면 일단 창의 X버튼을 누르고, kill_switch를 1로 켠다. 
            except :
                current = browser.current_url.split("/")[4]
                exit = browser.find_element_by_xpath("/html/body/div[3]/div/button")
                AC(browser).move_to_element(exit).click().perform()
                kill_switch = 1
                sleep(1)
        #kill_switch = 1, 즉 예외가 발생했던 경우
        if kill_switch == 1:
            #fail_return으로 마지막 위치에서 다시 시작한다.
            fail_return(current)
            aa,current = engine_engine()
            datalist.append(aa)
            #예외 처리 후 kill_switch를 0으로 다시 끈다.
            kill_switch = 0
            currentpage += 1
        print(datalist)
    return datalist


# In[189]:


#껍데기

def main(ids,passwords,keyword,lastpage):
    datum = list()
    
    login_seq(ids,passwords)
    sleep(1)
    
    search(keyword)
    sleep(7)
    
    cont = browser.find_element_by_xpath("//*[@id='react-root']/section/main/article/div[2]/div/div[1]/div[1]/a/div[1]/div[1]")
    AC(browser).move_to_element(cont).click().perform()
    sleep(0.5)
    
    datum.append(engine(lastpage))
    return datum
    


# In[186]:


browser = webdriver.Chrome("chromedriver.exe")

html = main("neverland251@gmail.com","패스워드","하이네켄",100)


# In[178]:


html


# In[70]:





# In[76]:

'''
for i in browser.find_elements_by_tag_name("a"):
    if i.find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_xpath("..").tag_name == "article":
        tests = i.get_attribute("href").split("/")[4]
        if current == tests:
            AC(browser).move_to_element(i).click().perform()
            print("executed")
        else : print("false")

'''


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

