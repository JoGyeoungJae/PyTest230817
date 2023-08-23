import time
import bs4
import urllib.request
import ssl
import pymysql
import requests
from tkinter import *
from tkinter import messagebox
import re
# 주의사항, 문자열 안에 특수문자 부분 체크 잘하기.
# 현재 네이트 기사는 특정 시간 예 1분마다 새로운 기사가 나옴.
# 그래서, 현재 페이지에 1페이지에서 20개 기사만 디비에 저장하기로 함.
# 특정 시간 time.sleep(300), 5분정도 인터벌을 두고 저장하기로 함.
# 예스24는 한페이지의 상품이 고정,
# 뉴스는 실시간으로 계속 생성됨.
ssl_context = ssl.SSLContext()
ssl_context.verify_mode = ssl.CERT_NONE
imgUrl, title, cityname, citysubname, startday, endday, contentlink = "", "", "", "", "", "", ""
null = None


def clean_text(inputString):
    text_rmv = re.sub(
        '[-=+,#/\?:^.@*\"※~ㆍ!』‘\(\)\[\]`\'…》\”\“\’·]', ' ', inputString)
    return text_rmv


def insertData(title, cityname, citysubname, startday, endday, contentlink, imgUrl):
    con, cur = None, None
    data = ""
    data0, data1, data2, data3, data4, data5, data6, data7 = "", "", "", "", "", "", "", ""
    sql = ""
    con = pymysql.connect(host='127.0.0.1', user='root',
                          password='1234', database='festival', charset='utf8')
    cur = con.cursor()
    data1 = title
    data2 = cityname
    data3 = citysubname
    data4 = startday
    data5 = endday
    data6 = contentlink
    data7 = imgUrl

    # data1 = clean_text(subject)
    # data2 = clean_text(press)
    # data3 = clean_text(pDate)
    # data4 = clean_text(pTime)
    # data5 = clean_text(link)
    # data6 = clean_text(imgLinkUrl)
    #
    try:
        # print(null)
        # print("데이터 실행전 확인")
        # print(data1)
        # print(data2)
        # print(data3)
        # print(data4)
        # print(data5)
        # print(data6)
        sql = "INSERT INTO festivaltable (title,cityname,citysubname,startday,endday,contentlink,imgUrl)  VALUES('" + \
            data1 + "','" + data2 + "','" + data3 + "','" + \
            data4 + "','" + data5 + "','"+data6 + "','" + data7 + "')"
        print("순서2 : sql 실행전 ")
        print(f"sql : {sql}")

        cur.execute(sql)

        # cur.execute(query, values)
    except:
        print('================================')
        print("순서3 : 예외 발생")
        print('================================')
        # messagebox.showerror('오류', '데이터 입력 오류가 발생함')
    else:
        print('================================')
        print("순서3: 성공")
        print('================================')
        # messagebox.showinfo('성공', '데이터 입력 성공')
    con.commit()
    con.close()


##
count = 0
while True:
    festivalURL = "https://korean.visitkorea.or.kr/kfes/list/wntyFstvlList.do"

    if (count <= 20):
        try:
            count += 1
            fesUrl = festivalURL
            response = requests.get(fesUrl, verify=False)
            response.raise_for_status()
            bsObject = bs4.BeautifulSoup(response.content, 'html.parser')

            ul_tag = bsObject.find('ul', {'class': 'other_festival_ul'})
            print(f"ul_tag = {ul_tag}")
            tag_list = ul_tag.findAll('li')  # ul 태그 내부의 모든 li 태그 추출
            print(f"tag_list = {tag_list}")
            # title, cityname, citysubname, startday, endday,contentlink, imgUrl
            for tag in tag_list:
                title = tag.find(
                    'strong').text
                title = clean_text(title)
                contentlink = tag.find('a')['href']
                contentlink = 'https:' + contentlink
                imgLink = tag.find('div', {'class': 'other_festival_img'})
                # 이미지 없는 경우 처리 부분. 파이썬 null 대신  None
                if imgLink != None:
                    imgLinkUrl = imgLink.find('img')['src']
                    imgLinkUrl = 'https:' + imgLinkUrl
                else:
                    imgLinkUrl = '이미지가 존재 하지 않음'

                fullcity = tag.find('div', {'class': 'date'}).text
                fullcity.replace('\t', ' ')
                fullcity.replace('\n', ' ')
                print(f"fullcity = {fullcity}")
                if len(fullcity.split()) == 2:
                    cityname, citysubname = fullcity.split()
                else:
                    cityname = 'pTime없음'
                    citysubname = 'pDate없음'

                fullDate = tag.find('div', {'class': 'date'}).text
                fullDate.replace('~', ' ')
                print(f"fullDate = {fullDate}")
                if len(fullDate.split()) == 2:
                    startday, endday = fullDate.split()
                else:
                    startday = 'pTime없음'
                    endday = 'pDate없음'

                    # continue
                print("순서1: 데이터 추가 전")
                print("subject: %s" % (title))
                insertData(title, cityname, citysubname, startday,
                           endday, contentlink, imgLinkUrl)
                # print('(' , page, ')', subject)
                # print('\t https:'+link, press, pDate, pTime)
                # print('\t imgLink : '+ imgLinkUrl)

        except:
            break
    else:
        break
    # time.sleep(10)
