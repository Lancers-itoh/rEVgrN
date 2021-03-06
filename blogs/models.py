from django.db import models
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta


class Racelist(models.Model):
    url = models.TextField(unique=True)
    title = models.TextField()
    place = models.TextField()
    date = models.DateTimeField()
    racedata_updated_at = models.DateTimeField()
    race_num = models.IntegerField()
    def __str__(self):
        return self.url

    def was_passed_in_days(self,day):
        return self.date < timezone.now() - datetime.timedelta(days = day)

class Racedata(models.Model):
    racelist = models.ForeignKey(Racelist, on_delete=models.CASCADE)
    horse_name = models.TextField()
    horse_code = models.TextField(default = "未定")
    horse_data = models.TextField()
    time_result = models.TextField()
    lackparams = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.horse_data

class Learningdata(models.Model):
    horse_data = models.TextField()
    time_result = models.TextField()
    Xmean = models.TextField()
    Xstd = models.TextField()
    Ymean = models.FloatField()
    Ystd = models.FloatField()
    test_score = models.FloatField()
        
    #[float(s) for s in a.split('/')]
    #[Horse_win_rate, Age, Gender, Number, Prize, Burden, Distance_prev, Time_diff_prev, Weight, Delta_weight, Jockey_win_rate,  Distance, FirstTime]
    #c = q.choice_set.create(Horse_name='Jus', horse_data = '[ss,s,s,s,s,s,s,]')

