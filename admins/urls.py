from django.urls import path
from .views import login_view,user_logout

urlpatterns = [
    path('login/',login_view,name='login'),
    path('logout/',user_logout,name='logout')
]