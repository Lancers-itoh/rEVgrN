from django.urls import path
from . import views

# set the application namespace
# https://docs.djangoproject.com/en/2.0/intro/tutorial03/
app_name = 'smsusers'

urlpatterns = [
	path('', views.index, name='index'),
	path('<int:email_id>/', views.detail, name='detail'),
	path('email/', views.create, name='create'),
]