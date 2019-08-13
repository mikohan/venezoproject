from django.urls import path

from .views import (
    Blog,
    BlogDetailSlugView,
)

urlpatterns = [
    path('', Blog.as_view(), name='blog'),
    path('<slug:slug>/', BlogDetailSlugView.as_view(), name='detailed'),
]
