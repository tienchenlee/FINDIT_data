#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import os

from bs4 import BeautifulSoup
from pprint import pprint
from selenium import webdriver
#from selenium.webdriver.common.by import By
from time import sleep

def scrapeTag(soup, tag, attr=None, **kwargs):
    """
    抓取指定的標籤和屬性，返回所有匹配的內容或屬性值。
    
    :param soup: BeautifulSoup 解析過的頁面
    :param tag: 要查找的 HTML 標籤
    :param attr: 要提取的屬性名稱（如 'href'），若為 None，則返回文本
    :param kwargs: 其他要查找的屬性，比如 id、class 等
    :return: 抓取的標籤文本或屬性值列表
    """
    tagLIST = soup.find_all(tag, **kwargs)
    if tagLIST:
        if attr:
            textLIST = [t.get(attr) for t in tagLIST]
            textSTR = " ".join(textLIST)
            return textSTR
        else:
            textLIST = [t.get_text().replace("\n", "").replace(" ", "") for t in tagLIST]  # 去除換行和空格
            tagSTR = "；".join(textLIST)  # 用「；」將所有文本串聯成一個字符串
            return tagSTR               
    else:
        return f"Not Provided"    
    

def get_compInfo(url):
    resultLIST = []
    # 使用瀏覽器驅動
    driver = webdriver.Chrome()
    driver.get(url)
    
    # 等待頁面加載完成
    driver.implicitly_wait(15)
    # 獲取動態加載的 HTML
    htmlSTR = driver.page_source
    driver.quit()
    soup = BeautifulSoup(htmlSTR, "lxml")
    
    # 使用統一的 scrapeTag 函數來抓取不同的標籤
    comp_nameSTR = scrapeTag(soup, "h2", id="info-name", class_="fz-B")                                     #公司名稱
    dateSTR = scrapeTag(soup, "div", class_="found-date content-holder")                                    #成立時間
    comp_idSTR = scrapeTag(soup, "div", class_="company-id content-holder")                                 #統一編號
    statusSTR = scrapeTag(soup, "div", class_="company-companyStatus content-holder")                       #公司狀態
    mem_numSTR = scrapeTag(soup, "div", class_="member-num content-holder")                                 #團隊人數
    moneySTR = scrapeTag(soup, "span", id="ContentPlaceHolder_CompanyInfoPlaceHolder_money")                #實收資本額   
    founderSTR = scrapeTag(soup, "div", class_="founder content-holder")                                    #負責人
    categorySTR = scrapeTag(soup, "div", class_="category content-holder")                                  #主分類
    linkSTR = scrapeTag(soup, "a", attr="href", class_="a-link")                                            #官方網站
    patentSTR = "；".join([scrapeTag(soup, "a", attr=None, **{"data-target": f"#modal-patent{i}"}) for i in range(4)])#專利狀況
    productSTR = scrapeTag(soup, "div", class_="product content-holder")                                 #產品/服務簡介
    #productLIST = [p.replace("\n", "").replace(" ", "") for p in productLIST]
    comp_introSTR = scrapeTag(soup, "div", class_="company-intro content-holder")                           #公司簡介
    locationSTR = scrapeTag(soup, "div", class_="location content-holder")                                  #公司註冊地址    

    resultLIST = [
    {
        "公司名稱": comp_nameSTR,
        "成立時間": dateSTR,
        "統一編號": comp_idSTR,
        "公司狀態": statusSTR,
        "團隊人數": mem_numSTR,
        "實收資本額(元/新台幣)": moneySTR,
        "負責人": founderSTR,
        "主分類": categorySTR,
        "官方網站": linkSTR,
        "專利狀況": patentSTR,
        "產品/服務簡介": productSTR,
        "公司簡介": comp_introSTR,
        "公司註冊地址": locationSTR
        
    }
    ]
    
    return resultLIST

def get_compLink(url):
    compLIST = []
    # 使用瀏覽器驅動
    driver = webdriver.Chrome()
    driver.get(url)
    
    sleep(60)
    # 獲取動態加載的 HTML
    htmlSTR = driver.page_source
    driver.quit()
    soup = BeautifulSoup(htmlSTR, "lxml")
    compTag = soup.find_all("div", class_="col-12 col-lg-3 main-title")
    for c in compTag:
        link = c.find("a").get("href")
        compLIST.append(link)
    return compLIST

def load_jsonFILE(jsonFILE, company_resultLIST):
    if os.path.exists(jsonFILE):
        with open (jsonFILE, "r", encoding="utf-8") as f:
            try:
                all_resultLIST = json.load(f)
            except json.JSONDecodeError:
                all_resultLIST = []
    else:
        all_resultLIST = []
    
    all_resultLIST.extend(company_resultLIST)
    with open (jsonFILE, "w", encoding="utf-8") as f:
        json.dump(all_resultLIST, f, ensure_ascii=False, indent=4)
    
    return all_resultLIST

def get_companyjsonFILE(i, company_i, company_resultLIST):
    company_jsonFILE = f"../../corpus/company/company_{company_i}.json"
    with open(company_jsonFILE, "w", encoding="utf-8") as f:
        json.dump(company_resultLIST, f, ensure_ascii=False, indent=4)

def get_pagejsonFILE(i, page_resultLIST):
    page_jsonFILE = f"../../corpus/page/page_{i + 1}.json"
    with open(page_jsonFILE, "w", encoding="utf-8") as f:
        json.dump(page_resultLIST, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    jsonFILE = "../../corpus/FINDIT_LIST.json"
    
    if os.path.exists(jsonFILE):
        os.remove(jsonFILE)
        
    all_resultLIST = []
    
    company_i = 1
    for i in range(0, 64): #在這裡循環每一頁
        url = f"https://findit.org.tw/twCompanyList.aspx?strSortColumn=strFundDate&strSortDirection=descending&intPageIndex={i}&intCountPerPage=50"
        compLIST = get_compLink(url)    #每次迴圈都抓取該頁的公司連結
        pprint(compLIST)

        page_resultLIST = []
        for c in compLIST:  #使用抓取到的公司連結進一步抓取公司資訊
            url = "https://findit.org.tw/" + c
            company_resultLIST = get_compInfo(url)
            companyjsonFILE = get_companyjsonFILE(i, company_i, company_resultLIST)
            company_i += 1
            page_resultLIST.extend(company_resultLIST)
            pprint(company_resultLIST)
            all_resultLIST = load_jsonFILE(jsonFILE, company_resultLIST)    # 將該公司的資料合併到總資料中
            
        pagejsonFILE = get_pagejsonFILE (i, page_resultLIST)    # 儲存該頁的 JSON 檔案
        pprint(all_resultLIST)
    
