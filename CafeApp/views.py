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
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from CafeApp.dataShared import DataShared
from CafeApp.models import *
from Comment.models import Comment


def home(request):
    hit_cafe = []
    hit_pk_list = []
    total_score_pk_list = []
    total_score_list = []
    hit_cafe_name_list = []
    comment_list = []
    image_pk_list = []
    image_list = []
    cafe_list = Cafe.objects.all()

    cafe_score = CafeScore.objects.all().order_by('-score')[:3]
    cafe_score_total = CafeScore.objects.all()
    for i in cafe_list:
        image_pk_list.append(i.pk)
    print(image_pk_list)

    for i in image_pk_list:
        image = CafeImage.objects.get(image_id=i)
        image_list.append(image)
    print(image_list)

    ## 주간 인기 카페 PK ##
    for i in cafe_score:
        hit_pk_list.append(i.pk)
    # print(hit_pk_list)

    ## 주간 인기 카페 이미지 ##
    for i in hit_pk_list:
        cafe = CafeImage.objects.get(image_id=i)
        hit_cafe.append(cafe)
    #print(hit_cafe)

    ## 주간 인기 카페 정보 ##
    for i in hit_pk_list:
        cafe = Cafe.objects.get(pk=i)
        hit_cafe_name_list.append(cafe)
    #print(hit_cafe_name_list)

    ## 전체 점수 PK ##
    for i in cafe_score_total:
        total_score_pk_list.append(i.pk)
    #print(total_score_pk_list)

    ## 전체 점수 ##
    for i in total_score_pk_list:
        score = CafeScore.objects.get(pk=i)
        total_score_list.append(score)
    #print(total_score_list)

    ## 댓글 수 ##
    for i in total_score_pk_list:
        comment = Comment.objects.filter(post=i)
        comment_list.append(comment)
    # print(comment_list)

    page = request.GET.get('page', '1')
    paginator = Paginator(cafe_list, '16')
    page_obj = paginator.page(page)

    page_image = request.GET.get('page', '1')
    paginator_image = Paginator(image_list, '16')
    page_obj_image = paginator_image.page(page_image)

    page_score = request.GET.get('page', '1')
    paginator_score = Paginator(total_score_list, '16')
    page_obj_score = paginator_score.page(page_score)

    page_comment = request.GET.get('page', '1')
    paginator_comment = Paginator(comment_list, '16')
    page_obj_comment = paginator_comment.page(page_comment)

    zip_list = zip(page_obj, page_obj_score, page_obj_comment, page_obj_image)
    popular_weeks_list = zip(hit_cafe, cafe_score, hit_cafe_name_list)

    context = {
        'cafe': cafe_list,
        'page_obj': page_obj,
        'hit_cafe': hit_cafe,
        'cafe_score': cafe_score,
        'mylist': popular_weeks_list,
        'zip_list': zip_list,
        'cafe_score_total': cafe_score_total,
        'comment_list': comment_list,
    }
    return render(request, 'home.html', context)

def cafe_detail(request, pk):
    cafe_detail = get_object_or_404(Cafe, pk=pk)
    if request.method == "POST":
        user = request.user
        comments = request.POST.get('comment')
        comment = Comment(
            post = cafe_detail,
            author=user,
            comment=comments,
        )
        comment.save()
        return redirect('detail', pk)
    else:
        cafe_name_1 = Cafe.objects.filter(id=pk+1)
        cafe_name_2 = Cafe.objects.filter(id=pk+2)
        cafe_name_3 = Cafe.objects.filter(id=pk+3)
        cafe_name_4 = Cafe.objects.filter(id=pk+4)
        cafe_name_pre = Cafe.objects.filter(id=pk-1)
        cafe_image = CafeImage.objects.filter(image_id=pk)
        cafe_image_1 = CafeImage.objects.filter(image_id=pk+1)
        cafe_image_2 = CafeImage.objects.filter(image_id=pk+2)
        cafe_image_3 = CafeImage.objects.filter(image_id=pk+3)
        cafe_image_4 = CafeImage.objects.filter(image_id=pk+4)
        cafe_score = CafeScore.objects.filter(id=pk)
        cafe_score_1 = CafeScore.objects.filter(id=pk+1)
        cafe_score_2 = CafeScore.objects.filter(id=pk+2)
        cafe_score_3 = CafeScore.objects.filter(id=pk+3)
        cafe_score_4 = CafeScore.objects.filter(id=pk+4)
        cafe_theme = CafeTheme.objects.filter(theme_id=pk)
        comment = Comment.objects.filter(post=pk).order_by('-create_at')
        current_comment = Comment.objects.filter(post=pk).order_by('-create_at')[:1]
        context = {
            'cafe_name_pre': cafe_name_pre,
            'detail': cafe_detail,
            'image': cafe_image,
            'score': cafe_score,
            'name_1': cafe_name_1,
            'name_2': cafe_name_2,
            'name_3': cafe_name_3,
            'name_4': cafe_name_4,
            'image_1': cafe_image_1,
            'image_2': cafe_image_2,
            'image_3': cafe_image_3,
            'image_4': cafe_image_4,
            'score_1': cafe_score_1,
            'score_2': cafe_score_2,
            'score_3': cafe_score_3,
            'score_4': cafe_score_4,
            'comment': comment,
            'current_comment': current_comment,
            'cafe_theme': cafe_theme,
        }
        return render(request, 'cafe_detail.html', context)
def cafe_map(request):
    return render(request, 'cafe_map.html')

def search_result(request):
    query = None
    total_score_pk_list = []
    total_score_list = []
    comment_list = []
    image_pk_list = []
    image_list = []

    cafe_score_total = CafeScore.objects.all()

    if 'search' in request.GET:
        query = request.GET.get('search')
        cafe_list = Cafe.objects.all().filter(Q(name=query) | Q(name__contains=query) | Q(add1=query) | Q(add1__contains=query) | Q(add2=query) | Q(add2__contains=query))
        for i in cafe_list:
            image_pk_list.append(i.pk)
        print(image_pk_list)

        for i in image_pk_list:
            image = CafeImage.objects.get(image_id=i)
            image_list.append(image)
        print(image_list)

        ## 전체 점수 ##
        for i in image_pk_list:
            score = CafeScore.objects.get(pk=i)
            total_score_list.append(score)
        # print(total_score_list)

        ## 댓글 수 ##
        for i in image_pk_list:
            comment = Comment.objects.filter(post=i)
            comment_list.append(comment)

        page = request.GET.get('page', '1')
        paginator = Paginator(cafe_list, '16')
        page_obj = paginator.page(page)

        page_image = request.GET.get('page', '1')
        paginator_image = Paginator(image_list, '16')
        page_obj_image = paginator_image.page(page_image)

        page_score = request.GET.get('page', '1')
        paginator_score = Paginator(total_score_list, '16')
        page_obj_score = paginator_score.page(page_score)

        page_comment = request.GET.get('page', '1')
        paginator_comment = Paginator(comment_list, '16')
        page_obj_comment = paginator_comment.page(page_comment)


        zip_list = zip(page_obj, page_obj_score, page_obj_comment, page_obj_image)

        return render(request, 'search_result.html', {'query': query, 'page_obj': page_obj, 'zip_list': zip_list,})
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

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")

        driver = webdriver.Chrome(options=chrome_options)
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
    location = ["서울", "경기", "충북", "충남", "전북", "전남", "강원", "경북", "경남", "제주", "울릉도", "독도"]
    smoke = ["모두 금연석", "일부 금연석", "모두 흡연석"]
    reservation = ["가능", "불가", "세미나룸 예약"]
    restroom = ["업소내위치", "업소외위치", "개별화장실", "공용화장실"]
    delivery = ["배달", "포장"]
    ballet = ["전용/30분 무료", "업소앞", "주차안됨", "전용", "임대/1시간 무료", "전용/2시간 무료", "타워/기계식", "무료/공영주차장", "전용/3시간 주차 무료", "타워", "임대/인근 공영주차장", "무료/공영", "발렛파킹", "임대", "업소앞/주중 : 2시간 무료 / 주말 : 1시간 무료", "가게 옆 유료주차장 이용",
              "전용/1시간30분 무료주차", "1시간 무료", "유료/한강공원 주차장", "죽녹원 무료 공용주차장 앞", "업소앞/주변 추가 주차 가능", "자전거 주차 가능", "전용/1시간 1000원", "유료/공영주차장"]
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
        'location': location,
        'smoke': smoke,
        'reservation': reservation,
        'restroom': restroom,
        'delivery': delivery,
        'ballet': ballet,
    }
    return render(request, 'category.html', context)

def category_result(request):
    select_theme = request.POST.getlist('theme', None)
    select_location = request.POST.getlist('location', None)
    select_smoke = request.POST.getlist('smoke', None)
    select_reservation = request.POST.getlist('reservation', None)
    select_restroom = request.POST.getlist('restroom', None)
    select_delivery = request.POST.getlist('delivery', None)
    select_ballet = request.POST.getlist('ballet', None)
    select_cafe = request.GET.get('name')
    cafe_pre_list = []
    cafe_next_list = []
    cafe_name_list = []
    pk_pre_list = []
    pk_next_list = []
    filter_pk_list = []
    image_list = []
    score_list = []
    comment_list = []
    select_item = [select_location, select_smoke, select_reservation, select_restroom, select_delivery, select_ballet, select_theme]
    q = Q()
    w = Q()
    e = Q()
    r = Q()
    t = Q()
    x = Q()
    y = Q()
    z = Q()
    theme_pk_list = []
    if select_theme:
        z |= Q(theme__in=select_theme)
    theme = CafeTheme.objects.filter(z)

    #        for i in select_theme:
    for i in theme:
        theme_pk_list.append(i.theme_id)
    for i in theme_pk_list:
        x |= Q(pk=i.pk)

    if select_location:
        for i in select_location:
            q |= Q(add1__contains=i)

    if select_smoke:
        for i in select_smoke:
            w |= Q(smoke__contains=i)

    if select_reservation:
        for i in select_reservation:
            e |= Q(reservation__contains=i)

    if select_restroom:
        for i in select_restroom:
            r |= Q(restroom__contains=i)

    if select_delivery:
        for i in select_delivery:
            t |= Q(delivery__contains=i)

    if select_ballet:
        for i in select_ballet:
            y |= Q(ballet__contains=i)

    for i in theme_pk_list:
        cafe = Cafe.objects.filter(theme_id=i.pk)
        for j in cafe:
            cafe_pre_list.append(j.name)
            pk_pre_list.append(j.pk)

    for value in cafe_pre_list:
        if value not in cafe_next_list:
            cafe_next_list.append(value)
    cafe = Cafe.objects.filter(name=select_cafe)

    for value in pk_pre_list:
        if value not in pk_next_list:
            pk_next_list.append(value)

    for i in pk_next_list:
        cafe_name = Cafe.objects.get(pk=i)
        cafe_name_list.append(cafe_name)

    filter_cafe = Cafe.objects.filter(q & w & e & r & t & x)

    for i in filter_cafe:
        filter_pk_list.append(i.pk)

    ### 카페 이미지 ###
    for i in filter_pk_list:
        images = CafeImage.objects.get(image_id=i)
        image_list.append(images)

    ### 카페 점수 ###
    for i in filter_pk_list:
        scores = CafeScore.objects.get(score_id=i)
        score_list.append(scores)

    ### 카페 댓글 ###
    for i in filter_pk_list:
        comment = Comment.objects.filter(post=i)
        comment_list.append(comment)

    zip_list = zip(filter_cafe, score_list, comment_list, image_list)

    result_list = zip(cafe_name_list, pk_next_list, filter_cafe)
    # print(list) #전체 카페
    context = {
        'cafe': cafe,
        'result_list': result_list,
        'zip_list': zip_list,
        'select_item': select_item,
    }
    return render(request, 'category_result.html', context)


def hashtag(request, theme):
    hash_tag = theme
    cafe_obj_list = []
    cafe_pk_list = []
    image_list = []
    score_list = []
    comment_list = []
    theme = CafeTheme.objects.filter(theme=theme)
    for i in theme:
        cafe_obj_list.append(i.theme_id)
    print(cafe_obj_list)

    #i.pk로 뽑자
    for i in cafe_obj_list:
        cafe_pk_list.append(i.pk)
    print(cafe_pk_list)

    ### 카페 이미지 ###
    for i in cafe_pk_list:
        images = CafeImage.objects.get(image_id=i)
        image_list.append(images)

    ### 카페 점수 ###
    for i in cafe_pk_list:
        scores = CafeScore.objects.get(score_id=i)
        score_list.append(scores)

    ### 카페 댓글 ###
    for i in cafe_pk_list:
        comment = Comment.objects.filter(post=i)
        comment_list.append(comment)

    zip_list = zip(cafe_obj_list, score_list, comment_list, image_list)
    context = {
        'hash_tag': hash_tag,
        'zip_list': zip_list,
    }
    return render(request, 'hash_tag.html', context)