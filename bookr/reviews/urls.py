from django.contrib import admin
from django.urls import path
from rest_framework.views import APIView

from . import views, api_views

urlpatterns = [path('books/', views.book_list, name='book_list'),
               path('books/<int:book_id>/', views.book_detail, name='book_detail'),
               path('publishers/new', views.publisher_edit, name='publisher_create'),
               path('publishers/<int:pk>/', views.publisher_edit, name='publisher_edit'),
               path('api/all_books/',api_views.AllBooks.as_view(), name='all_books'),
               path ('book_search/', views.book_search, name='book_search'),
               path('books/<int:book_pk>/reviews/new', views.review_edit, name='review_create'),
               path ('books/<int:book_pk>/reviews/<int:review_pk>', views.review_edit, name ='review_edit')]