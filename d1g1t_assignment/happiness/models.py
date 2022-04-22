from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator,\
    MaxValueValidator
import secrets
import datetime

class Team(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name}'

# we are generating a 32 character long token for each user.
def auth_token_generator():
    return secrets.token_urlsafe(32)[:32]


class Member(models.Model):
    member = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    average_happiness = models.IntegerField(default=0)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    token = models.CharField(max_length=32, default=auth_token_generator)

    def __str__(self):
        return f'{self.team}-{self.member}'


class HappinessLevel(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    # happiness_level value >=0 and <=10. The value 0 indicates
    # Unhappy/sad and value 10 indicates Extreme Happy.
    happiness_level = models.IntegerField(validators=[
        MinValueValidator(0.0), MaxValueValidator(10.0)
    ])

    def __str__(self):
        return f'{self.member}-{self.date}: {self.happiness_level}'

    # member and date are unique so members can submit once per day
    class Meta:
        unique_together = ('member', 'date')
