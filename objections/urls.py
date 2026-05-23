from django.urls import path

from .views import (
    ObjectionCreateView,
    MyObjectionListView,
    ObjectionProcessView
)

urlpatterns = [
    path('objections/', ObjectionCreateView.as_view()),
    path('objections/me/', MyObjectionListView.as_view()),
    path('objections/<int:objection_id>/process/', ObjectionProcessView.as_view()),
]