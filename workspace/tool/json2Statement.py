#!/usr/bin/env python3
# -*- coding:utf-8 -*-


import re
purgePAT = re.compile("\([^\)]+\)")

from pprint import pprint

def main(itemNameSTR, itemDICT):
    """
    輸入：itemNameSTR
    輸出：LIST [statementSTR, ...]

    main()
    itemNameSTR 做為主詞，接上「的」和 itemDICT 的 key，再加上「是」和 itemDICT 的 value，
    結構：itemNameSTR的itemDICT.key是itemDICT.value
    範例：隆順綠能科技股份有限公司 的 成立時間 是 2017
    """
    resultDICT = {"name"       : [], #公司名稱
                  "setup_time" : [], #成立時間
                  "tax_num"    : [], #統一編號
                  "status"     : [], #公司狀態
                  "team_num"   : [], #團隊人數
                  "capital"    : [], #實收資本額
                  "owner"      : [], #負責人
                  "category"   : [], #主分類
                  "website"    : [], #官方網站
                  "patent_all" : [], #專利總數
                  "patent_dsc" : [], #發明專利
                  "patent_mdl" : [], #新型專利
                  "patent_dsn" : [], #設計專利
                  "product"    : [], #產品/服務簡介
                  "address"    : []  #公司註冊地址
                  }
    aliasLIST = []
    for i_s in ("股份", "科技"):
        aliasLIST.append(itemNameSTR.split(i_s)[0])
    for i_s in itemDICT.keys():
        #print(f"{itemNameSTR}的{i}是{itemDICT[i_s]}")
        if i_s.startswith("公司名稱"):
            resultDICT["name"].append(f"{itemNameSTR}的{i_s}是{itemDICT[i_s]}")
            for a_s in aliasLIST:
                resultDICT["name"].append(f"{a_s}的{i_s}是{itemDICT[i_s]}")
        elif i_s.startswith("成立時間"):
            resultDICT["setup_time"].append(f"{itemNameSTR}的{i_s}是 {itemDICT[i_s]}")
            if len(itemDICT[i_s]) == 4:
                resultDICT["setup_time"].append(f"{itemNameSTR}的{i_s}是 {itemDICT[i_s]}年")
            for a_s in aliasLIST:
                resultDICT["setup_time"].append(f"{a_s}的{i_s}是{itemDICT[i_s]}")
        elif i_s.startswith("統一編號"):
            resultDICT["tax_num"].append(f"{itemNameSTR}的{i_s}是{itemDICT[i_s]}")
            for a_s in aliasLIST:
                resultDICT["tax_num"].append(f"{a_s}的{i_s}是{itemDICT[i_s]}")
        elif i_s.startswith("公司狀態"):
            resultDICT["status"].append(f"{itemNameSTR}的{i_s}是{itemDICT[i_s]}")
            for a_s in aliasLIST:
                resultDICT["status"].append(f"{a_s}的{i_s}是{itemDICT[i_s]}")
        elif i_s.startswith("團隊人數"):
            resultDICT["team_num"].append(f"{itemNameSTR}的{i_s}是{itemDICT[i_s]}")
            for a_s in aliasLIST:
                resultDICT["team_num"].append(f"{a_s}的{i_s}是{itemDICT[i_s]}")
        elif i_s.startswith("實收資本額"):
            resultDICT["team_num"].append(f"{itemNameSTR}的{purgePAT.sub('', i_s)}是{itemDICT[i_s]}")
            resultDICT["team_num"].append(f"{itemNameSTR}的{purgePAT.sub('', i_s)}是{itemDICT[i_s]}元")
            resultDICT["team_num"].append(f"{itemNameSTR}的{purgePAT.sub('', i_s)}是新台幣{itemDICT[i_s]}元")
            for a_s in aliasLIST:
                resultDICT["team_num"].append(f"{a_s}的{i_s}是{itemDICT[i_s]}")
                resultDICT["team_num"].append(f"{a_s}的{i_s}是{itemDICT[i_s]}元")
                resultDICT["team_num"].append(f"{a_s}的{i_s}是新台幣{itemDICT[i_s]}元")
        elif i_s.startswith("負責人"):
            resultDICT["owner"].append(f"{itemNameSTR}的{i_s}是{itemDICT[i_s]}")
            for a_s in aliasLIST:
                resultDICT["owner"].append(f"{a_s}的{i_s}是{itemDICT[i_s]}")
        elif i_s.startswith("主分類"):
            resultDICT["category"].append(f"{itemNameSTR}的{i_s}是 {itemDICT[i_s]}")
            for a_s in aliasLIST:
                resultDICT["category"].append(f"{a_s}的{i_s}是 {itemDICT[i_s]}")
        elif i_s.startswith("官方網站"):
            resultDICT["website"].append(f"{itemNameSTR}的{i_s}是 {itemDICT[i_s]}")
            for a_s in aliasLIST:
                resultDICT["website"].append(f"{a_s}的{i_s}是 {itemDICT[i_s]}")
        elif i_s.startswith("專利狀況"):
            itemDICT[i_s] = itemDICT[i_s].replace("︰", "：")
            resultDICT["patent_all"].append(f"{itemNameSTR}的專利總數是{itemDICT[i_s].split('；')[0].split('：')[1]}")
            resultDICT["patent_all"].append(f"{itemNameSTR}的專利總數是{itemDICT[i_s].split('；')[0].split('：')[1]}件")
            for a_s in aliasLIST:
                resultDICT["patent_all"].append(f"{a_s}的專利總數是{itemDICT[i_s].split('；')[0].split('：')[1]}")
                resultDICT["patent_all"].append(f"{a_s}的專利總數是{itemDICT[i_s].split('；')[0].split('：')[1]}件")

            resultDICT["patent_dsc"].append(f"{itemNameSTR}的發明專利總數是{itemDICT[i_s].split('；')[1].split('：')[1]}")
            resultDICT["patent_dsc"].append(f"{itemNameSTR}的發明專利總數是{itemDICT[i_s].split('；')[1].split('：')[1]}件")
            for a_s in aliasLIST:
                resultDICT["patent_dsc"].append(f"{a_s}的發明專利總數是{itemDICT[i_s].split('；')[1].split('：')[1]}")
                resultDICT["patent_dsc"].append(f"{a_s}的發明專利總數是{itemDICT[i_s].split('；')[1].split('：')[1]}件")

            resultDICT["patent_mdl"].append(f"{itemNameSTR}的新型專利總數是{itemDICT[i_s].split('；')[2].split('：')[1]}")
            resultDICT["patent_mdl"].append(f"{itemNameSTR}的新型專利總數是{itemDICT[i_s].split('；')[2].split('：')[1]}件")
            for a_s in aliasLIST:
                resultDICT["patent_mdl"].append(f"{a_s}的新型專利總數是{itemDICT[i_s].split('；')[2].split('：')[1]}")
                resultDICT["patent_mdl"].append(f"{a_s}的新型專利總數是{itemDICT[i_s].split('；')[2].split('：')[1]}件")

            resultDICT["patent_dsn"].append(f"{itemNameSTR}的設計專利總數是{itemDICT[i_s].split('；')[3].split('：')[1]}")
            resultDICT["patent_dsn"].append(f"{itemNameSTR}的設計專利總數是{itemDICT[i_s].split('；')[3].split('：')[1]}件")
            for a_s in aliasLIST:
                resultDICT["patent_dsn"].append(f"{a_s}的設計專利總數是{itemDICT[i_s].split('；')[3].split('：')[1]}")
                resultDICT["patent_dsn"].append(f"{a_s}的設計專利總數是{itemDICT[i_s].split('；')[3].split('：')[1]}件")

        elif i_s.startswith("產品/服務簡介"):
            resultDICT["product"].append(f"{itemNameSTR}的{i_s}是{itemDICT[i_s]}")
            for a_s in aliasLIST:
                resultDICT["product"].append(f"{a_s}的{i_s}是{itemDICT[i_s]}")
        elif i_s.startswith("公司註冊地址"):
            resultDICT["address"].append(f"{itemNameSTR}的{i_s}是{itemDICT[i_s]}")
            for a_s in aliasLIST:
                resultDICT["address"].append(f"{a_s}的{i_s}是{itemDICT[i_s]}")

    return resultDICT


if __name__ == "__main__":
    devLIST = [{"公司名稱": "隆順綠能科技股份有限公司/LONGSHUNGREENENERGYTECHNOLOGYLTD.",
                "成立時間": "2017",
                "統一編號": "59276799",
                "公司狀態": "核准設立",
                "團隊人數": "未揭露",
                "實收資本額(元/新台幣)": "380,000,000",
                "負責人": "陳俊宇",
                "主分類": "Sustainability",
                "官方網站": "https://www.longshun.eco/",
                "專利狀況": "公告專利總數︰14；發明專利︰7；新型專利︰7；設計專利︰0",
                "產品/服務簡介": "固體回收燃料&固體廢棄物衍生燃料",
                "公司簡介": "隆順綠能科技股份有限公司是整合廢棄物資源化再利用、技術與設備整合及互聯網應用等高度專業之團隊，是由台灣的國立高雄科技大學廢棄物處理與資源化研究單位博士級研究人員所發起，其技術團隊因結合環境工程研究機構之背景，因此具科研資源豐厚之優勢，技術研發實力堅強，且長期接受政府相關單位委託，以及民間企業諮詢，進行許多環境工程之專案，對廢棄物處理、再利用及資源化之相關經驗豐富，在台灣部分固體廢棄物之回收、中間處理及最終處置之相關法規即是由此團隊核心成員。",
                "公司註冊地址": "高雄市梓官區中正路118號"
                }
               ]
    resultLIST = []
    for i in devLIST:
        itemNameSTR = i["公司名稱"]
        resultLIST.append(main(itemNameSTR, i))
    pprint(resultLIST)