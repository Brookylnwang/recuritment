from django.contrib import admin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import path
from django import forms

from mef3.models import Mef
import csv
import logging


# exportable_fields = ("mef_report_file_status")


@admin.action(description="更改状态")
def make_path_status(modeladmin, request, queryset):
    server_names = ""
    for obj in queryset:
        if str(obj.mef_report_file_status) == "1":
           obj.mef_report_file_status = 2
        elif str(obj.mef_report_file_status) == "2":
           obj.mef_report_file_status = 1
        obj.save()
        server_names = server_names + "," + obj.mef_server_name
    if queryset.count() > 3:
        messages.success(request, "一大批服务器状态已改变")
    else:
        messages.success(request, "服务器%s状态已改变" % server_names)

# @admin.action(description="导入mef3信息")
#def upload_csv_as_model(modeladmin, request, queryset):
#    pass


def get_urls(self):
    urls = super().get_urls()
    my_urls = [
        path('import-csv/', self.import_csv)
    ]
    return my_urls + urls


@admin.action(description="导入mef3")
def import_csv(self, request):
    if request.method == "POST":
        print(1)
        csv_file = request.FILES["csv_file"]
        reader = csv.reader(csv_file)
        print(reader)

        messages.success(request, "Your csv file upload successfully")
        return redirect("..")
    form = CsvImportForm()
    payload = {"form": form}
    return render(
        request, "templates/mef3/csv_form.html", payload
    )
    # logging.info("This row content is %s" % str(mef3_content_list[0]))


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


# Register your models here.
class MefAdmin(admin.ModelAdmin):
    list_display = ("mef_server_name", "mef_date", "mef_report_file", "mef_report_file_status")

    actions = [import_csv, make_path_status]

admin.site.register(Mef, MefAdmin)
