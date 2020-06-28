from django.core.management.base import BaseCommand, CommandError
import numpy as np
import csv
from blogs.models import Learningdata

class Command(BaseCommand):
    def handle(self, *args, **options):

	    with open('static/data/OldEXlist3.csv') as f:
	        reader = csv.reader(f)
	        OldEX = [row for row in reader]

	    print(OldEX[1][0])

	    with open('static/data/OldRES3.csv') as f:
	        reader = csv.reader(f)
	        OldRES = [row for row in reader]
	    print(OldRES[0][0])

	    for i in range(len(OldEX)):
	    	p = Learningdata(horse_data = OldEX[i][0], time_result = OldRES[i][0],
	    		Xmean = 0, Xstd = 0, Ymean = 0, Ystd = 0, test_score = 0)
	    	p.save()