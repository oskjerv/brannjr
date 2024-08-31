import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django.db import models

from django.utils import timezone

def validate_rating(value):
    if value < 1 or value > 6:
        raise ValidationError(
            _("Verdien må være mellom 1 og 6."),
            params={"value": value},
        )
def validate_non_negative(value):
    if value < 0:
        raise ValidationError(
            _("Verdien må være over 0."),
            params={"value": value},
        )

#COPY polls_squad(name, shirt_no) FROM '/Users/oivind/Library/CloudStorage/OneDrive-UniversityofBergen/Privat/prosjekter/brannjr/data/squad.txt' DELIMITER ';' CSV HEADER;
class Squad(models.Model):
    name = models.CharField(max_length=200)
    shirt_no = models.IntegerField(default=None)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'shirt_no'], name='unique_name_shirtno')
        ]
    
    def __str__(self):
        return self.name + ' (no. '+ str(self.shirt_no) +')'
    
    class Meta:
        
        ordering = ('shirt_no',) 
        verbose_name_plural = "Spillere i stallen"
        verbose_name = "Spillerstall"
    
class Match(models.Model):
    #match = models.CharField(max_length=200)
    opponent = models.CharField(default=None)
    date = models.DateTimeField("Kampdato")
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['opponent', 'date'], name='unique_opponent_date')
        ]
        ordering = ('date', )
        
        verbose_name_plural = "Kamper"
        verbose_name = "Kamp"
    
    def __str__(self):
        return self.opponent + ' - ' + self.date.strftime('%d.%m.%y')
    def get_day(self):
        return self.date.strftime('%d.%m.%y')
    def was_played_recently(self):
        return self.date >= timezone.now() - datetime.timedelta(days=1)

class Player(models.Model):
    POSITION_CHOICES = {
        'GK': 'Målvakt',
        'LB': 'Venstreback',
        'RB': 'Høyreback',
        'LCB': 'Venstre midtstopper',
        'RCB': 'Høyre midtstopper',
        'LDM': 'Venstre defensiv midtbane',
        'HDM': 'Høyre defensiv midtbane',
        'LCM': 'Venstre sentral midtbane',
        'RCM': 'Høyre sentral midtbane',
        'LW': 'Venstreving',
        'RW': 'Høyreving',
        'LAM': 'Venstre offensiv midtbane',
        'RAM': 'Høyre offensiv midtbane',
        'LCF': 'Venstre spiss',
        'RCF': 'Høyre spiss'
    }
    
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    player = models.ForeignKey(Squad, on_delete=models.CASCADE)
    position = models.CharField(
        max_length = 200,
        choices = POSITION_CHOICES
    )
    goals = models.IntegerField(validators=[validate_non_negative], default=0, null=True, blank=True)
    assists = models.IntegerField(validators=[validate_non_negative], default=0, null=True, blank=True)
    started = models.BooleanField(default=True, null=True, blank=True)
    subbed = models.BooleanField(default=False, null=True, blank=True)
    rating = models.IntegerField(validators=[validate_rating], default=0)
    mom_votes = models.IntegerField(default=0)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['match', 'player'], name='unique_match_player')
        ]
        
        verbose_name_plural = "Kamptropp"
        verbose_name = "Kamptropp"
        
    
    
    def rating_string(self):
        if self.rating == 1:
            return 'one'
        elif self.rating == 2:
            return 'two'
        elif self.rating == 3:
            return 'three'
        elif self.rating == 4:
            return 'four'
        elif self.rating == 5:
            return 'five'
        elif self.rating == 6:
            return 'six'
    
    def lastname(self):
        return self.player.name.rsplit(' ', 1)[1]
    def lastname_pos(self):
        return self.player.name.rsplit(' ', 1)[1] + '\n(' + self.position + ')'
    
    def __str__(self):
        return self.player.name + ' (' + self.position + ')' + ' - ' + self.match.opponent
    
