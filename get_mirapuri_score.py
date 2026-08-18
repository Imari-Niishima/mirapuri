#get_mirapuri_score.py
#自分のミラプリスナップの点数を自動取得するプログラム
#2026/8/15 by Imari
import os
import datetime
import requests
import json
import time
import glob
import sys
from bs4 import BeautifulSoup

if __name__ == "__main__":

    url = "https://mirapri.com/?keyword=%E6%96%B0%E5%B3%B6%E4%BC%8A%E4%B8%87%E9%87%8C"
    id_list = []

    #URLからHTMLを取得している
    base_html = requests.get(url).text

    #BeautifulSoupのオブジェクトを作っている
    base_soup = BeautifulSoup(base_html, "html5lib")
    
    for each_a in base_soup.find_all("a"):
         #全てのリンクを取得。ここから厳選
        cand_id = each_a.get("href")
        #print(cand_id)
        #文字列を持ってるものだけ残す
        if ((type(cand_id) is str) == True) and ((cand_id is not None) == True):
            #"/"は邪魔なので削除
            cand_id = cand_id.replace("/", "")

            #数字か判定
            if cand_id.isdecimal() == True:
                id_list.append(cand_id)

    c = 0
   
    #json形式で出力するためのリスト
    output = []
    
    #jsonファイルだけを抜き出し、日付(作成日時順)にソート
    json_list = glob.glob("scores/*.json")
    #日付の最新順にソート
    json_list.sort()  
    
    #jsonファイルの中身をリスト形式で読み込み
    with open(json_list[-1], mode="r", encoding="utf_8") as f:
        json_items = json.load(f)        

    #各webページに対して処理
    for each_id in id_list:
        page_url = "https://mirapri.com/" + each_id

        html = requests.get(page_url).text
        soup = BeautifulSoup(html, "html5lib")

        #F12キーで要素を取りたいところをクリック、右の青く光ったところを右クリックしてコピー>selectorをコピーしてsoup.selectに張り付ける。nth-childには気をつけろ
        elems_name = soup.select('#photoDetail > article > div.mainText > div.information > div.leftContent > div.title > h2')
        title = str(elems_name[0].contents[0])
        #print(elems_name[0].contents[0])
            
        elems_score = soup.select('#like-button > span.like-count')
        score = str(elems_score[0].contents[0])
        #print(elems_score[0].contents[0])
        
        #過去にいいね数を計測していた場合は差分も求める。なければ0のまま
        diff = 0
        for i in range(len(json_items)):
            if title == json_items[i]["name"]:
                diff = int(score) - int(json_items[i]["scores"])
                break
        
        output.append({"name":title, "scores":score, "diff":diff})

        c += 1
        print(str(c) + "/" + str(len(id_list)) + " finish!")
        
        #1秒停止
        time.sleep(1)

    #今日の日付を出力ファイル名にする
    d_today = datetime.date.today()
    output_json = "scores/score_" + str(d_today) + ".json"

    #jsonファイル出力
    with open(output_json, mode="w", encoding="utf_8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
        
    #webから読み込むファイルを毎回上書きして出力
    with open("scores/scores.json", mode="w", encoding="utf_8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(output_json, " make!")