from django.db import models

# Create your models here.
#資料表裡有的欄位
class DrugIntro(models.Model):
    ch_name = models.TextField()
    en_name = models.TextField()
    # desc = models.TextField()

    class Meta:
        db_table = "drug_type"

    # 取得毒品詳細資訊
    def drugInfo(**kwargs):
        drug_id = kwargs.get('id')
        if id:
            result = DrugIntro.objects.raw('SELECT * FROM drug_type WHERE id = %s', [drug_id])
        else: #基本上應該是不會跑這個
            result = "No drug found"
        return result

    # 取得毒品清單
    def drugList(**kwargs):
        num = kwargs.get('num')
        start_id = kwargs.get('start_id')
        if id:
            result = DrugIntro.objects.raw('SELECT * FROM drug_type WHERE id >= %s LIMIT %s', [start_id,num])
        else:  # 基本上應該是不會跑這個
            result = "No drug found"
        return result
