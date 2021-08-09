import sys
import argparse
import time

import requests
import urllib.request
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from urllib.parse import quote_plus
import json
from io import BytesIO

# API_URL = 'https://dapi.kakao.com/v2/vision/multitag/generate'
# MYAPP_KEY = 'd9e2c49b15d65ae73a121b52505915c9'
#
# def generate_tag(image_url):
#     headers = {'Authorization': 'KakaoAK {}'.format(MYAPP_KEY)}
#
#     try:
#         data = {'image_url': image_url}
#         resp = requests.post(API_URL, headers=headers, data=data)
#         resp.raise_for_status()
#         result = resp.json()['result']
#         if len(result['label_kr']) > 0:
#             if type(result['label_kr'][0]) != str:
#                 result['label_kr'] = map(lambda x: str(x.encode("utf-8")), result['label_kr'])
#             print("이 이미지를 대표하는 태그는 \"{}\"입니다.".format(','.join(result['label_kr'])))
#         else:
#             print("이미지로부터 태그를 생성하지 못했습니다.")
#
#     except Exception as e:
#         print(str(e))
#         sys.exit(0)
#
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description='Classify Tags')
#     parser.add_argument('image_url', type=str, nargs='?',
#         default="https://www.jeongdong.or.kr/static/portal/img/HKPU_04_04_pic1.jpg",#이부분에 링크를 삽입하면된다.
#         help='image url to classify')
#
#     args = parser.parse_args()
#
#     generate_tag(args.image_url)
#
# # 이미지 검색
# url = "https://dapi.kakao.com/v2/search/image"
# headers = {
#     "Authorization": "KakaoAK 78ec36a81d4f183763795e94629433cc"
# }
# data = {
#     "query": "성남 카페 내부"
# }
#
# # 이미지 검색 요청
# response = requests.post(url, headers=headers, data=data)
# # 요청에 실패했다면,
# if response.status_code != 200:
#     print("error! because ", response.json())
# else:  # 성공했다면,
#     count = 0
#     print("검색 결과에 대한 이미지는", data['query'], "입니다.")
#     for image_info in response.json()['documents']:
#         print(f"[{count}th] image_url =", image_info['image_url'])
#         # 저장될 이미지 파일명 설정
#         count = count + 1
#
# # 이미지 크롤링
# i = 1;
# queryUrl = input('검색어 입력: ')
# crawl_num = int(input('크롤링할 갯수 입력(최대 50개): '))
# for i in range(1,4):
#     url = 'http://www.menupan.com/search/restaurant/restaurant_result.asp?sc=basicdata&kw=' + queryUrl + '&page=' + str(i)
#     # url = baseUrl + quote_plus(queryUrl)  # 한글 검색 자동 변환
#     html = urlopen(url)
#     soup = bs(html, "html.parser")
#     img = soup.find_all(class_='thumb')
#     img_text = soup.find_all('dt')
#     cafe_text = soup.find_all('dd')
#
#     cafe_name = []
#     for i in img_text:
#         cafe_name.append(i.text)
#
#     cafe_info = []
#     for i in cafe_text:
#         cafe_info.append(i.text)
#     print(cafe_info)
#
#     word_slice = "\n\n"
#     for i, word in enumerate(cafe_name):
#         if word_slice in word:
#             cafe_name[i] = word.strip(word_slice)
#     print(cafe_name)
#
#     n = 1
#     originalUrl = 'https://www.menupan.com/'
#     for i in img:
#         print(n)
#         imgUrl = i['src']
#         url = originalUrl + imgUrl
#         with urlopen(url) as f:
#             with open('./images/' + cafe_name[n-1] + '.jpg', 'wb') as h:  # w - write b - binary
#                 img = f.read()
#                 h.write(img)
#             with open('./cafe_text/' + cafe_name[n-1] + '.txt', 'w', encoding='utf-8') as t:
#                 t.write(cafe_info[n-1])
#
#         n += 1
#         if n > crawl_num:
#             break
#
#     print('Image Crawling is done.')

import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
def crawling(selector, dict):
    if(driver.find_elements_by_css_selector(selector)):
        cafe_info_dict[dict].append(driver.find_element_by_css_selector(selector).text)
    else:
        cafe_info_dict[dict].append(None)

def image_crawling():
    if (driver.find_elements_by_css_selector('#restphoto_img_6')):
        elements = driver.find_elements_by_css_selector('#restphoto_img_6')
        for i in elements:
            image = i.get_attribute('src')
        cafe_info_dict['img'].append(image)
    else:
        cafe_info_dict['img'].append(None)

for i in range(1, 16):
    URL = 'https://www.menupan.com/search/restaurant/restaurant_result.asp?sc=basicdata&kw=cafe&page=' + str(i)

    errorURL = 'https://www.menupan.com/errpage/err_onepage.asp'

    driver = webdriver.Chrome(executable_path='chromedriver')
    driver.get(url=URL)

    cafe_info_dict = {
        'img': [],
        'name': [],
        'type': [],
        'tel1': [],
        'add1': [],
        'add2': [],
        'score': [],
        'theme': [],
        'opening': [],
        'off': [],
        'sit': [],
        'alcohol': [],
        'smoke': [],
        'reservation': [],
        'restroom': [],
        'delivery': [],
        'ballet': [],
        'order': [],
        'introduce': [],
    }
    list_selectors = [
        'dd.name',
        'dd.type',
        'dd.tel1',
        'dd.add1',
        'dd.add2',
        'span.total',
        'dd.Theme',
        'dd.txt2', #영업 시간
        'dd.txt1', #휴일
        'ul.tableLR > li > dl:nth-child(1) > dd', #좌석
        'ul.tableLR > li > dl:nth-child(2) > dd', #주류판매
        'ul.tableLR > li:nth-child(2) > dl:nth-child(1) > dd', #금연석 #
        'ul.tableLR > li:nth-child(2) > dl:nth-child(2) > dd', #예약정보 #
        'ul.tableLR > li:nth-child(3) > dl:nth-child(1) > dd', #화장실 #
        'ul.tableLR > li:nth-child(3) > dl:nth-child(2) > dd', #배달/포장 #
        'ul.tableLR > li:nth-child(4) > dl:nth-child(1) > dd', #주차
        'ul.tableLR > li:nth-child(4) > dl:nth-child(2) > dd', #기타시설
        '#info_ps_f', #소개
    ]
    list_keys = [
        'name',
        'type',
        'tel1',
        'add1',
        'add2',
        'score',
        'theme',
        'opening',
        'off',
        'sit',
        'alcohol',
        'smoke',
        'reservation',
        'restroom',
        'delivery',
        'ballet',
        'order',
        'introduce',
    ]
    count = 0
    for i in range(1, 16):
        time.sleep(1)
        detailPage = driver.find_element_by_css_selector('ul.listStyle3 > li:nth-child(' + str(i) + ') > dl > dt > a')
        time.sleep(1)
        detailPage.click()
        #detailPage.get_attribute('href')
        driver.switch_to.window(driver.window_handles[1])
        if(driver.current_url == errorURL):
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        else:
            #print(list_keys[0])
            image_crawling()
            for i in range(len(list_keys)):
                crawling(list_selectors[i], list_keys[i])
            print(cafe_info_dict)
            count = count + 1
            print(count)

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

    # for i in cafe_info_dict:
    #     for j in range(count):
    #         if(j % count == 0):
    #             print("\n")
    #         print(cafe_info_dict[i][j])
    for i in list_keys:
        print(cafe_info_dict[i])