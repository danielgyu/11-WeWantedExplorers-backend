from django.urls import path

from .views import SubcategoryView

urlpatterns = [
    path('', SubcategoryView.as_view()),
]
