#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import os

from bs4 import BeautifulSoup
from pprint import pprint
from selenium import webdriver
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
    

def get_compInfo(comp_url):
    """
    從指定的公司網址抓取公司資訊。

    使用瀏覽器驅動訪問網頁，等待頁面加載後，提取並解析 HTML 內容，然後抓取所需的公司資訊，包括公司名稱、成立時間、統一編號、公司狀態等。

    參數:
        comp_url (str): 目標公司網頁的 URL。

    返回:
        list: 包含公司資訊的字典列表。
    """
    resultLIST = []
    # 使用瀏覽器驅動
    driver = webdriver.Firefox()
    driver.get(comp_url)
    
    # 等待頁面加載完成
    #driver.implicitly_wait(15)
    sleep(30)
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

def get_compLink(page_url):
    """
    從指定的公司列表頁面抓取所有公司連結。

    使用瀏覽器驅動訪問網頁，等待頁面加載後，提取並解析 HTML 內容，然後抓取所有公司連結，將其存入列表中。

    參數:
        page_url (str): 目標公司列表頁面的 URL。

    返回:
        list: 包含公司連結的列表。
    """
    compLIST = []
    # 使用瀏覽器驅動
    driver = webdriver.Firefox()
    driver.get(page_url)
    
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

def get_companyjsonFILE(start_page, company_i, company_resultLIST):
    """
    將指定公司的資訊儲存為 JSON 檔案。
    
    參數：
        start_page (int): 頁碼索引。
        company_i (int): 公司編號。
        company_resultLIST (list): 包含公司資訊的列表。

    功能：
        - 將公司的資訊儲存到對應的 JSON 檔案中，檔案名稱格式為 "company_{company_i}.json"。
    """
    # 確保資料夾存在，如果不存在則創建
    company_folder = "../../corpus/company"
    if not os.path.exists(company_folder):
        os.makedirs(company_folder)

    company_jsonFILE = f"../../corpus/company/company_{company_i}.json"
    with open(company_jsonFILE, "w", encoding="utf-8") as f:
        json.dump(company_resultLIST, f, ensure_ascii=False, indent=4)

def get_pagejsonFILE(page_number, page_resultLIST):
    """
    將指定頁面的公司資訊儲存為 JSON 檔案。

    參數：
        page_number (int): 頁碼索引。
        page_resultLIST (list): 包含該頁所有公司資訊的列表，每頁 50 個公司。

    功能：
        - 將頁面資訊儲存到對應的 JSON 檔案中，檔案名稱格式為 "page_{page_number}.json"。
    """
    page_folder = "../../corpus/page"
    if not os.path.exists(page_folder):
        os.makedirs(page_folder)    
    
    page_jsonFILE = f"../../corpus/page/page_{page_number}.json"
    with open(page_jsonFILE, "w", encoding="utf-8") as f:
        json.dump(page_resultLIST, f, ensure_ascii=False, indent=4)

def to_FINDIT_LIST(jsonFILE):
    """
    匯總所有公司資訊並保存到一個 JSON 檔案。

    參數：
        jsonFILE (str): 匯總後 JSON 檔案的路徑。

    功能：
        - 遍歷存儲公司資訊的資料夾，載入每個公司資訊 JSON 檔案的數據。
        - 匯總所有公司的資訊並保存到指定的 JSON 檔案中。
    """    
    company_folder = "../../corpus/company"
    all_resultLIST = []
    for company_jsonFILE in os.listdir(company_folder):
        if company_jsonFILE.startswith("company_") and company_jsonFILE.endswith(".json"):
            with open(os.path.join(company_folder, company_jsonFILE), "r", encoding="utf-8") as f:
                companyLIST = json.load(f)
                all_resultLIST.extend(companyLIST)
    
    with open(jsonFILE, "w", encoding="utf-8") as f:
        json.dump(all_resultLIST, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    jsonFILE = "../../corpus/FINDIT_LIST.json"
    
    if os.path.exists(jsonFILE):
        os.remove(jsonFILE)
   
    all_resultLIST = []
    page_resultLIST = []
    company_i = 1  # 從第 1 公司開始
    while company_i <= 9576:  # 假設總公司數不超過 192 頁 * 50
        company_FILEname = f"../../corpus/company/company_{company_i}.json"
        if os.path.exists(company_FILEname):    #檔案已存在就跳下一個 company_i
            print(f"{company_FILEname} already exists, skipping...")
            company_i += 1
            continue

        start_page_idx = (company_i - 1) // 50  #page 的 idx 是從 0 開始，也就是 page 1 的 idx 是 0
        page_url = f"https://findit.org.tw/twCompanyList.aspx?strSortColumn=strFundDate&strSortDirection=descending&intPageIndex={start_page_idx}&intCountPerPage=50"
        compLIST = get_compLink(page_url)  # 每次迴圈抓取該頁的公司連結
        pprint(compLIST)
        
        for c_index, c_link in enumerate(compLIST):
            if c_index + 1 != (company_i - 1) % 50 + 1:
                continue
                
            comp_url = "https://findit.org.tw/" + c_link
            company_resultLIST = get_compInfo(comp_url)
            companyjsonFILE = get_companyjsonFILE(start_page_idx, company_i, company_resultLIST)
            company_i += 1
            
            #page_resultLIST.extend(company_resultLIST)   
            ## 每 50 個公司儲存一個 page_jsonFILE
            #if company_i % 50 == 1 or company_i == 9576:
                #page_number = ((company_i - 1) // 50) + 1
                #get_pagejsonFILE(page_number, page_resultLIST)
                #page_resultLIST = []  # 重置頁面列表
                
            break
            
    to_FINDIT_LIST(jsonFILE)
