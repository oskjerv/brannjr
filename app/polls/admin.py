from django.contrib import admin

# Register your models here.
from .models import Squad, Match, Player

admin.site.register(Squad)
admin.site.register(Match)
admin.site.register(Player)

admin.site.site_header = "Brannjr"
admin.site.site_title = "Brannjr"
admin.site.index_title = "Brannjr"