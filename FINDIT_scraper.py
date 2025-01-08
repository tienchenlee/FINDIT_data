#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.by import By

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
    

def main(url):
    resultLIST = []
    # 使用瀏覽器驅動
    driver = webdriver.Chrome()
    driver.get(url)
    
    # 等待頁面加載完成
    driver.implicitly_wait(10)
    
    # 獲取動態加載的 HTML
    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, "lxml")
    
    # 使用統一的 scrape_tag 函數來抓取不同的標籤
    comp_nameSTR = scrapeTag(soup, "h2", id="info-name", class_="fz-B")                                     #公司名稱
    dateSTR = scrapeTag(soup, "div", class_="found-date content-holder")                                    #成立時間
    comp_idSTR = scrapeTag(soup, "div", class_="company-id content-holder")                                 #統一編號
    statusSTR = scrapeTag(soup, "div", class_="company-companyStatus content-holder")                       #公司狀態
    mem_numSTR = scrapeTag(soup, "div", class_="member-num content-holder")                                 #團隊人數
    moneySTR = scrapeTag(soup, "span", id="ContentPlaceHolder_CompanyInfoPlaceHolder_money")                #實收資本額   
    founderSTR = scrapeTag(soup, "div", class_="founder content-holder")                                    #負責人
    categorySTR = scrapeTag(soup, "div", class_="category content-holder")                                  #主分類
    linkSTR = scrapeTag(soup, "a", attr="href", class_="a-link")                                            #官方網站
    patentLIST = [scrapeTag(soup, "a", attr=None, **{"data-target": f"#modal-patent{i}"}) for i in range(4)]#專利狀況
    productSTR = scrapeTag(soup, "div", class_="product content-holder")                                    #產品/服務簡介
    comp_introSTR = scrapeTag(soup, "div", class_="company-intro content-holder")                           #公司簡介
    locationSTR = scrapeTag(soup, "div", class_="location content-holder")                                  #公司註冊地址    

    resultLIST = [
        {
        "公司名稱": comp_nameSTR,
        "公司資訊": [
            {"成立時間": dateSTR},
            {"統一編號": comp_idSTR},
            {"公司狀態": statusSTR},
            {"團隊人數": mem_numSTR},
            {"實收資本額(元/新台幣)": moneySTR},
            {"負責人": founderSTR},
            {"主分類": categorySTR},
            {"官方網站": linkSTR},
            {"專利狀況": patentLIST},
            {"產品/服務簡介": productSTR},
            {"公司簡介": comp_introSTR},
            {"公司註冊地址": locationSTR}
        ]
    }
    ]
    return resultLIST


if __name__ == "__main__":
    url = "https://findit.org.tw/twCompanyInfo.aspx?strId=5967"
    #url = "https://findit.org.tw/twCompanyList.aspx"
    result = main(url)
    pprint(result)
    