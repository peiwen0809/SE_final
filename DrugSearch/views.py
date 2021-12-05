from django.http import JsonResponse
import numpy as np

from DrugSearch.models import DrugCountry,DrugGender
from DrugSearch.serializers import *

from rest_framework import viewsets
from rest_framework.decorators import action
import matplotlib.pyplot as plt

# Create your views here.
class DrugSearchViewSet(viewsets.ModelViewSet):
    # queryset = DrugCountry.objects.all()
    # serializer_class = DrugCountrySerializer

    imgUrl = 'D:/Users/User/Desktop/SE_IMG/'  # 圖片儲存路徑

    # 畫圖
    def drawPlot(self, imgName):
        # 設定字體以顯示中文
        plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
        plt.rcParams['axes.unicode_minus'] = False
        # 加座標軸文字
        plt.xlabel("年")
        plt.ylabel("人數")
        # 另存圖片，如果要存的話要再show前。否則圖片會是空白
        plt.savefig(self.imgUrl + imgName)
        plt.clf()  # 清除當前圖形
        # plt.show()


    # /api/DrugIntro/getCountryYearNum/
    # 取得一個國家每年的吸毒人數
    @action(detail=False, methods=['post'])
    def getCountryYearNum(self, request):
        #{"id":1}
        country_id = request.data['id']
        countryYearNum = DrugCountry.countryYearNum(country_id=country_id)
        serializer = DrugCountrySerializer(countryYearNum, many=True)  # many=true means queryset 包含多個項目（項目列表）
        if len(serializer.data) == 0:  #TODO 錯誤訊息的格式
            return JsonResponse({"sucecss":False,"desc":"No drug found"})
        # print(serializer.data)
        #取出年份、人數的陣列
        yearArr = []
        numArr = []
        for d in serializer.data:
            yearArr.append(str(d['year']))
            numArr.append(d['num'])
        # 畫圖
        plt.plot(yearArr, numArr, 'r-o')
        imgName = "country_year_num.png"
        self.drawPlot(imgName)
        return JsonResponse({'id':country_id,'img':self.imgUrl + imgName}, safe=False)  # 回傳圖片路徑
        # return JsonResponse(serializer.data,safe=False)  # 為了允許非 dict 對像被序列化，將安全參數設置為 False

    # /api/DrugIntro/getAgeNum/
    # 取得一個國家每年的吸毒人數，依年齡層區分
    @action(detail=False, methods=['post'])
    def getAgeNum(self, request):
        # {"id":1}
        country_id = request.data['id']
        ageNum = DrugAge.ageNum(country_id=country_id)
        ageSet = {}  # 各年齡層人數 {"0-19":{"num":[123,456],"year":[2019,2020]},"20-29":{"num":[123,456],"year":[2019,2020]},...}
        # 將結果取出，存放到特定物件
        for r in ageNum:
            if r.age in ageSet.keys():  # 如果這個年齡層已經有資料了，將資料加入原本的array
                tmp = ageSet.get(r.age)  # 取出毒品種類的人數及年份
                numTmp = tmp.get("num")  # 取出人數
                numTmp.append(r.num)
                yearTmp = tmp.get("year")  # 取出年份
                yearTmp.append(str(r.year))
                ageSet[r.age] = {"num":numTmp,"year":yearTmp}
            else:
                ageSet[r.age] = {"num":[r.num],"year":[str(r.year)]}
        # serializer = DrugAgeSerializer(ageNum, many=True)  # many=true means queryset 包含多個項目（項目列表）
        # if len(serializer.data) == 0:  # TODO 錯誤訊息的格式
        #     return JsonResponse({"sucecss": False, "desc": "No drug found"})
        # print(serializer.data)

        # 畫圖
        for key in ageSet:
            plt.plot(ageSet[key].get("year"), ageSet[key].get("num"),'-o')
        plt.legend(ageSet.keys())  # 圖例說明
        imgName = "age_num.png"
        self.drawPlot(imgName)
        return JsonResponse({'id': country_id, 'img': self.imgUrl + imgName},
                            safe=False)  # 回傳圖片路徑
        # return JsonResponse(serializer.data,safe=False)  # 為了允許非 dict 對像被序列化，將安全參數設置為 False


    # /api/DrugIntro/getGenderNum/
    # 取得一個國家每年的吸毒人數，依性別區分
    @action(detail=False, methods=['post'])
    def getGenderNum(self, request):
        # {"id":1}
        country_id = request.data['id']
        genderNum = DrugGender.genderNum(country_id=country_id)
        # serializer = DrugGenderSerializer(genderNum, many=True)  # many=true means queryset 包含多個項目（項目列表）
        # if len(serializer.data) == 0:  # TODO 錯誤訊息的格式
        #     return JsonResponse({"sucecss": False, "desc": "No drug found"})

        genderSet = {}  # 各性別人數 {"男":{"num":[123,456],"year":[2019,2020]},"女":{"num":[123,456],"year":[2019,2020]}}
        # 將結果取出，存放到特定物件
        for r in genderNum:
            if r.gender in genderSet.keys():  # 如果這個性別已經有資料了，將資料加入原本的array
                tmp = genderSet.get(r.gender)  # 取出性別的人數及年份
                numTmp = tmp.get("num")  # 取出人數
                numTmp.append(r.num)
                yearTmp = tmp.get("year")  # 取出年份
                yearTmp.append(str(r.year))
                genderSet[r.gender] = {"num": numTmp, "year": yearTmp}
            else:
                genderSet[r.gender] = {"num": [r.num], "year": [str(r.year)]}
        # serializer = DrugAgeSerializer(ageNum, many=True)  # many=true means queryset 包含多個項目（項目列表）
        # if len(serializer.data) == 0:  # TODO 錯誤訊息的格式
        #     return JsonResponse({"sucecss": False, "desc": "No drug found"})
        # print(serializer.data)

        # 畫圖
        for key in genderSet:
            plt.plot(genderSet[key].get("year"), genderSet[key].get("num"), '-o')
        plt.legend(genderSet.keys())  # 圖例說明
        imgName = "gender_num.png"
        self.drawPlot(imgName)
        return JsonResponse({'id': country_id, 'img': self.imgUrl + imgName},
                            safe=False)  # 回傳圖片路徑
        # return JsonResponse(serializer.data,safe=False)  # 為了允許非 dict 對像被序列化，將安全參數設置為 False


    # /api/DrugIntro/getDrugTypeNum/
    # 取得一個國家每年的吸毒人數，依毒品種類區分
    @action(detail=False, methods=['post'])
    def getDrugTypeNum(self, request):
        # {"id":1}
        country_id = request.data['id']
        drugTypeNum = DrugType.drugTypeNum(country_id=country_id)
        drugTypeSet = {}  # 各毒品種類人數 {"大麻":{"num":[123,456],"year":[2019,2020]},"海洛因":{"num":[123,456],"year":[2019,2020]}}
        # 將結果取出，存放到特定物件
        for r in drugTypeNum:
            if r.ch_name in drugTypeSet.keys():  # 如果這個毒品種類已經有資料了，將資料加入原本的array
                tmp = drugTypeSet.get(r.ch_name)  # 取出毒品種類的人數及年份
                numTmp = tmp.get("num")  # 取出人數
                numTmp.append(r.num)
                yearTmp = tmp.get("year")  # 取出年份
                yearTmp.append(str(r.year))
                drugTypeSet[r.ch_name] = {"num":numTmp,"year":yearTmp}
            else:
                drugTypeSet[r.ch_name] = {"num":[r.num],"year":[str(r.year)]}
        # serializer = DrugAgeSerializer(ageNum, many=True)  # many=true means queryset 包含多個項目（項目列表）
        # if len(serializer.data) == 0:  # TODO 錯誤訊息的格式
        #     return JsonResponse({"sucecss": False, "desc": "No drug found"})
        # print(serializer.data)

        # 畫圖
        for key in drugTypeSet:
            plt.plot(drugTypeSet[key].get("year"), drugTypeSet[key].get("num"),'-o')
        plt.legend(drugTypeSet.keys())  # 圖例說明
        imgName = "drug_type_num.png"
        self.drawPlot(imgName)
        return JsonResponse({'id': country_id, 'img': self.imgUrl + imgName},
                            safe=False)  # 回傳圖片路徑
        # return JsonResponse(serializer.data,safe=False)  # 為了允許非 dict 對像被序列化，將安全參數設置為 False