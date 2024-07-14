from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.AMirzaLoginView.as_view(), name='login'),
    path('logout/', views.AMirzaLogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),

    path('customer/', views.all_customers_view, name='all-customers'),
    path('customer/profile/', views.CustomerProfileView.as_view(), name='customer-profile'),

    path('staff/', views.all_staffs_view, name='all-staffs'),
    path('staff/profile/', views.StaffProfileView.as_view(), name='staff-profile'),
    path('superuser/profile/', views.SuperuserProfileView.as_view(), name='superuser-profile'),
]
