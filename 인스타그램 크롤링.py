#!/usr/bin/env python
# coding: utf-8

# In[291]:


from selenium import webdriver
from selenium.webdriver import ActionChains as AC
from selenium.webdriver.common.keys import Keys

from pandas import Series,DataFrame
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
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


# In[401]:


#블록 등 비정상상황 발생시 해당 게시물 위치부터 다시 시작

def fail_return(current):
    for ax in browser.find_elements_by_tag_name("a"):
        if ax.find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_xpath("..").tag_name == "article":
            tests = ax.get_attribute("href").split("/")[4]
            if current == tests:
                AC(browser).move_to_element(ax).click().perform()
            


# In[500]:


#엔진 속 엔진. 실제 데이터들을 스크래핑하여 datus 변수로 이를 반환(return)함

def engine_engine(current):
    datus = list()
    log = list()
    fail_return(current)
    log.append("소생 페이즈 성공")
    
    for i in range(0,9):
        if i <= 7:
            log.append("start,"+str(i))
            j = len(browser.find_elements_by_xpath("/html/body/div[3]/div/div[1]/div/div/a"))
            for k in browser.find_elements_by_xpath("/html/body/div[3]/div/div[1]/div/div/a"):

                #만일 이전, 다음 버튼 두개가 존재하는 경우
                if j == 2:
                    if k.text == "다음" :
                        sleep(1)
                        ab = browser.find_element_by_xpath("/html/body/div[3]/div/div[2]/div/article/div[2]/div[1]/ul/li[1]/div/div/div/span")
                        datus.append(ab.text.replace("\n","").replace("#"," "))
                        AC(browser).move_to_element(k).click().perform()
                        current = browser.current_url.split("/")[4]
                    
                #만일 이전, 다음 버튼 중 하나만 존재하는 경우
                if j == 1:
                    #다음 버튼만 존재하는 경우 : 첫 페이지를 의미
                    if k.text == "다음":
                        sleep(1)
                        ab = browser.find_element_by_xpath("/html/body/div[3]/div/div[2]/div/article/div[2]/div[1]/ul/li[1]/div/div/div/span")
                        datus.append(ab.text.replace("\n","").replace("#"," "))
                        AC(browser).move_to_element(k).click().perform()
                        current = browser.current_url.split("/")[4]
                    
                    #이전 버튼만 존재하는 경우 : 마지막 페이지를 의미
                    else :
                        sleep(1)
                        ab = browser.find_element_by_xpath("/html/body/div[3]/div/div[2]/div/article/div[2]/div[1]/ul/li[1]/div/div/div/span")
                        datus.append(ab.text.replace("\n","").replace("#"," "))
                        exit = browser.find_element_by_xpath("/html/body/div[3]/div/button")
                        AC(browser).move_to_element(exit).click().perform()
                        current = browser.current_url.split("/")[4]
        if i >= 7 : 
            log.append("end,"+str(i))
            log.append("종료 페이즈 시작")
            exit = browser.find_element_by_xpath("/html/body/div[3]/div/button")
            AC(browser).move_to_element(exit).click().perform()
            AC(browser).send_keys(Keys.PAGE_DOWN).perform()
            return (datus,current,log)


# In[535]:


#엔진. 정상 진행과 예외 진행을 구분하여 예외 발생 시 이를 핸들링해준다.

def engine(firstpage,lastpage,current):
    datalist = []
    kill_switch = 0
    
    while firstpage <= lastpage:
        sleep(random.randint(0,1))
        #kill_switch = 0, 즉 예외가 발생했던 적이 없는 경우
        if kill_switch == 0:
            try : 
                aa,current,log = engine_engine(current)
                datalist.append(aa)
                log += log
                firstpage += 1
            #예외가 발생하면 일단 창의 X버튼을 누르고, kill_switch를 1로 켠다. 
            except :
                fail_return(current)
                exit = browser.find_element_by_xpath("/html/body/div[3]/div/button")
                AC(browser).move_to_element(exit).click().perform()
                kill_switch = 1
                log.append("킬 스위치 켜짐")
                sleep(1)
        #kill_switch = 1, 즉 예외가 발생했던 경우
        if kill_switch == 1:
            #fail_return으로 마지막 위치에서 다시 시작한다.
            try:
                aa,current,log = engine_engine(current)
                datalist.append(aa)
                log += log

                #예외 처리 후 kill_switch를 0으로 다시 끈다.
                kill_switch = 0
                log.append("킬 스위치 꺼짐")
                firstpage += 1
            except:
                exit = browser.find_element_by_xpath("/html/body/div[3]/div/button")
                AC(browser).move_to_element(exit).click().perform()
                sleep(1)
    return (datalist,current,log)


# In[498]:


#껍데기(미사용)

def main(ids,passwords,keyword,lastpage):
    datum = list()
    
    login_seq(ids,passwords)
    sleep(1)
    
    search(keyword)
    sleep(7)
    
    cont = browser.find_element_by_xpath("//*[@id='react-root']/section/main/article/div[2]/div/div[1]/div[1]/a")
    current = cont.get_attribute("href").split("/")[4]
    
    datum.append(engine(lastpage,current))
    return datum
    


# In[492]:


browser = webdriver.Chrome("chromedriver.exe")


# In[541]:


datum = list()
logfile = DataFrame()

login_seq("아이디","")
sleep(1)

search("하이네켄")
sleep(3)

cont = browser.find_element_by_xpath("//*[@id='react-root']/section/main/article/div[2]/div/div[1]/div[1]/a")
current = cont.get_attribute("href").split("/")[4]
fail_return(current)

for i in range(0,1):
    aaa,current,log = engine(1,2,current)    
    datum.append(aaa)
    log += log
    logfile = pd.concat([logfile,DataFrame(log)])

logfile.reset_index()
logfile.to_csv("log.csv")


# In[ ]:


##테스트1

'''
count = 0
current = "BrvzHiyBPNR"

cont = browser.find_element_by_xpath("//*[@id='react-root']/section/main/article/div[2]/div/div[1]/div[1]/a")
current = cont.get_attribute("href").split("/")[4]
fail_return(current)

for ab in range(0,3):
    for i in range(0,9):
        if i <= 7:
            j = len(browser.find_elements_by_xpath("/html/body/div[3]/div/div[1]/div/div/a"))
            for k in browser.find_elements_by_xpath("/html/body/div[3]/div/div[1]/div/div/a"):
                print("start",i)
                #만일 이전, 다음 버튼 두개가 존재하는 경우
                if j == 2:
                    if k.text == "다음" :
                        sleep(1)
                        ab = browser.find_element_by_xpath("/html/body/div[3]/div/div[2]/div/article/div[2]/div[1]/ul/li[1]/div/div/div/span")
                        datus = ab.text.replace("\n","").replace("#"," ")
                        AC(browser).move_to_element(k).click().perform()
                        current = browser.current_url.split("/")[4]

                #만일 이전, 다음 버튼 중 하나만 존재하는 경우
                if j == 1:
                    #다음 버튼만 존재하는 경우 : 첫 페이지를 의미
                    if k.text == "다음":
                        sleep(1)
                        ab = browser.find_element_by_xpath("/html/body/div[3]/div/div[2]/div/article/div[2]/div[1]/ul/li[1]/div/div/div/span")
                        datus = ab.text.replace("\n","").replace("#"," ")
                        AC(browser).move_to_element(k).click().perform()
                        current = browser.current_url.split("/")[4]

                    #이전 버튼만 존재하는 경우 : 마지막 페이지를 의미
                    else :
                        sleep(1)
                        ab = browser.find_element_by_xpath("/html/body/div[3]/div/div[2]/div/article/div[2]/div[1]/ul/li[1]/div/div/div/span")
                        datus = ab.text.replace("\n","").replace("#"," ")
                        exit = browser.find_element_by_xpath("/html/body/div[3]/div/button")
                        AC(browser).move_to_element(exit).click().perform()
                        current = browser.current_url.split("/")[4]
        if i >= 7 : 
            print("end",i)
            print("phase start")
            exit = browser.find_element_by_xpath("/html/body/div[3]/div/button")
            AC(browser).move_to_element(exit).click().perform()
            AC(browser).send_keys(Keys.PAGE_DOWN).perform()
'''


# In[ ]:


## 테스트2
'''
for i in range(0,10):
    try:   
        div = browser.find_element_by_xpath("//*[@id='react-root']/section/main/article/div[2]/div")
        for i in div.find_elements_by_tag_name("a"):
            AC(browser).move_to_element(i).click().perform()
            sleep(1)
            ab = browser.find_element_by_xpath("/html/body/div[3]/div/div[2]/div/article/div[2]/div[1]")
            print(ab.text.replace("\n","").replace("#"," "))
            sleep(0.5)
            exit = browser.find_element_by_xpath("/html/body/div[3]/div/button")
            AC(browser).move_to_element(exit).click().perform()

    except :
        pass
'''


# In[298]:


## 테스트3
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

