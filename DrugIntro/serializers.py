from rest_framework import serializers
from DrugIntro.models import DrugIntro

class DrugIntroSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugIntro
        # fields = '__all__'
        fields = ['id', 'ch_name', 'en_name']
        # id = serializers.IntegerField()
        # name = serializers.CharField(source='drug_name')
        # eng_name = serializers.CharField(source='drug_eng_name')
        # desc = serializers.CharField(source='drug_desc')
