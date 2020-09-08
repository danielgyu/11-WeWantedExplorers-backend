from django.urls import path

from .views import (SubcategoryView,
                    PremiumCompanyView,
                    AverageSalaryView,
                    SalaryView,
                    TagRecommendView,
                    CompanyTagView)

urlpatterns = [
    path('', SubcategoryView.as_view()),
    path('/premium', PremiumCompanyView.as_view()),
    path('/salary', SalaryView.as_view()),
    path('/average/<int:id>', AverageSalaryView.as_view()),
    path('/tags/<int:id>', CompanyTagView.as_view()),
    path('/recommend',TagRecommendView.as_view()),
]
