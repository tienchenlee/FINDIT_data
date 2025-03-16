#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import json
import os

from bs4 import BeautifulSoup
from pprint import pprint
from selenium import webdriver
from time import sleep

def scrapeTag(soup, tag, attr=None, nested_tag=None, nested_attr=None, h4_class=None, **kwargs):
    """
    抓取指定的標籤和屬性，返回所有匹配的內容或屬性值。
    
    :param soup: BeautifulSoup 解析過的頁面
    :param tag: 要查找的 HTML 標籤
    :param attr: 要提取的屬性名稱（如 'href'），若為 None，則返回文本
    :param nested_tag: 內部標籤（若要提取內部標籤的內容）
    :param nested_attr: 內部標籤的屬性名稱（如 'href'）
    :param h4_class: 需要刪除的 h4 標籤的 class 名稱 (可選)
    :param kwargs: 其他要查找的屬性，比如 id、class 等
    :return: 抓取的標籤文本或屬性值列表
    """
    # 如果指定了 h4_class，就刪除該 class 的 <h4>
    if h4_class:
        for h4_tag in soup.find_all("h4", class_="fz-C history"):
            h4_tag.decompose()
    
    tagLIST = soup.find_all(tag, **kwargs)
    if tagLIST:
        if nested_tag and nested_attr:  # 提取內部標籤的屬性
            textLIST = []
            for t in tagLIST:
                innerLIST = [n.get(nested_attr) for n in t.find_all(nested_tag) if n.get(nested_attr)]
                textLIST.extend(innerLIST)

            # 在每個連結前面加上完整網址
            textLIST = [f"https://findit.org.tw{url}" for url in textLIST]
            return textLIST
        
        elif attr:
            textLIST = [t.get(attr) for t in tagLIST]
            textSTR = " ".join(textLIST)
            return "" if textSTR == "-" else textSTR    # 如果是 "-"，則回傳空字串 ""
            
        else:
            textLIST = [t.get_text().replace("\n", "") for t in tagLIST]  # 去除換行
            textSTR = "；".join(textLIST)  # 用「；」將所有文本串聯成一個字符串
            return "" if textSTR == "-" else textSTR    # 如果是 "-"，則回傳空字串 ""            
    
    else:
        return f""   
    

def get_compInfo(comp_url):
    """
    從指定的公司網址抓取公司資訊。

    參數:
        comp_url (str): 目標公司網頁的 URL。

    返回:
        list: 包含公司資訊的字典列表。
    """    
    resultLIST = []
    # 使用瀏覽器驅動
    #driver = webdriver.Firefox()
    driver = webdriver.Chrome()
    driver.get(comp_url)
    
    # 等待頁面加載完成
    sleep(30)
    # 獲取動態加載的 HTML
    htmlSTR = driver.page_source
    driver.quit()
    soup = BeautifulSoup(htmlSTR, "lxml")
    
    # 使用統一的 scrapeTag 函數來抓取不同的標籤
    comp_nameSTR = scrapeTag(soup, "h2", id="info-name", class_="fz-B")                            #公司名稱
    eng_nameSTR = scrapeTag(soup, "h4", id="info-nameEN", class_="fz-D")                           #公司英文名稱
    typeSTR = scrapeTag(soup, "span", id="ContentPlaceHolder_CompanyInfoPlaceHolder_LabelOutput")  #投資者類型
    stageSTR = scrapeTag(soup, "div", class_="invest-stage content-holder")                        #投資階段
    tagSTR = scrapeTag(soup, "div", class_="invest-tag content-holder")                            #主要投資領域
    scaleSTR = scrapeTag(soup, "div", class_="invest-scale content-holder")                        #投資規模
    areaSTR = scrapeTag(soup, "div", class_="invest-area content-holder")                          #投資地區   
    linkSTR = scrapeTag(soup, "a", attr="href", class_="a-link")                                   #官方網站    
    introSTR = scrapeTag(soup, "div", id="info-history", class_="info-section", h4_class="fz-C history")    #投資機構簡介
    caseSTR = scrapeTag(soup, "div", id="info-history-2", class_="info-section", h4_class="fz-C history")   #投資案例   
    case_linkSTR = scrapeTag(soup, "div", id="info-history-2", class_="info-section", nested_tag="a", nested_attr="href")   #投資案例連結

    resultLIST = [
    {
        "公司名稱": comp_nameSTR,        
        "公司英文名稱": eng_nameSTR,                
        "投資者類型": typeSTR,
        "投資階段": stageSTR,
        "主要投資領域": tagSTR,
        "投資規模": scaleSTR,
        "投資地區": areaSTR,
        "官方網站": linkSTR,
        "投資機構簡介": introSTR,
        "投資案例": caseSTR,
        "投資案例連結": case_linkSTR,
        
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
    #driver = webdriver.Firefox()
    driver = webdriver.Chrome()
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

def get_companyjsonFILE(start_page_idx, company_i, company_resultLIST):
    """
    將指定公司的資訊儲存為 JSON 檔案。
    
    參數：
        start_page_idx (int): 頁碼索引。
        company_i (int): 公司編號。
        company_resultLIST (list): 包含公司資訊的列表。

    功能：
        - 將公司的資訊儲存到對應的 JSON 檔案中，檔案名稱格式為 "company_{company_i}.json"。
    """    
    # 確保資料夾存在，如果不存在則創建
    company_folder = "./crawler_result/FINDIT_invest/"
    if not os.path.exists(company_folder):
        os.makedirs(company_folder)
        
    company_jsonFILE = f"./crawler_result/FINDIT_invest/company_{company_i}.json"
    with open(company_jsonFILE, "w", encoding="utf-8") as f:
        json.dump(company_resultLIST, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    all_resultLIST = []
    
    company_i = 501
    while company_i <= 1000:  #處理11～20頁
        company_FILEname = f"./crawler_result/FINDIT_invest/company_{company_i}.json"
        if os.path.exists(company_FILEname):    #檔案已存在就跳下一個 company_i
            print(f"{company_FILEname} already exists, skipping...")
            company_i += 1
            continue
            
        start_page_idx = (company_i - 1) // 50  #page 的 idx 是從 0 開始，也就是 page 1 的 idx 是 0
        page_url = f"https://findit.org.tw/twInvestorList.aspx?strSortColumn=strInvestorName&strSortDirection=descending&intPageIndex={start_page_idx}&intCountPerPage=50"
        compLIST = get_compLink(page_url)  # 每次迴圈抓取該頁的公司連結
        pprint(compLIST)
        
        for c_index, c_link in enumerate(compLIST): #確保 company_i 確實在 compLIST（該頁的公司列表）內
            if c_index + 1 != (company_i - 1) % 50 + 1:
                continue
                
            comp_url = "https://findit.org.tw/" + c_link
            company_resultLIST = get_compInfo(comp_url)
            pprint(company_resultLIST)
            
            companyjsonFILE = get_companyjsonFILE(start_page_idx, company_i, company_resultLIST)
            company_i += 1        