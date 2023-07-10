from django.contrib import admin
from mef3.models import Mef

# Register your models here.
class MefAdmin(admin.ModelAdmin):
    list_display = ("mef_server_name", "mef_date", "mef_report_file")

admin.site.register(Mef, MefAdmin)
