from django.contrib import admin
from lineup.models import Channel, Lineup, Key
# Register your models here.


@admin.register(Lineup)
class LineupAdmin(admin.ModelAdmin):
    list_display = ('zipcode', 'provider')
    search_fields = ('zipcode', 'provider')


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'icon')
    search_fields = ('number', 'name', 'icon')

admin.site.register(Key)
