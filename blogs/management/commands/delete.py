from django.core.management.base import BaseCommand, CommandError
from blogs.models import Racelist
import datetime
from django.utils import timezone

class Command(BaseCommand):
	def handle(self, *args, **options):
		comp_time =  timezone.now() - datetime.timedelta(days = 3)
		racelist = Racelist.objects.filter(date__lte = comp_time )
		racelist.delete()
		self.stdout.write(self.style.SUCCESS('Successfully delete 3days ago data'))