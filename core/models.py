from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    coach = models.CharField(max_length=100, blank=True)
    captain = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    def __str__(self): return self.name

class Tournament(models.Model):
    STATUS_CHOICES = [('Upcoming','Upcoming'),('Ongoing','Ongoing'),('Completed','Completed')]
    name = models.CharField(max_length=120)
    venue = models.CharField(max_length=120, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Upcoming')
    def __str__(self): return self.name

class Player(models.Model):
    ROLE_CHOICES = [('Batter','Batter'),('Bowler','Bowler'),('All-rounder','All-rounder'),('Wicketkeeper','Wicketkeeper')]
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(default=20)
    jersey_number = models.PositiveIntegerField(default=0)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='players')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Batter')
    batting_style = models.CharField(max_length=50, blank=True)
    bowling_style = models.CharField(max_length=50, blank=True)
    matches = models.PositiveIntegerField(default=0)
    runs = models.PositiveIntegerField(default=0)
    batting_average = models.FloatField(default=0)
    strike_rate = models.FloatField(default=0)
    wickets = models.PositiveIntegerField(default=0)
    economy = models.FloatField(default=0)
    fitness = models.PositiveIntegerField(default=75)
    recent_form = models.PositiveIntegerField(default=75)
    catches = models.PositiveIntegerField(default=0)
    def __str__(self): return self.name
