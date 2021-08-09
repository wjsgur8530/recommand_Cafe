import json
import time

from bs4 import BeautifulSoup as bs
from urllib.request import urlopen

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from selenium import webdriver
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect

# Create your views here.
from CafeApp.dataShared import DataShared
from CafeApp.models import *


def home(request):
    cafe_list = Cafe.objects.all()
    cafe_image = CafeImage.objects.all()
    hit_cafe_list = Cafe.objects.order_by('-hit')[:3]
    page = request.GET.get('page', '1')  # GET 방식으로 정보를 받아오는 데이터
    paginator = Paginator(cafe_image, '16')  # Paginator(분할될 객체, 페이지 당 담길 객체수)
    page_obj = paginator.page(page)  # 페이지 번호를 받아 해당 페이지를 리턴 get_page 권장
    context = {
        'cafe': cafe_list,
        'page_obj': page_obj,
        'hit_cafe': hit_cafe_list,
    }
    return render(request, 'home.html', context)

def cafe_detail(request, pk):
    cafe_detail = Cafe.objects.filter(id=pk)
    cafe_name_1 = Cafe.objects.filter(id=pk+1)
    cafe_name_2 = Cafe.objects.filter(id=pk+2)
    cafe_name_3 = Cafe.objects.filter(id=pk+3)
    cafe_image = CafeImage.objects.filter(id=pk)
    cafe_score = CafeScore.objects.filter(id=pk)
    context = {
        'detail': cafe_detail,
        'image': cafe_image,
        'score': cafe_score,
        'name_1': cafe_name_1,
        'name_2': cafe_name_2,
        'name_3': cafe_name_3,
    }
    return render(request, 'cafe_detail.html', context)
def cafe_map(request):
    return render(request, 'cafe_map.html')

def search_result(request):
    query = None
    if 'search' in request.GET:
        query = request.GET.get('search')
        cafe_list = Cafe.objects.all().filter(Q(name=query) | Q(name__contains=query) | Q(add1=query) | Q(add1__contains=query)).order_by('-pk')
        page = request.GET.get('page', '1')
        paginator = Paginator(cafe_list, '16')
        page_obj = paginator.page(page)
        return render(request, 'search_result.html', {'query': query, 'page_obj': page_obj})
    else:
        return render(request, 'search_result.html', {'query': query})

def crawling(request):
    def crawling(selector, dict):
        if (driver.find_elements_by_css_selector(selector)):
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

    def list_to_string(dict):
        if (cafe_info_dict[dict][0]):
            StrA = "\n".join(cafe_info_dict[dict]).split(",")
            for index in StrA:
                index = index.lstrip()
            cafe_info_dict[dict].remove(cafe_info_dict[dict][0])
            return index
        else:
            cafe_info_dict[dict].remove(cafe_info_dict[dict][0])
            return None

    for i in range(1, 271):
        URL = 'https://www.menupan.com/search/restaurant/restaurant_result.asp?sc=basicdata&kw=%C4%AB%C6%E4&page=' + str(i)

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
            'dd.txt2',  # 영업 시간
            'dd.txt1',  # 휴일
            'ul.tableLR > li > dl:nth-child(1) > dd',  # 좌석
            'ul.tableLR > li > dl:nth-child(2) > dd',  # 주류판매
            'ul.tableLR > li:nth-child(2) > dl:nth-child(1) > dd',  # 금연석 #
            'ul.tableLR > li:nth-child(2) > dl:nth-child(2) > dd',  # 예약정보 #
            'ul.tableLR > li:nth-child(3) > dl:nth-child(1) > dd',  # 화장실 #
            'ul.tableLR > li:nth-child(3) > dl:nth-child(2) > dd',  # 배달/포장 #
            'ul.tableLR > li:nth-child(4) > dl:nth-child(1) > dd',  # 주차
            'ul.tableLR > li:nth-child(4) > dl:nth-child(2) > dd',  # 기타시설
            '#info_ps_f',  # 소개
        ]
        list_keys = [ 'name', 'type', 'tel1', 'add1', 'add2', 'score', 'theme', 'opening', 'off', 'sit', 'alcohol', 'smoke', 'reservation', 'restroom', 'delivery', 'ballet', 'order', 'introduce',]
        count = 0
        for i in range(1, 16):
            time.sleep(1)
            detailPage = driver.find_element_by_css_selector('ul.listStyle3 > li:nth-child(' + str(i) + ') > dl > dt > a')
            time.sleep(1)
            detailPage.click()
            detailPage.get_attribute('href')
            driver.switch_to.window(driver.window_handles[1])
            if (driver.current_url == errorURL):
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            else:
                print(list_keys[0])
                image_crawling()
                for i in range(len(list_keys)):
                    crawling(list_selectors[i], list_keys[i])
                print(cafe_info_dict)
                count = count + 1
                print(count)

                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                name = list_to_string('name')
                tel1 = list_to_string('tel1')
                add1 = list_to_string('add1')
                add2 = list_to_string('add2')
                opening = list_to_string('opening')
                off = list_to_string('off')
                sit = list_to_string('sit')
                alcohol = list_to_string('alcohol')
                smoke = list_to_string('smoke')
                reservation = list_to_string('reservation')
                restroom = list_to_string('restroom')
                delivery = list_to_string('delivery')
                ballet = list_to_string('ballet')
                introduce = list_to_string('introduce')

                cafe = Cafe.objects.create (
                    name=name,
                    tel1=tel1,
                    add1=add1,
                    add2=add2,
                    opening=opening,
                    off=off,
                    sit=sit,
                    alcohol=alcohol,
                    smoke=smoke,
                    reservation=reservation,
                    restroom=restroom,
                    delivery=delivery,
                    ballet=ballet,
                    introduce=introduce,
                )

                #이미지
                if (cafe_info_dict['img'][0]):
                    StrA = "\n".join(cafe_info_dict['img']).split(",")
                    for index in StrA:
                        index = index.lstrip()
                        CafeImage.objects.create(
                            image_url=index,
                            image_id=cafe
                        )
                    cafe_info_dict['img'].remove(cafe_info_dict['img'][0])
                else:
                    cafe_info_dict['img'].remove(cafe_info_dict['img'][0])
                #종류
                if (cafe_info_dict['type'][0]):
                    StrA = "\n".join(cafe_info_dict['type']).split(",")
                    for index in StrA:
                        index = index.lstrip()
                        CafeType.objects.create(
                            type=index,
                            type_id=cafe
                        )
                    cafe_info_dict['type'].remove(cafe_info_dict['type'][0])
                else:
                    cafe_info_dict['type'].remove(cafe_info_dict['type'][0])
                #테마
                if (cafe_info_dict['theme'][0]):
                    StrA = "\n".join(cafe_info_dict['theme']).split(",")
                    for index in StrA:
                        index = index.lstrip()
                        CafeTheme.objects.create(
                            theme=index,
                            theme_id=cafe
                        )
                    cafe_info_dict['theme'].remove(cafe_info_dict['theme'][0])
                else:
                    cafe_info_dict['theme'].remove(cafe_info_dict['theme'][0])

                if (cafe_info_dict['score'][0]):
                    StrA = "\n".join(cafe_info_dict['score']).split(",")
                    for index in StrA:
                        index = index.lstrip()
                        CafeScore.objects.create(
                            score=index,
                            score_id=cafe
                        )
                    cafe_info_dict['score'].remove(cafe_info_dict['score'][0])
                else:
                    cafe_info_dict['score'].remove(cafe_info_dict['score'][0])

                if (cafe_info_dict['order'][0]):
                    StrA = "\n".join(cafe_info_dict['order']).split(",")
                    for index in StrA:
                        index = index.lstrip()
                        CafeOrder.objects.create(
                            order=index,
                            order_id=cafe
                        )
                    cafe_info_dict['order'].remove(cafe_info_dict['order'][0])
                else:
                    cafe_info_dict['order'].remove(cafe_info_dict['order'][0])

def category(request):
    theme_list = []
    previous_lists = []
    new_list = []
    select_theme = request.POST.getlist('theme', None)

    q = Q()
    if select_theme:
        q &= Q(theme__in=select_theme)
    theme = CafeTheme.objects.filter(q)

    ### 중복 제거 ###
    # theme = CafeTheme.objects.get(theme=select_theme)
    theme_distinct = CafeTheme.objects.all().values_list('theme', flat=True).distinct()
    # print(theme_distinct) #중복 제거 오브젝트
    for i in theme_distinct:
        theme_list.append(i)
    # print(theme_list) #중복 제거된 카페 리스트
    ### 중복 제거 ###

    # theme = CafeTheme.objects.filter(theme=select_theme)
    # cafe = Cafe.objects.all(pk=theme.pk)
    for i in theme:
        cafe = Cafe.objects.filter(theme_id=i.pk)
        for j in cafe:
            previous_lists.append(j.name)

    for value in previous_lists:
        if value not in new_list:
            new_list.append(value)
    # print(new_list) #전체 카페

    data = DataShared
    data.setCafeName(new_list)

    context = {
        'cafe_list': new_list,
        'theme_list': theme_list,
    }
    return render(request, 'category.html', context)

def category_result(request):
    select_theme = request.POST.getlist('theme', None)
    select_cafe = request.GET.get('name')
    cafe_pre_list = []
    cafe_next_list = []
    list = []
    pk_pre_list = []
    pk_next_list = []
    q = Q()
    if select_theme:
        q &= Q(theme__in=select_theme)
    theme = CafeTheme.objects.filter(q)

    for i in theme:
        cafe = Cafe.objects.filter(theme_id=i.pk)
        for j in cafe:
            cafe_pre_list.append(j.name)
            pk_pre_list.append(j.pk)

    for value in cafe_pre_list:
        if value not in cafe_next_list:
            cafe_next_list.append(value)
    cafe = Cafe.objects.filter(name=select_cafe)
    print(cafe)

    for value in pk_pre_list:
        if value not in pk_next_list:
            pk_next_list.append(value)
    print(pk_next_list)

    data = DataShared()
    cafe_name = data.getCafeName()
    for i in cafe_name:
        i = i.rstrip()
        list.append(i)

    # print(list) #전체 카페
    context = {
        'cafe': cafe,
        'data': cafe_next_list,
        'pk_next_list': pk_next_list,
    }
    return render(request, 'category_result.html', context)