from django.db import models
from django.contrib.auth.models import User

class Mep(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    mep_id = models.IntegerField(primary_key=True)
    fullname = models.CharField(max_length=200)
    gender = models.CharField(max_length=10, null=True)
    birth_date = models.DateField(null=True)
    eu_group_short = models.CharField(max_length=200)
    eu_group_long = models.CharField(max_length=200)
    national_party = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
    twitter = models.URLField(null=True)
    facebook = models.URLField(null=True)
    website = models.URLField(null=True)
    eu_page_url = models.URLField(null=True)
    photo_url = models.URLField(null=True)
    def __str__(self):
        return self.fullname


class Vote(models.Model):
    vote_number = models.PositiveSmallIntegerField(default=0)
    vote_id   = models.IntegerField(primary_key=True)
    vote_date = models.DateField()
    xml_url   = models.URLField()
    title     = models.CharField(max_length=1000)
    text_id   = models.CharField(max_length=200)
    epref     = models.CharField(max_length=200)
    total_for = models.IntegerField()
    total_against = models.IntegerField()
    total_abs  = models.IntegerField()
    short_desc = models.CharField(max_length=1000, null=True)
    summary_url = models.URLField()
    procedure_url = models.URLField(default=None, null=True)
    debate_url  = models.URLField(default=None, null=True)
    topic       = models.CharField(max_length=100)
    meps      = models.ManyToManyField(Mep, through='Position')


class Position(models.Model):
    mep = models.ForeignKey(Mep, on_delete=models.CASCADE)
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE)
    stance = models.CharField(max_length=3, null=True)  # for, ag, abs
    comment = models.TextField(blank=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['mep', 'vote'], name='unique_position')
        ]

    def __str__(self):
        return f"mep_id: {self.mep.mep_id}, vote_id: {self.vote_id}"

