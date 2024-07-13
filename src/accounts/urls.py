from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.AMirzaLoginView.as_view(), name='login'),
    path('logout/', views.AMirzaLogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
]
