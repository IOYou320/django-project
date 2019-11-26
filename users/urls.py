from django.urls import path
from .views import Login_view,Message,Register,Active


urlpatterns = [
    path('login/',Login_view.as_view()),
    path('message/',Message.as_view()),
    path('register/',Register.as_view()),
    path('active/',Active.as_view())
]