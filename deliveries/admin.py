from django.contrib import admin
from .models import CustomUser, Parcel,DeliveryProof
# Register your models here.




class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('role', 'is_active')
    ordering = ('username',)

class ParcelAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'sender', 'courier', 'receiver_name', 'created_at')
    search_fields = ('title', 'description', 'sender__username', 'receiver_name')
    list_filter = ('status', 'sender', 'courier')
    readonly_fields = ('created_at', 'delivered_at')

    



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Parcel, ParcelAdmin)
admin.site.register(DeliveryProof)