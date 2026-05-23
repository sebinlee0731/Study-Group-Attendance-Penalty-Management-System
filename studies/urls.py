from django.urls import path

from .views import (
    StudyListView,
    StudyDetailView,
    StudyMemberListView,
    StudyScheduleListView
)

urlpatterns = [
    path('studies/', StudyListView.as_view()),
    path('studies/<int:pk>/', StudyDetailView.as_view()),
    path('studies/<int:study_id>/members/', StudyMemberListView.as_view()),
    path('studies/<int:study_id>/schedules/', StudyScheduleListView.as_view()),
]