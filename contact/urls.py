from django.urls import path
from app1 import views
from django.contrib import admin
from contact.views import success, contact

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.contact, name='contact'),
    path('success/', success, name='success'),

]


