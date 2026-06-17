from ctypes import sizeof
from operator import contains
from platform import release
from tkinter import NO

from django.db import models
from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator

from .models import MediaModels, Genre
from django.db.models import Count
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm

ALL_GENRES = ['喜剧', '爱情', '动作', '科幻', '动画', '悬疑', '犯罪',  '惊悚', '冒险', '音乐', '历史', '奇幻', '恐怖', '战争', '传记', '歌舞', '武侠', '情色', '灾难', '西部', '纪录片', '短片']

ALL_TYPES = ["电影", "电视剧", '动漫', '剧场版']

ALL_COUNTRIES = ["华语", "欧美", "日韩", "东南亚", "中国大陆", "中国香港", "中国台湾", "韩国", "日本", "美国", "英国", "法国", "德国", "意大利", "西班牙", "印度", "泰国", "俄罗斯", "加拿大", "澳大利亚", "爱尔兰", "瑞典", "巴西", "丹麦"]

ALL_AREAS = ["华语", "欧美", "日韩", "东南亚"]

ALL_YEARS = ["2020年代", "2026", "2025", "2024", "2023", "2022", "2021", "2020", "2010年代", "2000年代", "1990年代", "1980年代", "70年代", "60", "更早"]

ALL_EARS = ["2020年代", "2010年代", "2000年代", "1990年代", "1980年代", "70年代", "60", "更早"]

ALL_SORTS = ['名称', '上映时间', '片长']

LIST_TYPE = {'movie': "电影", 'tv': "电视剧", 'animation': '动漫', 'animated_film': '剧场版', 'documentary': '纪录片', 'category': '分类'}

def media_detail(request, media_id):
    media = get_object_or_404(MediaModels, pk=media_id)
    return render(request, 'media_detail.html', {
        'media': media,
        'active_nav': media.type,
        'list_type': LIST_TYPE
    })

def index(request):
    movies = MediaModels.objects.filter(type='movie')[:14]
    tv_shows = MediaModels.objects.filter(type='tv')[:14]
    # genre_counts = get_genre_counts()
    return render(request, 'index.html', {
        'movies': movies,
        'tv_shows': tv_shows,
        # 'genre_counts': genre_counts,
        'active_nav': 'home',
    })

def media_filter(request, media_type: str):
    genre = request.GET.get('genre', '').strip()
    sort = request.GET.get('sort', '').strip()
    qs = MediaModels.objects.filter(type=media_type)
    media_total = qs.count()
    if genre and genre != '全部':
        qs = qs.filter(genres__name=genre)
    
    if sort == 'new':
        qs = qs.order_by('-release_date')
    elif sort == 'hot':
        # 如何定义最热？
        pass
    elif sort == 'score':
        qs = qs.order_by('-douban_rating')
        
    paginator = Paginator(qs, 30)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)
    media_list = f'media_view:{media_type}_list'
    genre_counts = Genre.objects.annotate(
        count=Count(
            "mediamodels",
            filter=models.Q(mediamodels__type=media_type),
            distinct=True
        )
    )
    
    filters = {
        "sort": sort
    }
    return render(request, 'index.html', {
        'media_type': LIST_TYPE[media_type],
        'page_obj': page_obj,
        'genre_counts': genre_counts,
        'current_genre': genre,
        'active_nav': media_type,
        'media_total': media_total,
        'media_list': media_list,
        "filters": filters,
    })


def movie_list(request):
    return media_filter(request, "movie")


def tv_list(request):
    return media_filter(request, "tv")


def animated_film_list(request):
    return media_filter(request, "animated_film")

def animation_list(request):
    return media_filter(request, "animation")

def documentary_list(request):
    return media_filter(request, "documentary")

def category_list(request):
    type = request.GET.get('type', '').strip()
    country = request.GET.get('country', '').strip()
    genre = request.GET.get('genre', '').strip()
    year = request.GET.get('year', '').strip()
    qs = MediaModels.objects.all()
    sort = request.GET.get('sort', '').strip()
    if type and type != '全部':
        qs = qs.filter(type=[k for k, v in LIST_TYPE.items() if v == type][0])

    # c存储数据为jsonFile，无法直接匹配
        
    if country and country != '全部':
        if country in ALL_AREAS:
            qs = qs.filter(area=country)
        else:
            qs = qs.filter(countries__name=country)

    if genre and genre != '全部':
        qs = qs.filter(genres__name=genre)
    
    if year and year != '全部':
        if year in ALL_EARS:
            qs = qs.filter(release_ear=year)
        else:
            qs = qs.filter(release_years=year)
            
    if sort == 'new':
        qs = qs.order_by('-release_date')
    elif sort == 'hot':
        # 如何定义最热？
        pass
    elif sort == 'score':
        qs = qs.order_by('-douban_rating')
        
    paginator = Paginator(qs, 30)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)

    # ===== 统一状态 =====
    filters = {
        "type": type,
        "genre": genre,
        "country": country,
        "year": year,
        "sort": sort
    }
    return render(request, 'index.html', {
        'all_types': ALL_TYPES,
        'all_countries': ALL_COUNTRIES,
        'all_genres': ALL_GENRES,
        'all_years': ALL_YEARS,

        'media_list': 'media:category_list',
        'active_nav': 'category',
        'media_type': LIST_TYPE['category'],

        'page_obj': page_obj,

        'media_total': qs.count(),
        "filters": filters,
    })