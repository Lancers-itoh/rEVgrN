from django.core.management.base import BaseCommand, CommandError
from blogs.models import Racelist, Learningdata
import datetime
from django.utils import timezone

class Command(BaseCommand):
	def handle(self, *args, **options):

		sample = Racedata.objects.filter(time_result__gt = 0).filter(lackparams =0)
		for i in range(len(sample)):
			p = Learningdata(horse_data = sample[i].horse_data, time_result = sample[i].time_result,
			Xmean = 0, Xstd = 0, Ymean = 0, Ystd = 0, test_score = 0 )
			p.save()


		comp_time =  timezone.now() - datetime.timedelta(days = 3)
		racelist = Racelist.objects.filter(date__lte = comp_time )
		racelist.delete()
		self.stdout.write(self.style.SUCCESS('Successfully delete 3days ago data and stock test data!!'))