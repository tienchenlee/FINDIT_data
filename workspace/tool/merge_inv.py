#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import glob
import json
import os

from pprint import pprint

def to_FINDIT_invLIST(jsonFILE):
    """
    匯總所有公司資訊並保存到一個 JSON 檔案。

    參數：
        jsonFILE (str): 匯總後 JSON 檔案的路徑。

    功能：
        - 遍歷存儲公司資訊的資料夾，載入每個公司資訊 JSON 檔案的數據。
        - 匯總所有公司的資訊並保存到指定的 JSON 檔案中。
    """    
    company_folder = "./crawler_result/FINDIT_invest/"
    all_resultLIST = []
    for company_jsonFILE in glob.glob(os.path.join(company_folder, "company_*.json")):
        with open(company_jsonFILE, "r", encoding="utf-8") as f:
            companyLIST = json.load(f)
            all_resultLIST.extend(companyLIST)

    with open(jsonFILE, "w", encoding="utf-8") as f:
        json.dump(all_resultLIST, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    jsonFILE = "./crawler_result/FINDIT_invest/FINDIT_invLIST.json"
    
    if os.path.exists(jsonFILE):
        os.remove(jsonFILE)
   
    missingLIST = []  # 用來記錄缺少的檔案
    all_resultLIST = []
    
    company_i = 1  # 從第 1 公司開始
    while company_i <= 1460:  # 總公司數不超過 1460 家
        company_FILEname = f"./crawler_result/FINDIT_invest/company_{company_i}.json"
        if os.path.exists(company_FILEname):    #檔案已存在就跳下一個 company_i
            print(f"{company_FILEname} already exists, skipping...")
            company_i += 1
            continue
        else:
            missingLIST.append(company_FILEname)
        
        company_i += 1
    
    if missingLIST:
        pprint(f"missing files: {missingLIST}")
    
    to_FINDIT_invLIST(jsonFILE)