from django.urls import path
from . import views 

urlpatterns =[
    path('home/', views.index, name="index"),
    path('dashboard/', views.admin_page, name="admin_page"),
    path('shop/',views.shop,name="shop"),
    path('table/',views.table_page,name="table_page"),
    path('create_table/',views.create_table,name="create_table"),
    path('delete_product/<int:pk>/', views.delete_product, name='delete'),
    path('edit_product/<int:pk>/', views.edit_product, name='edit_product'),
    path('create_user/', views.create_user, name='create_user'),
    path('admins/', views.admins, name='admins'),
    path('edit_user/<int:pk>/', views.edit_user, name='edit_user'),
    path('delete_user/<int:pk>/', views.delete_user, name='delete_user'),
    path('hisobot/', views.hisobot, name='hisobot'),
    path('users/', views.foydalanuvchilar, name='users'),
    path('boshliq/', views.boshliq_page, name='boshliq_page'),
    path('sotuvchi/', views.seller_page, name='sotuvchi_page'),
    path('admin_tekshiruv/', views.product_requests, name='product_requests'),
    path('qabul_product/<int:pk>/', views.qabul_product, name='qabul_product'),
    path('tuzatish/<int:pk>/',views.tuzatish_product,name='tuzatish_product')
]
