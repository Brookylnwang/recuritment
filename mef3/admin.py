from django.contrib import admin
from mef3.models import Mef
import csv
import logging

@admin.action(description="更改状态")
def make_path_status(modeladmin, request, queryset):
    print(queryset.values("mef_report_file_status"))
    for i in queryset.values("mef_report_file_status"):
        if str(i["mef_report_file_status"]) == "1":
            queryset.update(mef_report_file_status="2")
        else:
            queryset.update(mef_report_file_status="1")


def upload_csv_as_model(modeladmin, ):
    f = open("/Users/wangsheng/Downloads/mef3.csv", encoding="utf-8")
    reader = csv.reader(f)
    mef3_content_list = []
    for row in reader:
        # logging.error("This row content is %s" % str(row))
        mef3_content_list.append(str(row))
    logging.info("This row content is %s" % str(mef3_content_list[0]))



upload_csv_as_model.short_description = u"导入mef3信息"

# Register your models here.
class MefAdmin(admin.ModelAdmin):
    list_display = ("mef_server_name", "mef_date", "mef_report_file", "mef_report_file_status")

    actions = [upload_csv_as_model, make_path_status]

admin.site.register(Mef, MefAdmin)
