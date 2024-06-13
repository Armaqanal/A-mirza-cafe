from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='website-home'),
    path('about/', views.about, name='website-about'),
    path('book/', views.book, name='book'),
    path('menu/', views.menu, name='menu'),
    path('cart/', views.menu, name='cart'),
    path('order/', views.menu, name='order'), # TODO: NOT NEEDED
    path('customer/', views.menu, name='customer-profile'),
    path('staff/', views.staff, name='staff-profile')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
