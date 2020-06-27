from django.core.management.base import BaseCommand, CommandError
from blogs.models import Racelist, Racedata
from django.utils import timezone
import requests
from bs4 import BeautifulSoup
import re
import numpy as np
from datetime import datetime, timedelta


class Command(BaseCommand):
	def handle(self, *args, **options):
		def get_bs(url):
			try:
				res = requests.get(url)
				res.encoding = res.apparent_encoding
				res = res.text
				soup = BeautifulSoup(res, 'html.parser')
				return(soup)
			except:
				return(0)

		def JC_WinRateOf(code):
			jockey_url = "https://db.netkeiba.com/jockey/result/" + code
			jockey_info = get_bs(jockey_url).find("table")
			if jockey_info != None:
				Jockey_win_ratio = "0" + jockey_info.find_all("tr")[2].find_all("td")[18].text
			return(Jockey_win_ratio)


		def Parse_from(soup, race):
			string_distance = soup.find(class_ = "RaceData01").span.text
			Distance = re.sub("\\D", "", string_distance)
			RaceData02_spans = soup.find(class_ = "RaceData02").find_all("span")
			Number = re.sub("\\D", "", RaceData02_spans[7].text)
			Prize = RaceData02_spans[8].text.split(":")[1].split(",")[0]
			try:
				table_trs = soup.find("table").tbody.find_all("tr")
			except:
				table_trs = soup.find(class_ = "RaceTableArea").find_all(class_ = "HorseList")
			for row in table_trs:
				lackparams = 0
				horse_info = row.find_all("td")[4].text
				if horse_info.find("牡") == -1:
					#"牝"
					Gender = 0
				else:
					Gender = 1
					#"牡"
				#print("Gender:{}".format(Gender))
				Age = re.sub("\\D", "", horse_info)
				#print("Age:{}".format(Age))
				Burden = row.find_all("td")[5].text.strip()
				if Burden == '未定':
					print('未定')
					Burden = 0
					lackparams = lackparams + 1

				#print("Burden:{}".format(Burden))
				try:
					Jockey_code = re.sub("\\D", "", row.find(class_ = "Jockey").a.get("href"))
					Jockey_win_rate = JC_WinRateOf(Jockey_code)
				except:
					Jockey_win_rate = 0
				#print("JCwin:{}".format(Jockey_win_rate))
				horse_name = row.find_all("td")[3]
				Horsename = horse_name.text.strip()
				horse_url = horse_name.a.get("href")
				horse_soup = get_bs(horse_url)
				try:
					profile_trs = horse_soup.find(class_ = "db_prof_area_02").find_all("tr")
					if  str(profile_trs [8]).find("通算成績") == -1:
						a,b,c,d,e = re.findall(r'[0-9]+', profile_trs [7].find("td").text)[0:5]
					else:
						a,b,c,d,e = re.findall(r'[0-9]+', profile_trs [8].find("td").text)[0:5]
					if(a != '0'):
						Horse_win_rate = ( int(c) + int(d) + int(e))/int(a)
					else:
						Horse_win_rate = 0
				except:
					Horse_win_rate = 0
					lackparams = lackparams + 1
				#print("Horsewin:{}".format(Horse_win_rate))
				try:
					race_results = horse_soup.find(class_ = "db_h_race_results").tbody.find_all("tr")
					for i in range(len(race_results)):
						tds_prev = race_results[0].find_all("td")
						Distance_prev = tds_prev[14].text[1:5]
						Time_diff_prev = tds_prev[18].text
						if len(Distance_prev) > 1 and len(Time_diff_prev)  > 1:
							FirstTime = 0
							break
						if i == len(race_results)-1:
							lackparams = lackparams + 2
							Distance_prev = 0
							Time_diff_prev = 0
							FirstTime = 1
				except:
					lackparams = lackparams + 2
					Distance_prev = 0
					Time_diff_prev = 0
					FirstTime = 1
				#print("Distance_prev:{}".format(Distance_prev))
				#print("Time_diff_prev:{}".format(Time_diff_prev))
				#print("FirstTime:{}".format(FirstTime))
				try:
					weight_data_set = row.find(class_ = "Weight").text.split("(")
					Horse_weight = weight_data_set[0].strip()
					Delta_weight = re.sub("\\D", "", weight_data_set[1])
				except:
					try:
						Horse_weight, Delta_weight = re.findall(r'[0-9\+\-]+', tds[23].text)
					except:
						lackparams = lackparams + 2
						Horse_weight = 0
						Delta_weight = 0

				#print("Horse_weight:{}".format(Horse_weight))
				#print("Delta_weight:{}".format(Delta_weight))
				pre_ex = np.array([Horse_win_rate, Age, Gender, Number, Prize, Burden, Distance_prev, Time_diff_prev, Horse_weight, Delta_weight, Jockey_win_rate,  Distance, FirstTime])
				horse_data = ""
				for s in pre_ex:
					d = float(s)
					if (not isinstance(d, float)) & (not isinstance(d, int)):
						print("Non num:{}".format(d))
						d = 0
						lackparams = lackparams + 1

					horse_data = horse_data + str(d) + "/"

				print(horse_data)
				print("lack: {}".format(lackparams))
				#元データが更新されている場合これが聞かない。
				obs = race.racedata_set.filter(horse_name = Horsename)
				print(obs)
				if obs:
					print("UPDSTE!")
					obs.update(horse_name = Horsename, horse_data = horse_data, lackparams = lackparams)
				else:
					race.racedata_set.create(horse_name = Horsename, horse_data = horse_data, lackparams = lackparams)

		##end of Parse_from function
		#24h 以内にupdateがあるものはraceobsから除外する
		#子オブジェクトの作成がいつかってこと！
		# created_at - timedelta.now() > 24h &&
		# min ( created_at - timedelta.now() ) 
		yesterday = timezone.now() + timedelta(days=-1)
		# these records are not updated yet
		# high speed scraiping should be refrain
		raceobs = Racelist.objects.filter(racedata_updated_at__lt = yesterday)
		last_pk = Racelist.objects.last().pk
		for race in raceobs:
			print("{}/{}".format(race.pk, last_pk))
			race = Racelist.objects.get(pk = race.pk)
			soup = get_bs(race.url)
			if soup != 0:
				Parse_from(soup, race)
			#ここまできたら子要素の更新は完了なので、日付更新.
			race.racedata_updated_at = timezone.now()

		
		#最後に更新されたものを取得したとてo
