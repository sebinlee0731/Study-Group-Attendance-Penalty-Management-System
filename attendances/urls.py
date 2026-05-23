from django.urls import path

from .views import (
    AttendanceCreateView,
    AttendanceListView
)

urlpatterns = [

    path(
        'attendances/',
        AttendanceCreateView.as_view()
    ),

    path(
        'schedules/<int:schedule_id>/attendances/',
        AttendanceListView.as_view()
    ),
]