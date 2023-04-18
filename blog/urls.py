from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('article/<int:pk>/', views.detail, name='detail'),
    path('dates/<int:year>/<int:month>', views.dates, name='dates'),
    path('categories/<int:pk>', views.category, name='categories'),
    path('tags/<int:pk>', views.tag, name='tags'),
    path('auther/<int:pk>', views.auther, name='auther'),
]
