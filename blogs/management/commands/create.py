from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
	def add_arguments(self, parser):
		parser.add_argument('todo')
	def handle(self,  *args, **options):
		todo = options['todo']
		self.stdout.write(self.style.SUCCESS('Successfully create todo:  ' + todo