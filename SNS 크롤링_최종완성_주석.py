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
        #로그인 페이지로 바로 접속한다.
        browser.get("https://www.instagram.com/accounts/login/?source=auth_switcher")
        
        #username을 이름으로 가지는 객체를 찾은 후
        login = browser.find_element_by_name("username")
        
        #입력받은 ids를 해당 객체에 전송(send_keys)한다.
        login.send_keys(ids)
        #password를 이름으로 가지는 객체를 찾은 후
        password = browser.find_element_by_name("password")
        #password를 password 객체에 전송(send_keys)한다.
        password.send_keys(passwords)
        
        #확인 버튼을 찾은 후 이를 클릭(click())해준다.
        submit = browser.find_elements_by_xpath("//*[@id='react-root']/section/main/div/article/div/div[1]/div/form/div[3]/button")

        AC(browser).move_to_element(submit[0]).click().perform()
        
        #예외가 발생할경우. 즉 이미 로그인이 되어있는 상태라면 이 시퀀스를 건너 뛰어준다.
    except:
        pass


# In[161]:


#검색어 입력
def search(keyword,last,once):
    
    #로그인 직후 나오는 경고창을 우회하기 위해, instagram 페이지를 다시 로드해준다.    
    browser.get("https://www.instagram.com/")
    
    #해당 xpath를 가지는 검색창을 찾은 후에
    search = browser.find_elements_by_xpath("//*[@id='react-root']/section/nav/div[2]/div/div/div[2]/input")
    sleep(1)
    
    #검색어를 해당 위치에 전송한다.
    search[0].send_keys(keyword)
    
    #검색창의 검색 버튼을 찾아 눌러(click())해준다.
    button = browser.find_elements_by_xpath("//*[@id='react-root']/section/nav/div[2]/div/div/div[2]/span")
    AC(browser).move_to_element(button[0]).click().perform()
    sleep(2)
    
    #검색버튼을 누르면 여러 검색 결과들이 리스트로 나오는데
    for i in browser.find_elements_by_tag_name("div"):
        #검색 결과중 <#키워드>인 것을 찾으면
        if i.text == "#"+str(keyword):
            print("true")
            #iteration을 계산해준다. ietration은 ("iteration 반복 횟수 * 한번에 긁어오는 post 수)로 해당 키워드의 전체 포스트수를 나누어,
            #최종적으로 iteration을 몇번 반복하는지 자동으로 계산해준다.
            iteration = round(int(i.find_element_by_xpath("..").find_elements_by_tag_name("span")[2].text.replace(",",""))/(last*once))
            #해당 <키워드>를 클릭해준다.
            AC(browser).move_to_element(i).click().perform()
            break
        else : pass
    return iteration

# In[401]:


# In[12]:


#블록 등 비정상상황 발생시 해당 게시물 위치부터 다시 시작

def fail_return(current):
    #a를 태그로 갖는 모든 객체를 찾는다.
    for ax in browser.find_elements_by_tag_name("a"):
        #xpath(",,")는 윈도우의 상위 디렉토리 지정(cd ..)의 <..>와 같다. 즉 해당 태그에서 계속해서 상위 태그로 이동하여
        # 4계단 위의 상위 태그가 "article"이라면
        if ax.find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_xpath("..").find_element_by_xpath("..").tag_name == "article":
            #해당 객체의 주소 "href"를 반환받는다.
            tests = ax.get_attribute("href").split("/")[4]
            #만일 현재 URL이 해당 객체의 "href"와 같다면
            if current == tests:
                #그 객체를 클릭(click)한다.
                AC(browser).move_to_element(ax).click().perform()
                
            # 이렇게 복잡하게 해당 태그를 찾는 이유는, "태그네임(a)"는 너무 흔해서 특정이 어렵고, xpath는 해당 객체의 위치가 계속 변화하여 마찬가지로
            # 일반화가 어렵기 때문이다.


# In[4]:


def engine(firstpage,lastpage,current,post):
    datalist = []
    kill_switch = 0
    log = list()
    
    #while의 조건문은 iteration의 수다. 만일 1 <= 5 라면, 한번에 10개씩의 포스트를 긁어오는 작업을 5번 반복한다.
    while firstpage <= lastpage:
        sleep(random.randint(0,1))
        #kill_switch = 0, 즉 예외가 발생했던 적이 없는 경우
        try : 
            #앞서 정의한 fail_return을 통해 저장된 현재 위치(current)를 다시 소생시킨다.
            fail_return(current)
            log.append("소생 페이즈 성공")
            #post는 한번에 긁어올 포스트의 수이다.
            for i in range(0,post):
                #i가 아직 포스트 수에 미치지 못했다면
                if i < (post-2):
                    #로그를 저장한다.
                    log.append("start,"+str(i))
                    #<이전> 버튼과 <다음>버튼의 갯수 정보를 j에 담는다. 버튼이 둘 다 있을경우엔 2이고, 아닐 경우엔 1로 반환된다..
                    j = len(browser.find_elements_by_xpath("/html/body/div[3]/div/div[1]/div/div/a"))
                    #<이전>버튼과 <다음>버튼을 for문으로 번갈아 가져온다.
                    for k in browser.find_elements_by_xpath("/html/body/div[3]/div/div[1]/div/div/a"):
                        #만일 이전, 다음 버튼 두개가 존재하는 경우
                        if j == 2:
                            #그러면서, 동시에 그 버튼의 text 정보가 "다음"일 경우엔
                            if k.text == "다음" :
                                sleep(1)
                                #다음 버튼을 누르기 전에, 해당 포스트 내용을 긁어서 datalist에 저장한다.
                                ab = browser.find_element_by_xpath("/html/body/div[3]/div/div[2]/div/article/div[2]/div[1]/ul/li[1]/div/div/div/span")
                                datalist.append(ab.text.replace("\n","").replace("#"," "))
                                #이후 다음버튼(k)를 누른다.
                                log.append("append type1 완료")
                                AC(browser).move_to_element(k).click().perform()
                                #해당 포스트 load에 실패할 경우를 대비하여, 다음 포스트의 URL정보를 current에 저장한다.(fail_return에 활용)
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
                                #다음 버튼을 누르기 전에, 해당 포스트 내용을 긁어서 datalist에 저장한다.
                                ab = browser.find_element_by_xpath("/html/body/div[3]/div/div[2]/div/article/div[2]/div[1]/ul/li[1]/div/div/div/span")
                                datalist.append(ab.text.replace("\n","").replace("#"," "))
                                #이후 다음버튼(k)를 누른다.
                                log.append("append type3 완료")
                                exit = browser.find_element_by_xpath("/html/body/div[3]/div/button")
                                #exit 버튼의 위치를 find_element로 찾는다. 
                                AC(browser).move_to_element(exit).click().perform()
                                #exit 버튼을 눌러 창을 닫는다.
                                current = browser.current_url.split("/")[4]
                if i >= (post-1): 
                    #마지막으로 긁은 포스트의 순서를 log파일에 저장한다. 
                    log.append("end,"+str(i))
                    log.append("종료 페이즈 시작")
                    #exit 버튼을 찾는다.
                    exit = browser.find_element_by_xpath("/html/body/div[3]/div/button")
                    #exit 버튼을 눌러 창을 찾는다.
                    AC(browser).move_to_element(exit).click().perform()
                    #Page_Down 키를 브라우저에 전송해서, 앞으로 긁어올 포스트의 위치에 스크롤을 맞춘다.
                    ## 이는 Fail_return 상황이 발생할 경우, JAVA 기반의 인스타그램에서 해당 객체의 위치를 찾기 위해 스크롤이 해당 객체의 위치를 
                    ## 불러서 저장해둘 필요가 있기 때문이다.
                    AC(browser).send_keys(Keys.PAGE_DOWN).perform()
                    firstpage += 1
                    break
            
            #예외가 발생하면 일단 창의 X버튼을 누르고, kill_switch를 1로 켠다. 
        #예외가 발생하면 일단 창의 X버튼을 누른다.
        except :
            try:
                #exit  버튼을 찾아서 누른다.
                exit = browser.find_element_by_xpath("/html/body/div[3]/div/button")
                AC(browser).move_to_element(exit).click().perform()
            except : 
                #만일 fail_return이 실패했을 경우엔 exit 버튼을 찾을 수 없다. exit 버튼을 찾지 못해 오류가 발생했을 경우
                # page_down 키를 send 하여 fail_return이 해당 current를 찾도록 한다.
                AC(browser).send_keys(Keys.PAGE_DOWN).perform()
                pass
            log.append("오류 발생")
            sleep(1)

            
    return(datalist,current,log)


# In[5]:


def get_clear_browsing_button(browser):
    """Find the "CLEAR BROWSING BUTTON" on the Chrome settings page."""
    #구글 개인정보보호 섹션의 "<데이터 삭제> 버튼의 위치를 css_selector를 통해 /deep/으로 바로 불러온다.
    return browser.find_element_by_css_selector('* /deep/ #clearBrowsingDataConfirm')

def chrome_flush():
    log2 = list()
    #새로운 탭을 열어준다.
    browser.execute_script("window.open('');")
    #새로 연 탭으로 이동한다. browser.window_handlers는 현재 브라우저에 띄어져있는 탭들을 모두 나다낸다.
    browser.switch_to.window(browser.window_handles[-1])
    sleep(2)
    
    #구글 설정창을 열어준다.

    browser.get("chrome://settings/clearBrowserData");
    sleep(1)
    log2 = ["플러싱 시작"]
    
    #최대 60초까지 브라우저를 대기시킨다.
    wait = WebDriverWait(browser, 60)
    #<데이터 삭제>버튼이 소스코드로 읽힐때까지 기다려준다.
    wait.until(get_clear_browsing_button)
    #<데이터 삭제>버튼을 눌러준다.
    get_clear_browsing_button(browser).click()
    wait.until_not(get_clear_browsing_button)

    # # 현재 탭을 닫는다.
    browser.close()
    sleep(1)
    log2 = log2+["플러싱 완료"]

    # 원래 탭을 switch_to.window를 통해 다시 복귀한다.
    browser.switch_to.window(browser.window_handles[0])
    return log2


# In[6]:


def main(keyword,last,once):
    datum = list()
    logfile = DataFrame()
    
    #login_seq를 통해 로그인한다.
    login_seq("neverland251@gmail.com","패스워드")
    sleep(1)
    
    #search를 하면서 iteration을 반환받는다.
    iterations = search(keyword,last,once)
    browser.implicitly_wait(10)
    print(iterations)
    
    ##가장 처음 iteration에서, current값이 저장되어 있지 않기 때문에, 가장 처음 포스트의 URL을 읽어온다.

    cont = browser.find_element_by_xpath("//*[@id='react-root']/section/main/article/div[2]/div/div[1]/div[1]/a")
    current = cont.get_attribute("href").split("/")[4]
    #fail_return의 소생 기능을 사용하여 해당 포스트를 소생시킨다.(맨 처음 iteration에선 단순 실행의 의미만 갖는다.)
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




