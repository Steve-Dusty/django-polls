from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('polls/<int:question_id>/detail/', views.detail, name='detail'),
    path('polls/<int:question_id>/vote/', views.vote, name='vote'),
    path('polls/<int:question_id>/results', views.results, name='results'),
    path('createquestion/',
         views.createquestion, name='createquestion'),
    path('createchoice/<int:question_id>',
         views.createchoice, name='createchoice'),
]
