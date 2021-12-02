from django.contrib import admin

# Register your models here.
from django.contrib import admin
from DrugIntro.models import DrugIntro

# admin.site.register(DrugIntro)

#列出欄位
class ShowDrugInfo(admin.ModelAdmin):
    list_display = ('id', 'name', 'eng_name', 'desc')

admin.site.register(DrugIntro, ShowDrugInfo)  #admin/admin123
