import requests
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from multiprocessing import Pool
import datetime
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome('D:/chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
options.add_argument("lang=ko_KR")
driver = webdriver.Chrome('chromedriver', chrome_options = options)

genre = ["Yes24_CONCERT", "Yes24_MUSICAL", "Yes24_PLAY", "Yes24_CLASSIC+DANCE", "Yes24_EVENT+EXHIBITION"]
url = ['http://ticket.yes24.com/New/Genre/GenreList.aspx?genretype=1&genre=15456',
       "http://ticket.yes24.com/New/Genre/GenreList.aspx?genretype=1&genre=15457",
       "http://ticket.yes24.com/New/Genre/GenreList.aspx?genretype=1&genre=15458",
       "http://ticket.yes24.com/New/Genre/GenreList.aspx?genretype=1&genre=15459",
       "http://ticket.yes24.com/New/Genre/GenreList.aspx?genretype=1&genre=15460"
       ]
for i in range(0, 4):
    driver.get(url[i])
    body = driver.find_element_by_css_selector('body')
    for w in range(50):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    content_pic = []
    Content_pic = driver.find_elements_by_xpath('/html/body/section/div/a/div/img')
    for cp in Content_pic:
        conp = cp.get_attribute('src')
        content_pic.append(conp)
    Content_name = driver.find_elements_by_xpath('/html/body/ section/div/a/div/div/p[1]')
    content_name = []
    for cn in Content_name:
        content_name.append(cn.text)
    Content_location = driver.find_elements_by_xpath('/html/body/section/div/a/div/div/p[3]')
    content_location = []
    for cl in Content_location:
        content_location.append(cl.text)
    Content_date = driver.find_elements_by_xpath('/html/body/section/div/a/div/div/p[2]')
    content_date = []
    for cd in Content_date:
        content_date.append(cd.text)
    content_link = []
    Content_link = driver.find_elements_by_xpath('/html/body/section/div/a')
    for ctl in Content_link:
        conlink = ctl.get_attribute("onclick")
        conLink = conlink.replace('jsf_base_GoToPerfDetail(', '').replace(");", "")
        con_link = "http://ticket.yes24.com/Perf/" + conLink
        content_link.append(con_link)
    print(content_name, content_pic, content_date, content_location, content_link)
    print(len(content_name))

    yy = pd.DataFrame({'공연이름': content_name, '공연포스터': content_pic, '날짜': content_date,
                       '장소': content_location, '공연링크': content_link
                       })
    name = yy['공연이름'].to_list()
    yy.to_csv(genre[i] + '.csv')

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
        play_name = content_name[w]
        play_date = content_date[w]
        play_location = content_date[w]
        play_poster = []
        Play_poster = driver.find_elements_by_xpath('//*[@id="mainForm"]/div[10]/div/div[1]/div[1]/div[1]/img')
        for pp in Play_poster:
            plap = pp.get_attribute('src')
            play_poster.append(plap)
        play_info_1 = []
        play_info_2 = []
        play_info_act = []
        Play_info_1 = driver.find_elements_by_xpath('//*[@id="mainForm"]/div[10]/div/div[1]/div[2]/div/dl/dt')
        Play_info_2 = driver.find_elements_by_xpath('//*[@id="mainForm"]/div[10]/div/div[1]/div[2]/div/dl/dd')
        Play_info_act = driver.find_elements_by_xpath('//*[@id="mainForm"]/div[10]/div/div[1]/div[2]/div[1]/dl/dd[3]/a[1]')
        for pli in Play_info_1:
            play_info_1.append(pli.text)
        for pli in Play_info_2:
            play_info_2.append(pli.text.replace('\n', ''))
        play_info = play_info_1[0:6]
        del play_info[4]
        play_inf = play_info_2[0:6]
        del play_inf[2:5]
        for pla in Play_info_act:
            play_info_act.append(pla.text)
        play_inf.insert(2, play_info_act)

        Some_seat = driver.find_elements_by_xpath('//*[@id="mCSB_3_container"]/li')
        some_seat = []
        Some_price = driver.find_elements_by_xpath('//*[@id="mCSB_3_container"]/li/span')
        some_price = []
        for ss in Some_seat:
            sss = ss.text.replace('원', '').rsplit(' ', 1)
            some_seat.append(sss[0])
        for sp in Some_price:
            spp = sp.text + "원"
            some_price.append(spp)
        price = {x: y for x, y in zip(some_seat, some_price)}
        play_inf.insert(3, price)
        play_info_final = {x: y for x, y in zip(play_info, play_inf)}
        print(play_info_final)

        play_pic = []
        Play_pic_1 = driver.find_elements_by_xpath('//*[@id="divPerfNotice"]/p/img')
        Play_pic_2 = driver.find_elements_by_xpath('//*[@id="divPerfContent"]/p/img')
        for play in Play_pic_1:
            imgs_url = play.get_attribute('src')
            play_pic.append(imgs_url)
        for play in Play_pic_2:
            imgs = play.get_attribute('src')
            play_pic.append(imgs)
        print(play_pic)
driver.quit()
