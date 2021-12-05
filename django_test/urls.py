"""django_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from search.views import index
from rest_framework.routers import DefaultRouter
from DrugIntro.views import DrugIntroViewSet
from DrugSearch.views import DrugSearchViewSet
from django_test.adapter import drugInfo

router = DefaultRouter()
router.register(r'DrugIntro', DrugIntroViewSet, basename='common')
router.register(r'DrugSearch', DrugSearchViewSet, basename='common')

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^show/', index),
    # path("api/news/", include("search.urls")),
    url(r'^DIP/', include(router.urls)),  #DIP：Drug Information Paltform
    url(r'^drugInfo/', drugInfo),  # 測試接前端
]
