from django.contrib import admin

# Register your models here.
from django.contrib import admin
from musics.models import Music

class ShowMusic(admin.ModelAdmin):
    list_display = ('id','song')

admin.site.register(Music,ShowMusic)