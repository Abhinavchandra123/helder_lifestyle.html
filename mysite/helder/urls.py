
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from .views import *


urlpatterns = [

    path('loginn/',loginadmin, name="login"),
    path('logout/',logoutUser, name="logout"),
    # path('register/', views.registerUser, name="register"),
    path('adminhome/', adminhome, name='adhome'),
    path('addproduct/',addPhoto, name='addph'),
    path('product/',product, name='pdct'),
    path('topwear/',topwear, name='topw'),
    path('bottomwear/',bottom, name='bott'),
    path('kidswear/',kids, name='kids'),

    path('contact',contact, name='contact'),
    path('about/',about, name='about'),
    path('delb/<id>',delb,name="delb"),
    path('productedit/<str:pk>/',form2Photo, name='edit'),
    ]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)