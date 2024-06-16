from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

# app_name = 'staff'

urlpatterns = [
    path('', views.home, name='website-home'),
    path('about/', views.about, name='website-about'),
    path('book/', views.book, name='book'),
    path('menu/', views.menu, name='menu'),
    path('cart/', views.cart, name='cart'),
    path('order/', views.order, name='order'),  # TODO: NOT NEEDED


    path('customer/', views.all_staffs, name='all-customers'),
    path('customer/<str:customer_username>/', views.customer, name='customer-profile'),

    path('staff/', views.all_staffs, name='all-staffs'),
    path('staff/<str:staff_username>/', views.staff_profile, name='staff-profile')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
