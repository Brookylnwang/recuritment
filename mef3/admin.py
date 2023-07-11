from django.contrib import admin
from mef3.models import Mef
import csv
import logging


def upload_csv_as_model(modeladmin, ):
    f = open("/Users/wangsheng/Downloads/wang.txt", encoding="utf-8")
    reader = csv.reader(f)
    mef3_content_list = []
    for row in reader:
        # logging.error("This row content is %s" % str(row))
        mef3_content_list.append(str(row))
    logging.info("This row content is %s" % str(mef3_content_list[0]))



upload_csv_as_model.short_description = u"导入mef3信息"

# Register your models here.
class MefAdmin(admin.ModelAdmin):
    list_display = ("mef_server_name", "mef_date", "mef_report_file")

    actions = [upload_csv_as_model]

admin.site.register(Mef, MefAdmin)
