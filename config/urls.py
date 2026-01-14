
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from core.views import UserLoginView, dashboard


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('', include('core.urls')),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

]
