from django.contrib import admin
from lineup.models import Channel, Lineup, Key
# Register your models here.


@admin.register(Lineup)
class LineupAdmin(admin.ModelAdmin):
    list_display = ('zipcode', 'provider')


admin.site.register(Channel)
admin.site.register(Key)
