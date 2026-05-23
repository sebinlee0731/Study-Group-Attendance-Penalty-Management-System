from django.contrib import admin
from django.urls import path, include
from studies.views import StudyHomeView
from studies.views import StudyHomeView, AttendanceManagePageView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from studies.views import(
    StudyHomeView,
    AttendanceManagePageView,
    FineDashboardPageView,
    AppealPageView,
    AuditLogPageView
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('logs/', AuditLogPageView.as_view(), name='audit_log_page'),

    path('', StudyHomeView.as_view(), name='study_home'),

    path('attendance/', AttendanceManagePageView.as_view(), name='attendance_manage'),

    path('appeals/', AppealPageView.as_view(), name='appeal_page'),

    path('fines/', FineDashboardPageView.as_view(), name='fine_dashboard'),

    path(
        'api/v1/token/',
        TokenObtainPairView.as_view(),
    ),

    path(
        'api/v1/token/refresh/',
        TokenRefreshView.as_view(),
    ),

    path('api/v1/', include('studies.urls')),
    path('api/v1/', include('attendances.urls')),
    path('api/v1/', include('penalties.urls')),
    path('api/v1/', include('objections.urls')),
    path('api/v1/', include('accounts.urls')),
    path('api/v1/', include('audits.urls')),
]