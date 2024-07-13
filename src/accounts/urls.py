from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.AMirzaLoginView.as_view(), name='login'),
    path('logout/', views.AMirzaLogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),


    path('customer/', views.all_customers_view, name='all-customers'),
    path('customer/<str:customer_username>/', views.customer_profile, name='customer-profile'),

    path('staff/', views.all_staffs_view, name='all-staffs'),
    path('staff/<str:staff_username>/', views.staff_profile, name='staff-profile'),
]
