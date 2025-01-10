#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import os
from bs4 import BeautifulSoup
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By
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
    tags = soup.find_all(tag, **kwargs)
    if tags:
        if attr:
            tagSTR = [t.get(attr) for t in tags]
        else:
            tagSTR = [t.get_text() for t in tags]
        return tagSTR
    else:
        return f"No matching tags found for tag: {tag}"    
    

def get_compInfo(url):
    resultLIST = []
    # 使用瀏覽器驅動
    driver = webdriver.Chrome()
    driver.get(url)
    
    # 等待頁面加載完成
    driver.implicitly_wait(50)
    # 獲取動態加載的 HTML
    htmlSTR = driver.page_source
    driver.quit()
    soup = BeautifulSoup(htmlSTR, "lxml")
    
    # 使用統一的 scrape_tag 函數來抓取不同的標籤
    comp_nameLIST = scrapeTag(soup, "h2", id="info-name", class_="fz-B")                                     #公司名稱
    dateLIST = scrapeTag(soup, "div", class_="found-date content-holder")                                    #成立時間
    comp_idLIST = scrapeTag(soup, "div", class_="company-id content-holder")                                 #統一編號
    statusLIST = scrapeTag(soup, "div", class_="company-companyStatus content-holder")                       #公司狀態
    mem_numLIST = scrapeTag(soup, "div", class_="member-num content-holder")                                 #團隊人數
    moneyLIST = scrapeTag(soup, "span", id="ContentPlaceHolder_CompanyInfoPlaceHolder_money")                #實收資本額   
    founderLIST = scrapeTag(soup, "div", class_="founder content-holder")                                    #負責人
    categoryLIST = scrapeTag(soup, "div", class_="category content-holder")                                  #主分類
    linkLIST = scrapeTag(soup, "a", attr="href", class_="a-link")                                            #官方網站
    patentLIST = [scrapeTag(soup, "a", attr=None, **{"data-target": f"#modal-patent{i}"}) for i in range(4)]#專利狀況
    productLIST = scrapeTag(soup, "div", class_="product content-holder")                                 #產品/服務簡介
    productLIST = [p.replace("\n", " ") for p in productLIST]
    comp_introLIST = scrapeTag(soup, "div", class_="company-intro content-holder")                           #公司簡介
    locationLIST = scrapeTag(soup, "div", class_="location content-holder")                                  #公司註冊地址    

    resultLIST = [
    {
        "公司名稱": comp_nameLIST,
        "公司資訊": [
            {"成立時間": dateLIST},
            {"統一編號": comp_idLIST},
            {"公司狀態": statusLIST},
            {"團隊人數": mem_numLIST},
            {"實收資本額(元/新台幣)": moneyLIST},
            {"負責人": founderLIST},
            {"主分類": categoryLIST},
            {"官方網站": linkLIST},
            {"專利狀況": patentLIST},
            {"產品/服務簡介": productLIST},
            {"公司簡介": comp_introLIST},
            {"公司註冊地址": locationLIST}
        ]
    }
    ]
    
    return resultLIST

def get_compLink(url):
    compLIST = []
    # 使用瀏覽器驅動
    driver = webdriver.Chrome()
    driver.get(url)
    
    # 等待頁面加載完成
    #driver.implicitly_wait(120)
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

def load_jsonFILE(jsonFILE):
    if os.path.exists(jsonFILE):
        with open (jsonFILE, "r", encoding="utf-8") as f:
            try:
                all_resultLIST = json.load(f)
            except json.JSONDecodeError:
                all_resultLIST = []
    else:
        all_resultLIST = []
    
    all_resultLIST.extend(resultLIST)
    with open (jsonFILE, "w", encoding="utf-8") as f:
        json.dump(all_resultLIST, f, ensure_ascii=False, indent=4)
    
    return all_resultLIST

if __name__ == "__main__":   
    url = "https://findit.org.tw/twCompanyList.aspx"
    compLIST = get_compLink(url)
    pprint(compLIST)
    jsonFILE = "../../corpus/FINDIT_LIST.json"
    all_resultLIST = []
    for c in compLIST:
        url = "https://findit.org.tw/" + c
        resultLIST = get_compInfo(url)
        #pprint(resultLIST)
        all_resultLIST = load_jsonFILE(jsonFILE)
        pprint(all_resultLIST)
    
