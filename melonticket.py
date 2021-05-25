import requests
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from multiprocessing import Pool

driver = webdriver.Chrome('D:\chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
options.add_argument("lang=ko_KR")  # 한국어!
driver = webdriver.Chrome('chromedriver', chrome_options=options)

url = "https://ticket.melon.com/main/index.htm"  # 멜론티켓 url
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
driver.implicitly_wait(3)
prev_height = driver.execute_script("return document.body.scrollHeight")  # 대충 화면 젤 아랫쪽까지 스크롤하는 거
while True:
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(0.3)
    curr_height = driver.execute_script("return document.body.scrollHeight")
    if curr_height == prev_height:
        break
    else:
        prev_height = driver.execute_script("return document.body.scrollHeight")

site_url = soup.select('#gnb_menu > ul > li > a')  # 각 장르별 주소 소환
sites = []
genre = ["Melon_CONCERT", "Melon_MUSICAL+PLAY", "Melon_CLASSIC+DANCE", "Melon_EXHIBITION+EVENT"]  # csv 저장할때 썼는 건데 별 상관없을지두?
for ur in site_url:
    site = ur['href']
    sites.append(site)
sites_each = sites[1:5]  # 쓸데없는 사이트 슬라이싱
for i in range(0, 4):  # 아까 장르 링크 따낸 거 하나씩 반복
    driver.get(sites_each[i])
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    driver.implicitly_wait(3)
    prev_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(0.3)
        curr_height = driver.execute_script("return document.body.scrollHeight")
        if curr_height == prev_height:
            break
        else:
            prev_height = driver.execute_script("return document.body.scrollHeight")
    ticket_poster = []
    ticket_Poster = soup.select('#perf_poster > li > a > span.thumb > img')
    for p in ticket_Poster:
        imgUrl = p['src']  # 포스터 이미지 소스 따오기
        ticket_poster.append(imgUrl)
    ticket_name = []  # 근데 콘서트는 출력이 20개까지밖에 안 되더라구여? html 보니까 javascript 처음 불려올 때 listCnt 가 20개까지로
    # 제한되어 있어서 그런 거 같은데, html 은 어떻게든 끌고 오겠는데, javascript 는 어떻게 건드려야 할지 잘 모르겠어요
    # 스크롤 끝까지 내리는 함수 써도 그러네요 왜 그렇져? 멜론 말고 인터파크는 잘되던데
    ticket_Name = soup.select("#perf_poster > li > a > strong")
    for n in ticket_Name:  # 이름 불러오기
        ticket_name.append(n.get_text())
    ticket_date = []
    ticket_Date = soup.select('#perf_list > tr > td > ul > li')
    for d in ticket_Date:  # 콘서트 일정 불러오기
        ticket_date.append(d.get_text())
    ticket_location = []
    ticket_Location = soup.select('#perf_poster > li > a > span.location')
    for lo in ticket_Location:  # 콘서트 장소 불러오기
        ticket_location.append(lo.get_text())
    ticket_info = []
    ticket_Info = soup.select('#perf_poster > li > a')
    for info in ticket_Info:
        infoUrl = info['href']  # 상세 정보 있는 주소 따오기 안으로 드가면 그냥 정보 나옴
        infoUrl = "https://ticket.melon.com/" + infoUrl
        ticket_info.append(infoUrl)
    for item in zip(ticket_poster, ticket_name, ticket_date, ticket_location, ticket_info):
        # zip 함수 넣으면 한 세트로 묶어서 나오는 거 같긴 한데 이렇게 묶어서 어케 저장하는지는 잘 모르겠어여
        print(item)
    final = pd.DataFrame({'공연이름': ticket_name, '공연일자': ticket_date, '공연위치': ticket_location, '공연포스터': ticket_poster, '공연링크': ticket_info})
    name = final['공연이름'].to_list()  # 데이터 파일 csv 로 저장하는 건데 어차피 데이터베이스 있으니까 그쪽에다 나중에 저장하는 걸로 코드 바꿔야 하지 않을까요? 임시저장
    final.to_csv(genre[i] + '.csv')

    for w in range(len(ticket_info)):  # 아까 각 공연 링크 따온 거 있죠 그 링크 상세주소로 들어가서 크롤링하는 코드에요
        driver.get(ticket_info[w])
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        driver.implicitly_wait(3)
        prev_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(0.3)
            curr_height = driver.execute_script("return document.body.scrollHeight")
            if curr_height == prev_height:
                break
            else:
                prev_height = driver.execute_script("return document.body.scrollHeight")
        content_name = []  # 콘서트 이름
        content_Name = soup.select('#conts > div > div.wrap_consert_product > div.wrap_consert_cont > div.box_consert_txt > p.tit')
        for c in content_Name:
            content_name.append(c.get_text())
            print(content_name)
        content_info_11 = []  # 콘서트 정보 4개로 나누어서 가져왔는데, 그 html에 섹션이 왼쪽 섹션 오른쪽 섹션, 그리고 그 섹션 내에서 dt 클래서 dd 클래스로 나뉘어가지고
        content_info_12 = []  # 그냥 글씨 다 가져오고, 데이터 보니까 사전 형식으로 크롤링하면 좋겠다 싶어서 그렇게 하긴 했는데 바꿔도 되긴 할 거 같아요
        content_info_21_1 = []
        content_info_22 = []
        content_Info_11 = soup.select('#conts > div > div.wrap_consert_product > div.wrap_consert_cont > div.box_consert_txt > div.box_consert_info > dl.info_left > dt')
        content_Info_12 = soup.select('#conts > div > div.wrap_consert_product > div.wrap_consert_cont > div.box_consert_txt > div.box_consert_info > dl.info_left > dd')
        content_Info_21 = soup.select('#conts > div > div.wrap_consert_product > div.wrap_consert_cont > div.box_consert_txt > div.box_consert_info > dl.info_right > dt')
        content_Info_221 = soup.select('#performanceHallBtn > span.place')
        content_Info_222 = soup.select('#conts > div > div.wrap_consert_product > div.wrap_consert_cont > div.box_consert_txt > div.box_consert_info > dl.info_right > dd:nth-child(4)')
        for z in content_Info_11:
            content_info_11.append(z.get_text())
        for b in content_Info_12:
            content_info_12.append(b.get_text())
        for c in content_Info_21:
            content_info_21_1.append(c.get_text())
        content_info_21 = content_info_21_1[0:len(content_info_21_1)-1]
        for d in content_Info_221:
            content_info_22.append(d.get_text().replace(u'\xa0', u''))
            # xa0 인가 뭔가 나눠질수 없는 공백 어쩌구 그랬던 거 같아서 없애려고 replace 함수 썼어요
        for e in content_Info_222:
            content_info_22.append(e.get_text())
        dict_info_1 = {x: y for x, y in zip(content_info_11, content_info_12)}  # 왼쪽정보 크롤링
        dict_info_2 = {x: y for x, y in zip(content_info_21, content_info_22)}  # 오른쪽 정보 크롤링
        content_info = {**dict_info_1, **dict_info_2}  # 사전합치기
        print(content_info)

        talents = []
        talents_pic = []
        talents_act = []
        Talents = soup.select('#conts > div > div:nth-child(3) > div.wrap_detail_left_cont > div.box_artist_checking > div > ul > li > a > strong')
        Talents_pic = soup.select('#conts > div > div:nth-child(3) > div.wrap_detail_left_cont > div.box_artist_checking > div > ul > li > label > span > span > span.crop > img')
        Talents_act = soup.select('#conts > div > div:nth-child(3) > div.wrap_detail_left_cont > div.box_artist_checking > div.scroll > ul > li > a > span')
        for pic in Talents_pic:  #출연진 사진
            img_url = pic['src']
            talents_pic.append(img_url)
        for t in Talents:
            talents.append(t.get_text())
        for ac in Talents_act:
            talents_act.append(ac.get_text())
        actors = []
        for ac in zip(talents, talents_act, talents_pic):
            actors.append(ac)
        seat_location = []
        seat_price = []
        Seat_location = soup.select('#conts > div > div:nth-child(3) > div.wrap_detail_left_cont > div.box_bace_price > ul > li > span.seat_name')
        Seat_price = soup.select('#conts > div > div:nth-child(3) > div.wrap_detail_left_cont > div.box_bace_price > ul > li > span.price')
        for sl in Seat_location:
            seat_location.append(sl.get_text())
        for sp in Seat_price:
            seat_price.append(sp.get_text())
        seat = {x: y for x, y in zip(seat_location, seat_price)}
        print(seat)
        time_play = []
        Time_play = soup.select('#conts > div > div:nth-child(3) > div.wrap_detail_left_cont > div.box_concert_time > p:nth-child(2) > span')
        for tp in Time_play:
            time_play.append(tp.get_text().replace(u'xa0', u''))
        print(time_play)
        play_pic = []
        Play_pic2 = soup.select('#conts > div > div:nth-child(3) > div.wrap_detail_left_cont > div.box_img_content > p > img')
        Play_pic = soup.select('#conts > div > div:nth-child(3) > div.wrap_detail_left_cont > div.box_ticke_notice > p > span > img')
        for play in Play_pic:
            imgs_url = play['src']
            play_pic.append(imgs_url)
        for play in Play_pic2:
            imgs_url = play['src']
            play_pic.append(imgs_url)
        print(play_pic)