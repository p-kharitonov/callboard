from django.urls import path
from .views import *

urlpatterns = [
    path('<int:pk>', PostDetailView.as_view(), name='post'),
]