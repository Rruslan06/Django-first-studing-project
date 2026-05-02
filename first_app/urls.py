from django.urls import path
from . import views

app_name = "first_app" #Пространство имен ссылок, чтобы потом использовать в связке с name и не хардкордить шаблоны


urlpatterns = [
    #http:127.0.0.1:8000/first_app/
    path("", views.IndexView.as_view(), name='index'), 

    #http:127.0.0.1:8000/first_app/5/
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),

    #http:127.0.0.1:8000/first_app/5/results/
    path("<int:pk>/results/", views.ResultView.as_view(), name="results"),

    #http:127.0.0.1:8000/first_app/5/vote/
    path("<int:question_id>/vote/",  views.vote, name="vote"),

]