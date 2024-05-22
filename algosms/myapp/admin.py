from django.contrib import admin
# from .models import *
from .models import ClientDetail,ClientSignal,SYMBOL , Client_SYMBOL_QTY
# Register your models here.

# admin.site.register(MAddress)
# admin.site.register(MCompany)
# @admin.register(Account)
# class AccountAdmin(admin.ModelAdmin):
#     list_display = ('user_id','is_client','is_client','email','date_joined','last_login','is_admin','is_active','is_staff','is_superuser')  # Adjusted to valid fields
#     search_fields = ['user_id','is_client','is_client','email','date_joined','last_login','is_admin','is_active','is_staff','is_superuser']
#     list_per_page = 10 
    
 
@admin.register(ClientDetail)
class ProductAdmin(admin.ModelAdmin):
   
    list_display = [field.name for field in ClientDetail._meta.fields] 
''' 
@admin.register(ClientSignal)
class ClientSignalAdmin(admin.ModelAdmin):
    list_display = ('user','SYMBOL','TYPE','QUANTITY','ENTRY_PRICE','EXIT_PRICE','profit_loss','cumulative_pl','created_at')  # Adjusted to valid fields
    search_fields = ['user','SYMBOL','TYPE','QUANTITY','ENTRY_PRICE','EXIT_PRICE','profit_loss','cumulative_pl','created_at']
    list_per_page = 10 
'''    
@admin.register(ClientSignal)
class ProductAdmin(admin.ModelAdmin):
   
    list_display = [field.name for field in ClientSignal._meta.fields]     
   
   
@admin.register(SYMBOL)
class SYMBOLAdmin(admin.ModelAdmin):
    list_display = ('user','SYMBOL','created_at')  # Adjusted to valid fields
    search_fields = ['user','SYMBOL','created_at']
    list_per_page = 10    
    

@admin.register(Client_SYMBOL_QTY)
class ProductAdmin(admin.ModelAdmin):
   
    list_display = [field.name for field in Client_SYMBOL_QTY._meta.fields]         