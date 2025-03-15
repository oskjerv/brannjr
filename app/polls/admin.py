from django.contrib import admin



# Register your models here.
from .models import Squad, Match, Player

class PlayerAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        
        if db_field.name == "player":
            kwargs["queryset"] = Squad.objects.filter(active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Player, PlayerAdmin)


admin.site.register(Squad)
admin.site.register(Match)
#admin.site.register(Player)

admin.site.site_header = "Brannjr"
admin.site.site_title = "Brannjr"
admin.site.index_title = "Brannjr"