import logging

from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext
from django.contrib.auth import get_permission_codename

from mef3.models import Mef


# Register your models here.
class MefAdmin(admin.ModelAdmin):
    list_display = ("mef_server_name", "mef_date", "mef_report_file", "mef_report_file_status")

    actions = ["upload_csv_as_model", "make_path_status","add_default_path"]

    def get_actions(self, request):
        actions = super().get_actions(request)
        if request.user.username[0].upper() != "A":
            if "delete_selected" in actions:
                del actions["delete_selected"]
        return actions


    @admin.action(description="更改状态")
    def make_path_status(self, request, queryset):
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

    @admin.action(
        description="导入数据",
        permissions=["publish"],
    )
    def upload_csv_as_model(self, request, queryset):
        logging.info("这是检验信息")

    def has_publish_permission(self, request):
        opts = self.opts
        codename = get_permission_codename("publish", opts)
        return request.user.has_perm("%s.%s" % (opts.app_label, codename))


    @admin.action(description="修改为不存在")
    def add_default_path(self, request, queryset):
        updated = queryset.update(mef_report_file_status="2")
        self.message_user(
            request,
            ngettext(
                "%s story was successfully marked as published.",
                "%s stories were successfully marked as published.",
                updated,
            )
            % updated,
            messages.SUCCESS
        )



# admin.site.disable_action("delete_selected")



admin.site.register(Mef, MefAdmin)
