from django.urls import re_path, path
from jobs import views


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    # 职位列表路径
    re_path(r"^joblist/", views.joblist, name="joblist"),
    re_path(r"^job/(?P<job_id>\d+)/$", views.detail, name="detail"),

    path("resume/add/", views.ResumeCreateView.as_view(), name="resume-add"),
    path("resume/<int:pk>", views.ResumeDetailView.as_view(), name="resume-detail"),

    path('sentry-debug/', trigger_error),
    # 首页自动跳转到职位列表
    re_path(r"^$", views.joblist, name="name")
]