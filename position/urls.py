from django.urls import path

from .views import PositionView, LogoView, PositionDetailView

urlpatterns = [
    path('', PositionView.as_view()),
    path('/<int:id>', PositionDetailView.as_view()),
    path('/logo', LogoView.as_view()),
]
