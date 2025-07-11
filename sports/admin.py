from django.contrib import admin
from .models import Player

class PlayerAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'team', 'final_price', 'image_tag']
    readonly_fields = ['image_tag']

admin.site.register(Player, PlayerAdmin)