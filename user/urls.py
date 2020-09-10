from django.urls import path
from .views      import (
     SignUpView, 
     SignInView,
     EmailCheckerView, 
     GoogleSignInView,
     ApplicationView,
     ApplicationStatusView
     )    

urlpatterns = [
     path('/intro', EmailCheckerView.as_view()),
     path('/signup', SignUpView.as_view()),
     path('/signin', SignInView.as_view()),
     path('/googlesignin', GoogleSignInView.as_view()),
     path('/application', ApplicationView.as_view()),
     path('/applicationstatus', ApplicationStatusView.as_view())
]