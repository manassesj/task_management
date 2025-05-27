from django.urls import path
from django.urls import path, include

urlpatterns = [
    path('api/', include('users.urls')),
    path('api/', include('tasks.urls')),
]
