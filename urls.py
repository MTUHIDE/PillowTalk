from django.contrib import admin
from django.urls import include, path
from mainsite import views

urlpatterns = [
   path('', include('mainsite.urls')),
   path('admin/', admin.site.urls),
   path('submit', views.submit),
]