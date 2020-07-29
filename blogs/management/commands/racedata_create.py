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

        def ToTotal_time(text_time):
            minutes, seconds,milliseconds = map(int, re.split('[:.]',text_time))
            #deltatime = datetime.timedelta(minutes=minutes, seconds=seconds, milliseconds = milliseconds*100)
            deltatime = timedelta(minutes=minutes, seconds=seconds, milliseconds = milliseconds*100)
            total_time = deltatime.total_seconds()
            return(total_time)


        def Parse_from(soup, race):
            Horse_name_list = list()
            initial_registered_horses = race.racedata_set.values_list("horse_name", flat=True)

            string_distance = soup.find(class_ = "RaceData01").span.text
            Distance = re.sub("\\D", "", string_distance)
            RaceData02_spans = soup.find(class_ = "RaceData02").find_all("span")
            Number = re.sub("\\D", "", RaceData02_spans[7].text)
            Prize = RaceData02_spans[8].text.split(":")[1].split(",")[0]

            try:
                table_trs = soup.find("table").tbody.find_all("tr")
                table_thead = soup.find("table").thead.find_all("th")
                print(len(table_thead))
            except:
                table_trs = soup.find(class_ = "RaceTableArea").table.find_all(class_ = "HorseList")
                table_thead = soup.find(class_ = "RaceTableArea").table.thead.find_all("th")
                    
                #<th class="Umaban sort_common" rowspan="2"><div class="Inner_Shutuba">馬<br/>番<span class="sort_icon"></span></div></th>
            for i in range(len(table_thead)):
                if table_thead[i].text == "馬番":
                    umaban_index = i
                elif table_thead[i].text == "馬体重(増減)":
                    weight_index = i
                    print(weight_index)
                    break

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

                try:
                    time_result = row.find_all(class_ = "RaceTime")[0].text
                    TimeResult = ToTotal_time(time_result)
                    print("This race is passed")
                except:
                    TimeResult = 0
                #print("JCwin:{}".format(Jockey_win_rate))
                try:
                    #Num
                    umaban = row.find_all("td")[umaban_index].text.strip()
                except:
                    umaban = "未定"
                if umaban == '':
                    umaban = "未定"
                print(umaban)
                horse_name = row.find_all("td")[3]
                Horsename = horse_name.text.strip()
                Horse_name_list.append(Horsename)
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
                weight_data_set = row.find_all("td")[weight_index]
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
                #race に含まれているものを確認。
                #race.racedata_set.all()とHorsenameを比較して存在しないものは消す

                #[horse['horse_name'] for horse in race.racedata_set.values("horse_name")]
                if obs:
                    print("UPDSTE!")
                    obs.update(horse_name = Horsename,  horse_code = umaban, horse_data = horse_data, lackparams = lackparams, time_result = TimeResult)
                else:
                    race.racedata_set.create(horse_name = Horsename, horse_code = umaban, horse_data = horse_data, lackparams = lackparams, time_result = TimeResult)
            
            #End of for statement to each row
            print(Horse_name_list)
            print(initial_registered_horses)
            if len(initial_registered_horses) > 0:
                print("Initial delete execute")
                delete_name = ( set(Horse_name_list) ^ set(initial_registered_horses) ) & set(initial_registered_horses)
                print(delete_name)
                race.racedata_set.filter(horse_name__in = delete_name).delete()
                #inital_regstered_horses && Horse_name_list
        ##end of Parse_from function
        #24h 以内にupdateがあるものはraceobsから除外する
        #子オブジェクトの作成がいつかってこと！
        # created_at - timedelta.now() > 24h &&
        # min ( created_at - timedelta.now() ) 
        yesterday = timezone.now() + timedelta(days=-2)
        # these records are not updated yet
        # high speed scraiping should be refrain
        raceobs = Racelist.objects.filter(racedata_updated_at__lt = yesterday)
        #raceobs = Racelist.objects.all()
        last_pk = Racelist.objects.last().pk
        print(yesterday)
        for race in raceobs:
            print(race.racedata_updated_at)
            print(race.url)
            print("{}/{}".format(race.pk, last_pk))
            soup = get_bs(race.url)
            if soup != 0:
                Parse_from(soup, race)
            #ここまできたら子要素の更新は完了なので、日付更新.
            Racelist.objects.filter(pk = race.id).update(racedata_updated_at = timezone.now())
        
        #最後に更新されたものを取得したとてo
