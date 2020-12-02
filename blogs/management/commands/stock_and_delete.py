from django.core.management.base import BaseCommand, CommandError
from blogs.models import Racelist, Learningdata, Racedata
import datetime
from django.utils import timezone

class Command(BaseCommand):
	def handle(self, *args, **options):

		def rand_ints_nodup(a, b, k):
			ns = []
			while len(ns) < k:
				n = random.randint(a, b)
				if not n in ns:
					ns.append(n)
			return ns

		sample = Racedata.objects.filter(time_result__gt = 0).filter(lackparams =0)
		for i in range(len(sample)):
			p = Learningdata(horse_data = sample[i].horse_data, time_result = sample[i].time_result,
			Xmean = 0, Xstd = 0, Ymean = 0, Ystd = 0, test_score = 0 )
			p.save()

		if len(Learningdata.objects.all()) > 6200:
			new_added_num = len(sample)
			del_model = Learningdata.objects.order_by('?')[:new_added_num]
			for dm in del_model:
				dm.delete()

		comp_time =  timezone.now() - datetime.timedelta(days = 3)
		racelist = Racelist.objects.filter(date__lte = comp_time )
		racelist.delete()
		self.stdout.write(self.style.SUCCESS('Successfully delete 3days ago data and stock test data!!'))
		#The Hobby-dev plan allows a maximum of 10,000 rows
		#learning data が6100になったら、ランダムで追加分を削除する必要がある。