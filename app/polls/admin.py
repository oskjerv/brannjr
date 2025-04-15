from django.contrib import admin



# Register your models here.
from .models import Squad, Match, Player

class PlayerAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        
        if db_field.name == "player":
            kwargs["queryset"] = Squad.objects.filter(active=True)
            
        if db_field.name == "match":
            kwargs["queryset"] = Match.objects.order_by("-date")  # Newest first
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        newest_match = Match.objects.order_by("-date").first()
        if newest_match:
            initial['match'] = newest_match.pk
        return initial

admin.site.register(Player, PlayerAdmin)
admin.site.register(Squad)

#admin.site.register(Player)

admin.site.site_header = "Brannjr"
admin.site.site_title = "Brannjr"
admin.site.index_title = "Brannjr"