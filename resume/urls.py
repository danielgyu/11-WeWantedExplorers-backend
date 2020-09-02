from django.urls import path
from .views      import (
    NewResumeView,
    ResumesView,
    ResumeView
)

urlpatterns = [
     path('/new', NewResumeView.as_view()),
     path('/list', ResumesView.as_view()),
     path('/<int:id>', ResumeView.as_view())
]
