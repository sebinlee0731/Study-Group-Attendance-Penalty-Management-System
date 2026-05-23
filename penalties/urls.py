from django.urls import path

from .views import (
    PenaltyListView,
    PaymentCreateView,
    PaymentCompleteView
)

urlpatterns = [
    path('penalties/', PenaltyListView.as_view()),
    path('payments/', PaymentCreateView.as_view()),
    path('payments/<int:payment_id>/complete/', PaymentCompleteView.as_view()),
]