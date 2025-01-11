#ライブラリ読み込み
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import urllib
import os
import json
import sys
import time

#サイト内の章ごとのリンク
#listVer = ["P01","P02","P03","P04","P05","P06","2P01","2P03","2P05","2P07","3P01","3P02"]
listVer = ["3P02"]

#ファイル用連想配列初期化
dict_data = {}#コーデアイテムの連想配列
dict_RareNumber = {}#コーデアイテムのインデックス番号用の連想配列(現在未使用)

def fileRoad(dict_data):
    #CoordinationのJsonファイルを読み込む
    if os.path.isfile("./" + "Coordination.json") :
        with open("./" + "Coordination.json", "r",encoding = "utf-8")  as file:
            dict_data = json.load(file)    
    else:
        with open("./" + "Coordination.json", "w",encoding = "utf-8")  as file:
            dict_data = {}
            for i in range(1,10,1):
                dict_data.setdefault(str(i),[])
            json.dump(dict_data,file,indent = 2,ensure_ascii=False)
    return dict_data

    # #RareNumberのJsonファイルを読み込む
    # if os.path.isfile("./" + "RareNumber.json") :
    #     with open("./" + "RareNumber.json", "r",encoding = "utf-8")  as file:
    #         dict_RareNumber = json.load(file)    
    # else:
    #     with open("./" + "RareNumber.json", "w",encoding = "utf-8")  as file:
    #             dict_RareNumber = {"rare4":-1}

def fileWrite(dict_data):
    # #レア度ごと(集計ごと)の通し番号のJsonファイル更新
    # with open("./" + "RareNumber.json", "w",encoding = "utf-8")  as file:
    #     json.dump(dict_RareNumber,file,indent = 2,ensure_ascii=False)

    #コーデの情報のJson更新
    with open("./" + "Coordination.json", "w",encoding = "utf-8")  as file:
        json.dump(dict_data,file,indent = 2,ensure_ascii=False)

    #コーデの情報のJsonをJSに変換して変更
    with open("./" + "Coordination.json","r",encoding = "utf-8") as file:
        s = file.read()
        with open ("./" + "Coordination.js", "w",encoding = "utf-8") as file:
            file.write("let item =")
            file.write(s)


def download():

    #ファイル用連想配列初期化
    dict_data = {}#コーデアイテムの連想配列
    dict_RareNumber = {}#コーデアイテムのインデックス番号用の連想配列(現在未使用)

    #保存用Jsonの取得
    dict_data = fileRoad(dict_data)

    #クロームの立ち上げ
    driver=webdriver.Chrome()
    
    flag = 0

    #章ごとのループ
    for ver in listVer:
        url  =  "https://www.takaratomy-arts.co.jp/specials/primagi/item/" + ver + "/"
        driver.get(url)
        
        #コーデ詳細用の配列の初期化
        listDetailHref = []
        listCoordName = []
        listImgUrl = []
        
        #同一章内のセクション要素を取得してループを回す
        sectionElements = driver.find_elements(By.XPATH,"/html/body/div[2]/div[2]/div[1]/div[2]/div[3]/div/div[6]/div")
        for sectionElement in sectionElements:

            #コーデの塊の要素とその背景が交互にdivで並んでいるため奇数回はスキップ
            flag = flag + 1    
            if flag % 2 ==0 :

                f = 0
                #セクションから複数コーデの要素を取得してコーデごとでループを回す
                coordinations = sectionElement.find_elements(By.XPATH,".//div/div")
                for coordination in coordinations:

                    #なぜかコーデの右下の青い矢印(>)の画像も取られるため偶数回はスキップ
                    f = f + 1
                    if f % 2 == 1: 
                        #コーデ名を取得
                        CoordName =  coordination.text
                        listCoordName.append(CoordName)

                        #画像パスを取得
                        img =  coordination.find_element(By.XPATH,".//a/div/img")
                        imgUrl =  img.get_attribute("src")
                        listImgUrl.append(imgUrl)

                        #コーデ詳細ページへのリンクの取得
                        href = coordination.find_element(By.XPATH,".//a").get_attribute("href")
                        listDetailHref.append(href)
                        
                        print(CoordName)

        #画像の詳細ページへリンク
        for i in range(0,len(listCoordName),1):
            #???を取得しないようにする(詳細のクリックでボタンがなく遷移せずにエラーになる)
            if listCoordName[i] != '? ? ?':
                driver.get(listDetailHref[i])
                    
                #ボタンの取得(存在確認も兼ねてelementsで取得)
                btn =driver.find_elements(By.XPATH,"/html/body/div[2]/div[2]/div[1]/div[2]/div[3]/div/div[5]/div/div/div[2]/div[1]/div/div")
                if len(btn) == 0:
                    #一個だけのコーデを読み取る用(スマイルエレメンツ)
                    btn =driver.find_elements(By.XPATH,"/html/body/div[2]/div[2]/div[1]/div[2]/div[3]/div/div[5]/div/div/div/div/div/div")

                #ボタンの描画範囲内にスクロール
                driver.execute_script("arguments[0].scrollIntoView();", btn[0])
                time.sleep(1)
                #詳細画面を開くためのボタンを押す
                action = ActionChains(driver)
                action.move_to_element(btn[0])
                action.click()
                #キューに入れた操作を実行
                action.perform()
                #詳細画面が出るのを待つ(60秒ダメだったらタイムアウト)
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div[2]/div/div[2]/div/div/dl/dt[1]")))
                
                #レア度とブランドを取得
                detailRare = driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/div[2]/div/div[2]/div/div/dl/dd[1]/span").get_attribute("class")
                detailRare = detailRare[-1]
                detailBrand = driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/div[2]/div/div[2]/div/div/dl/dd[3]/span").get_attribute("class")
                detailBrand = detailBrand[-1]
        
                dict_coord = {}
                dict_coord.setdefault("name",listCoordName[i])
                dict_coord.setdefault("image",listImgUrl[i])
                dict_coord.setdefault("Rare",detailRare)
                dict_coord.setdefault("brand",detailBrand)
                
                dict_data[detailBrand].append(dict_coord)

    #JsonとJSの保存
    fileWrite(dict_data)

    print("fin")



#メイン処理実行
download()

