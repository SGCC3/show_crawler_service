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
url = ["http://ticket.interpark.com/TPGoodsList.asp?Ca=Mus",
       "http://ticket.interpark.com/TPGoodsList.asp?Ca=Liv",
       "http://ticket.interpark.com/TPGoodsList.asp?Ca=Dra&Sort=3",
       "http://ticket.interpark.com/TPGoodsList.asp?Ca=Cla",
       "http://ticket.interpark.com/TPGoodsList.asp?Ca=Eve&SubCa=Eve_T"
       ]
for i in range(0, 5):
    driver.get(url[i])
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    driver.implicitly_wait(20)
    content_pic = []
    Content_pic = driver.find_elements_by_xpath('/html/body/table/tbody/tr[2]/td[3]/div/div/div[2]/div/table/tbody/tr/td[1]/a/img')
    for cp in Content_pic:
        conp = cp.get_attribute('src')
        content_pic.append(conp)
    Content_name = driver.find_elements_by_xpath('/html/body/table/tbody/tr[2]/td[3]/div/div/div[2]/div/table/tbody/tr/td[2]/span/a')
    content_name = []
    for cn in Content_name:
        content_name.append(cn.text)
    Content_location = driver.find_elements_by_xpath('/html/body/table/tbody/tr[2]/td[3]/div/div/div[2]/div/table/tbody/tr/td[3]/a')
    content_location = []
    for cl in Content_location:
        content_location.append(cl.text)
    Content_date = driver.find_elements_by_xpath('/html/body/table/tbody/tr[2]/td[3]/div/div/div[2]/div/table/tbody/tr/td[4]')
    content_date = []
    for cd in Content_date:
        content_date.append(cd.text.replace('\n', '').replace("\t", ''))
    content_link = []
    Content_link = driver.find_elements_by_xpath('/html/body/table/tbody/tr[2]/td[3]/div/div/div[2]/div/table/tbody/tr/td[1]/a')
    for ctl in Content_link:
        conlink = ctl.get_attribute('href')
        content_link.append(conlink)
    ff = pd.DataFrame({'공연이름': content_name, '공연포스터': content_pic, '날짜': content_date,
                       '장소': content_location, '공연링크': content_link
                       })
    name = ff['공연이름'].to_list()
    ff.to_csv(genre[i] + '.csv')

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
        Play_name = driver.find_elements_by_xpath('//*[@id="container"]/div[5]/div[1]/div[2]/div[1]/div/div[1]/h2')
        play_name = []
        for pn in Play_name:
            play_name.append(pn.text)
        play_poster = []
        Play_poster = driver.find_elements_by_xpath('//*[@id="container"]/div[5]/div[1]/div[2]/div[1]/div/div[2]/div/div[1]/img')
        for pp in Play_poster:
            plap = "https:" + pp.get_attribute('src')
            play_poster.append(plap)
        play_info_1 = []
        play_info_2 = []
        Play_info_1 = driver.find_elements_by_xpath('//*[@id="container"]/div[5]/div[1]/div[2]/div[1]/div/div[2]/ul/li/strong')
        Play_info_2 = driver.find_elements_by_xpath('//*[@id="container"]/div[5]/div[1]/div[2]/div[1]/div/div[2]/ul/li/div/p')
        Play_info_lo = driver.find_elements_by_xpath('//*[@id="container"]/div[5]/div[1]/div[2]/div[1]/div/div[2]/ul/li[1]/div/a')
        for pll in Play_info_lo:
            play_info_2.append(pll.text.replace('(자세히)', ''))
        for pi1 in Play_info_1:
            play_info_1.append(pi1.text)
        play_info_1 = play_info_1[0:5]
        for pi2 in Play_info_2:
            play_info_2.append(pi2.text)
        play_info_2 = play_info_2[0:4]
        Play_seat = driver.find_elements_by_xpath('//*[@id="container"]/div[5]/div[1]/div[2]/div[1]/div/div[2]/ul/li[5]/div/ul/li[2]/div/div/ul/li')
        Play_price = driver.find_elements_by_xpath('//*[@id="container"]/div[5]/div[1]/div[2]/div[1]/div/div[2]/ul/li[5]/div/ul/li[2]/div/div/ul/li/strong')
        play_price = []
        play_seat = []
        for ss in Play_seat:
            sss = ss.text.replace('원', '').rsplit(' ', 1)
            play_seat.append(sss[0])
        for sp in Play_price:
            spp = sp.text + "원"
            play_price.append(spp)
        price = {x: y for x, y in zip(play_seat, play_price)}
        print(play_name, price)

        talents = []
        talents_pic = []
        talents_act = []
        Talents = soup.select('#productMainBody > div > div.content.casting > div > ul > li > div.castingInfo > div.castingName')
        Talents_pic = driver.find_elements_by_xpath('//*[@id="productMainBody"]/div/div[1]/div/ul/li/div[1]/a[1]/div/img')
        Talents_act = soup.select('#productMainBody > div > div.content.casting > div > ul > li > div.castingInfo > div.castingActor')
        for pic in Talents_pic:  # 출연진 사진
            img_url = pic.get_attribute('src')
            talents_pic.append(img_url)
        for t in Talents:
            talents.append(t.get_text())
        for ac in Talents_act:
            talents_act.append(ac.get_text())
        actors = []
        if i == 0 or i == 2:
            for ac in zip(talents, talents_act, talents_pic):
                actors.append(ac)
        if i == 1 or i == 3:
            for ac in zip(talents, talents_pic):
                actors.append(ac)
        time_play = []
        Time_play = driver.find_elements_by_xpath('//*[@id="productMainBody"]/div/div[2]/div')
        for tp in Time_play:
            time_play.append(tp.text.replace('\n', ' '))
        play_pic = []
        Play_pic = driver.find_elements_by_xpath('//*[@id="productMainBody"]/div/div[3]/div/p/strong/img')
        for play in Play_pic:
            imgs_url = play.get_attribute('src')
            play_pic.append(imgs_url)

driver.quit()
