"""
URL configuration for algosms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from myapp import views
from django.contrib.auth import views as auth_views
# from .views import client_dashboard, multibank_login, multibank_login_api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',views.index , name='index'),
   
    
    # Your admin authenticate url is here
    path('admin_register/', views.create_superuser, name='create_superuser'),
    path('adminlogin/',views.admin_login, name='admin_login'),
    path('admin_change_password/',views.admin_change_password,name='admin_change_password'),
    path('client_base/',views.client_base,name='client_base'),
    
    
    # Your client authenticate url is here
    path('',views.client_login, name='client_login'),
    path('registration/',views.registration, name='registration'),
    path('clientlist',views.client_list, name='client_list'),
    path('update_client/<str:user_id>/', views.update_client, name='update_client'),
    path('delete_client/<str:user_id>/', views.delete_client, name='delete_client'),
    
    path('adminlogout/',views.logoutAdmin, name='logoutAdmin'),
    path('logout/',views.logoutUser, name='logoutUser'),
    # path('profile/', views.profile, name='profile'),
    path('changepassword/',views.change_password, name='change_password'),
    
    
    path('add_singnal_qty/',views.add_singnal_qty, name='add_singnal_qty'),
    path('symbol_inactive/',views.symbol_inactive, name='symbol_inactive'),
    
    
    path('admin_dashboard/',views.admin_dashboard, name='admin_dashboard'),
    path('admin_message/',views.admin_message, name='admin_message'),
    path('admin_signals/',views.admin_signals, name='admin_signals'),
    path('admin_thistory/',views.admin_thistory, name='admin_thistory'),
    path('admin_tstatus/',views.admin_tstatus, name='admin_tstatus'),
    # path('admin_client/',views.admin_client,name='admin_client'),
    path('admin_help_center/',views.admin_help_center,name='admin_help_center'),
    path('settings/',views.Settings,name='Settings'),
    
    path('dashboard/',views.client_dashboard, name='client_dashboard'),
    path('signals/',views.client_signals, name='client_signals'),
    path('tradehistory/',views.client_trade_history, name='client_trade_history'),
    path('tradingstatus/',views.client_tstatus, name='client_tstatus'),
    path('multibank/',views.multibank, name='multibank'),
   
    
    path('create_symbol_qty/',views.create_client_symbol_qty, name='create_client_symbol_qty'),
    path('symbol_qty_list/',views.client_symbol_qty_list, name='client_symbol_qty_list'),
    path('edit_symbol_qty/',views.edit_client_symbol_qty, name='edit_client_symbol_qty'),
    path('delete_symbol_qty/',views.delete_client_symbol_qty, name='delete_client_symbol_qty'),
  
    path('symbol_list/',views.symbol_list, name='symbol_list'),
    path('create_symbol/',views.create_symbol, name='create_symbol'),
    path('update_symbol/<int:symbol_id>/', views.update_symbol, name='update_symbol'),
    path('delete_symbol/<int:symbol_id>/', views.delete_symbol, name='delete_symbol'),
    
    path('logout/', auth_views.LogoutView.as_view(next_page='client_login'), name='logout'),
    path('', auth_views.LoginView.as_view(), name='client_login'),
    
    path('client_help_center/', views.client_help_center, name='client_help_center'),
    path('admin_help_center/', views.admin_help_center, name='admin_help_center'),

    path('Analysis/',views.Analysis, name='Analysis'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
