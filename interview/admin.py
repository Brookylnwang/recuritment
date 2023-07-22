import logging

from django.contrib import admin
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.contrib import messages

from datetime import datetime
from interview.models import Candidate
from jobs.models import Resume
from interview.candidate_fieldset import default_fieldsets, default_fieldsets_first, default_fieldsets_second
from django.db.models import Q


import csv
# Register your models here.

logger = logging.getLogger(__name__)

exportable_fields = ('username', 'city', 'phone', 'bachelor_school', 'master_school', 'degree', 'first_result',
                     'first_interviewer_user', 'second_result', 'second_interviewer_user', 'hr_result', 'hr_score',
                     'hr_remark', 'hr_interviewer_user')

# 导出文件
def export_model_as_csv(modeadmin, request, queryset):
    response = HttpResponse(content_type='text/csv', charset='utf-8-sig')
    field_list = exportable_fields
    response['Content-Disposition'] = 'attachment; filename=recuritment-candidates-list-%s.csv' % (
        datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
    )

    ## 写入表头
    writer = csv.writer(response)
    writer.writerow(
        [ queryset.model._meta.get_field(f).verbose_name.title() for f in field_list]
    )

    for obj in queryset:
        ## 单行的记录, 各字段的值写入csv
        csv_line_values = []
        for field in field_list:
            field_object = queryset.model._meta.get_field(field)
            field_value = field_object.value_from_object(obj)
            csv_line_values.append(field_value)
        writer.writerow(csv_line_values)

    # logger.info("%s exported %s candidate records" % (request.user, len(queryset)))
    logger.error("%s exported %s candidate records" % (request.user, len(queryset)))

    return response

export_model_as_csv.short_description = u'导出为csv文件'
export_model_as_csv.allowed_permissions = ('export',)


# 候选人管理类
class CandidateAdmin(admin.ModelAdmin):
    exclude = ('creator', 'created_date', 'modified_date')

    actions = [export_model_as_csv]

    # 用户名不是以A开头的没有删除权限
    def get_actions(self, request):
        actions = super().get_actions(request)
        if request.user.username[0].upper() != "A":
            if "delete_selected" in actions:
                del actions["delete_selected"]
        return actions

    list_display = (
        "username", "city", "bachelor_school", "get_resume", "first_score", "first_result", "first_interviewer_user",
        "second_result", "second_interviewer_user", "hr_score", "hr_result", "last_editor"
    )

    # 筛选条件
    list_filter = ('city', 'first_result', 'second_result', 'hr_result', 'first_interviewer_user', 'second_interviewer_user', 'hr_interviewer_user')

    # 查询字段
    search_fields = ('username', 'phone', 'email', 'bachelor_school',)

    # 列表页排序字段
    ordering = ('hr_result', 'second_result', 'first_result')

    default_list_editable = ('first_interviewer_user', 'second_interviewer_user',)

    readonly_fields = ('first_interviewer_user', 'second_interviewer_user')

    def get_resume(self, obj):
        if not obj.phone:
            return ""
        resumes = Resume.objects.filter(phone=obj.phone)
        if resumes and len(resumes) > 0:
            return mark_safe(u'<a href="/resume/%s" target="_blank">%s</a>' % (resumes[0].id, "查看简历"))
        return ""

    get_resume.short_description = "查看简历"
    get_resume.allow_tags = True

    # HR 有导出权限，面试官没有导出权限
    def has_export_permission(self, request):
        opts = self.opts
        return request.user.has_perm('%s.%s' % (opts.app_label, "export"))

    def get_list_editable(self, request):
        group_names = self.get_group_names(request.user)

        if request.user.is_superuser or 'hr' in group_names:
            return self.default_list_editable
        return ()

    def get_changelist_instance(self, request):
        self.list_editable = self.get_list_editable(request)
        return super(CandidateAdmin, self).get_changelist_instance(request)

    def get_group_names(self, user):
        group_names = []
        for g in user.groups.all():
            group_names.append(g.name)
        return group_names

    def get_readonly_fields(self, request, obj):
        group_names = self.get_group_names(request.user)

        if 'interviewer' in group_names:
            logger.info("interviewer is in user's group for %s" % request.user.username)
            return ('first_interviewer_user', 'second_interviewer_user',)
        return ()

    # 对于一 二面面试官，只能看到他们自己的页面
    def get_queryset(self, request):
        qs = super(CandidateAdmin, self).get_queryset(request)

        group_names = self.get_group_names(request.user)
        if request.user.is_superuser or 'hr' in group_names:
            return qs
        return Candidate.objects.filter(
            Q(first_interviewer_user=request.user) | Q(second_interviewer_user=request.user)
        )


    # 一面面试官仅填写一面反馈，二面面试官填写二面反馈
    def get_fieldsets(self, request, obj=None):
        group_names = self.get_group_names(request.user)

        if 'interviewer' in group_names and obj.first_interviewer_user == request.user:
            return default_fieldsets_first
        if 'interviewer' in group_names and obj.second_interviewer_user == request.user:
            return default_fieldsets_second
        return default_fieldsets

    def save_model(self, request, obj, form, change):
        obj.last_editor = request.user.username
        if not obj.creator:
            obj.creator = request.user.username
        obj.modified_date = datetime.now()
        obj.save()

admin.site.register(Candidate, CandidateAdmin)
