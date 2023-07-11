from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


ServerGroup = [
    (0, "WAVE1组"),
    (1, "WAVE2组"),
    (2, "DEV组"),
    (3, "windows组"),
    (4, "AIOps组")
]


class Mef(models.Model):
    mef_date = models.DateTimeField(verbose_name="获取mef时间", null=True)
    mef_server_name = models.CharField(max_length=20, blank=False, verbose_name="服务器名称")
    mef_report_file = models.FileField(upload_to='uploads/%Y/%m/%d/',blank=True, max_length=254, verbose_name="文件名路径")

    class Meta:
        verbose_name = _('收集mef3')
        verbose_name_plural = _("收集mef3文件")


