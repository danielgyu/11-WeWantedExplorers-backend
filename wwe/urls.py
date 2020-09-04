from django.urls import path, include

urlpatterns = [
    path('user', include('user.urls')),
    path('positions', include('position.urls')),
    path('companies', include('company.urls')),
]
