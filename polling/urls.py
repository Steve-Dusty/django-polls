from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('polls/<int:question_id>/detail/', views.detail, name='detail'),
    path('polls/<int:question_id>/vote/', views.vote, name='vote'),
    path('createpoll/',
         views.createpoll, name='createpoll'),
    path('createchoice/', views.createchoice, name='createchoice')

]
