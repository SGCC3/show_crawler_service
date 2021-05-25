import requests
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from multiprocessing import Pool


driver = webdriver.Chrome('D:/chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
options.add_argument("lang=ko_KR")
# driver = webdriver.Chrome('chromedriver', chrome_options=options)
genre = ["Interpark_MUSICAL", "Interpark_CONCERT", "Interpark_PLAY", "Interpark_CLASSIC+DANCE", "Interpark_EVENT+EXHIBITION"]
url = ["http://ticket.interpark.com/TPGoodsList.asp?Ca=Mus", "http://ticket.interpark.com/TPGoodsList.asp?Ca=Liv", "http://ticket.interpark.com/TPGoodsList.asp?Ca=Dra&Sort=3", "http://ticket.interpark.com/TPGoodsList.asp?Ca=Cla", "http://ticket.interpark.com/TPGoodsList.asp?Ca=Eve&SubCa=Eve_T"]
for i in range(0, 5):
    driver.get(url[i])
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    driver.implicitly_wait(20)
    prev_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        driver.implicitly_wait(20)
        curr_height = driver.execute_script("return document.body.scrollHeight")
        if curr_height == prev_height:
            break
        else:
            prev_height = driver.execute_script("return document.body.scrollHeight")
    driver.implicitly_wait(20)
    content_pic = []
    Content_pic = soup.select('body > table > tbody > tr:nth-child(2) > td:nth-child(3) > div > div > div.con > div > table > tbody > tr > td.RKthumb > a > img')
    for cp in Content_pic:
        conp = cp['src']
        content_pic.append(conp)
    Content_name = soup.select('body > table > tbody > tr:nth-child(2) > td:nth-child(3) > div > div > div.con > div > table > tbody > tr > td.RKtxt > span > a')
    content_name = []
    for cn in Content_name:
        content_name.append(cn.get_text())
    Content_location = soup.select('body > table > tbody > tr:nth-child(2) > td:nth-child(3) > div > div > div.con > div > table > tbody > tr > td:nth-child(3) > a')
    content_location = []
    for cl in Content_location:
        content_location.append(cl.get_text())
    Content_date = soup.select('body > table > tbody > tr:nth-child(2) > td:nth-child(3) > div > div > div.con > div > table > tbody > tr > td:nth-child(4)')
    content_date = []
    for cd in Content_date:
        content_date.append(cd.get_text().replace('\n', '').replace("\t", ''))
    content_link = []
    Content_link = soup.select('body > table > tbody > tr:nth-child(2) > td:nth-child(3) > div > div > div.con > div > table > tbody > tr > td.RKtxt > span > a')
    for ctl in Content_link:
        conlink = "http://ticket.interpark.com/" + ctl['href']
        content_link.append(conlink)
    ff = pd.DataFrame({'공연이름': content_name, '공연포스터': content_pic, '날짜': content_date, '장소': content_location, '공연링크': content_link})
    name = ff['공연이름'].to_list()
    ff.to_csv(genre[i] + '.csv')
    print(content_name,len(content_name))

    for w in range(len(content_link)):
        driver.get(content_link[w])
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        driver.implicitly_wait(20)
        prev_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            driver.implicitly_wait(20)
            curr_height = driver.execute_script("return document.body.scrollHeight")
            if curr_height == prev_height:
                break
            else:
                prev_height = driver.execute_script("return document.body.scrollHeight")
        driver.implicitly_wait(20)
        Play_name = soup.select('#container > div.contents > div.productWrapper > div.productMain > div.productMainTop > div > div.summaryTop > h2')
        play_name = []
        for pn in Play_name:
            play_name.append(pn.get_text())
        play_poster = []
        Play_poster = soup.select('#container > div.contents > div.productWrapper > div.productMain > div.productMainTop > div > div.summaryBody > div > div.posterBoxTop > img')
        for pp in Play_poster:
            plap = "https:" + pp['src']
            play_poster.append(plap)
        play_info_1 = []
        play_info_2 = []
        Play_info_1 = soup.select('#container > div.contents > div.productWrapper > div.productMain > div.productMainTop > div > div.summaryBody > ul > li > strong')
        Play_info_2 = soup.select('#container > div.contents > div.productWrapper > div.productMain > div.productMainTop > div > div.summaryBody > ul > li > div > p')
        Play_info_lo = soup.select('#container > div.contents > div.productWrapper > div.productMain > div.productMainTop > div > div.summaryBody > ul > li:nth-child(1) > div > a')
        for pll in Play_info_lo:
            play_info_2.append(pll.get_text().replace('(자세히)', ''))
        for pi1 in Play_info_1:
            play_info_1.append(pi1.get_text())
        play_info_1 = play_info_1[0:5]
        for pi2 in Play_info_2:
            play_info_2.append(pi2.get_text())
        play_info_2 = play_info_2[0:4]
        time.sleep(2)
        Play_seat = soup.select('#container > div.contents > div.productWrapper > div.productMain > div.productMainTop > div > div.summaryBody > ul > li.infoItem.infoPrice > div > ul > li > span.name')
        Play_price = soup.select('#container > div.contents > div.productWrapper > div.productMain > div.productMainTop > div > div.summaryBody > ul > li.infoItem.infoPrice > div > ul > li > span.price')
        play_price = []
        play_seat = []
        for ps in Play_seat:
            play_seat.append(ps.get_text())
        for pp in Play_price:
            play_price.append(pp.get_text())

        price = {x: y for x, y in zip(play_seat, play_price)}
        Some_seat = soup.select('#container > div.contents > div.productWrapper > div.productMain > div.productMainTop > div > div.summaryBody > ul > li.infoItem.infoPrice > div > ul > li:nth-child(2) > div > div')
        some_seat = []
        Some_price = soup.select('#container > div.contents > div.productWrapper > div.productMain > div.productMainTop > div > div.summaryBody > ul > li.infoItem.infoPrice > div > ul > li:nth-child(2) > div > div > strong')
        some_price = []
        for ss in Some_seat:
            for strong in ss.find_all('strong'):
                strong.extract()
            sss = ss.get_text().replace('원', '')
            some_seat.append(sss)
        for sp in Some_price:
            spp = sp.get_text() + "원"
            some_price.append(spp)
        some = {x: y for x, y in zip(some_seat, some_price)}
        price_info = {**price, **some}
        play_info = play_info_2.append(price_info)

        talents = []
        talents_pic = []
        talents_act = []
        Talents = soup.select('#productMainBody > div > div.content.casting > div > ul > li > div.castingInfo > div.castingName')
        Talents_pic = soup.select('#productMainBody > div > div.content.casting > div > ul > li > div.castingTop > a.castingLink > div > img')
        Talents_act = soup.select('#productMainBody > div > div.content.casting > div > ul > li:nth-child(2) > div.castingInfo > div.castingActor')
        for pic in Talents_pic:  # 출연진 사진
            img_url = pic['src']
            talents_pic.append(img_url)
        for t in Talents:
            talents.append(t.get_text())
        for ac in Talents_act:
            talents_act.append(ac.get_text())
        actors = []
        for ac in zip(talents, talents_act, talents_pic):
            actors.append(ac)
        time_play = []
        Time_play = soup.select('#productMainBody > div > div:nth-child(2) > div')
        for tp in Time_play:
            time_play.append(tp.get_text())
        print(time_play)
        play_pic = []
        Play_pic = soup.select('#productMainBody > div > div:nth-child(2) > div')
        for play in Play_pic:
            imgs_url = play['src']
            play_pic.append(imgs_url)
        print(play_pic)

driver.quit()