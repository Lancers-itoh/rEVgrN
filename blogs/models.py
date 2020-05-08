from django.db import models
from django.urls import reverse
import datetime
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # https://docs.djangoproject.com/en/2.0/ref/class-based-views/generic-editing/
        # return reverse('blogs:detail', kwargs={'pk': self.pk})
        return reverse('blogs:index')

class Racelist(models.Model):
    url = models.TextField(unique=True)
    title = models.TextField()
    place = models.TextField()
    date = models.DateTimeField()
    def __str__(self):
        return self.url

    def was_passed_in_days(self,day):
        return self.date < timezone.now() - datetime.timedelta(days = day)

class Racedata(models.Model):
    racelist = models.ForeignKey(Racelist, on_delete=models.CASCADE)
    horse_name = models.TextField()
    horse_data = models.TextField()
    def __str__(self):
        return self.horse_data
        
    #[float(s) for s in a.split('/')]
    #[Horse_win_rate, Age, Gender, Number, Prize, Burden, Distance_prev, Time_diff_prev, Weight, Delta_weight, Jockey_win_rate,  Distance, FirstTime]
    #c = q.choice_set.create(Horse_name='Jus', horse_data = '[ss,s,s,s,s,s,s,]')

