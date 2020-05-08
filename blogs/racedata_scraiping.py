import requests
from bs4 import BeautifulSoup
import datetime
import re
import numpy as np
from models import Racelist, Racedata

def get_bs(url):
    res = requests.get(url)
    res.encoding = res.apparent_encoding
    res = res.text
    soup = BeautifulSoup(res, 'html.parser')
    return(soup)

def JC_WinRateOf(code):
    jockey_url = "https://db.netkeiba.com/jockey/result/" + code
    jockey_info = get_bs(jockey_url).find("table")
    if jockey_info != None:
        Jockey_win_ratio = "0" + jockey_info.find_all("tr")[2].find_all("td")[18].text
    return(Jockey_win_ratio)


def Parse_from(race_pk):

    race = Racelist.objects.get(pk = race_pk)
    soup = get_bs(race.url)
    ## Universal data in this race
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
        horse_info = row.find_all("td")[4].text
        if horse_info.find("牡") == -1:
                #"牝"
            Gender = 0
        else:
            Gender = 1
                #"牡"
        Age = re.sub("\\D", "", horse_info)

        Burden = row.find_all("td")[5].text.strip()
        print("Burnden:{}".format(Burden))

        Jockey_code = re.sub("\\D", "", row.find(class_ = "Jockey").a.get("href"))
        Jockey_win_rate = JC_WinRateOf(Jockey_code)

        horse_name = row.find_all("td")[3]
        Horsename = horse_name.text.strip()
        horse_url = horse_name.a.get("href")
        horse_soup = get_bs(horse_url)
        profile_trs = horse_soup.find(class_ = "db_prof_area_02").find_all("tr")
        if  str(profile_trs [8]).find("通算成績") == -1:
            a,b,c,d,e = re.findall(r'[0-9]+', profile_trs [7].find("td").text)[0:5]
        else:
            a,b,c,d,e = re.findall(r'[0-9]+', profile_trs [8].find("td").text)[0:5]
        Horse_win_rate = ( int(c) + int(d) + int(e))/int(a)
        race_results = horse_soup.find(class_ = "db_h_race_results").tbody.find_all("tr")
        tds = race_results[0].find_all("td")
        row_list = ()
        tds_prev =  race_results[0].find_all("td")
        if len(tds_prev[14].text[1:5]) > 0:
            Distance_prev = tds_prev[14].text[1:5]
            Time_diff_prev = tds_prev[18].text
            FirstTime = 0
        else:
            Distance_prev = 0
            Time_diff_prev = 0
            FirstTime = 1
            
        try:
            weight_data_set = row.find(class_ = "Weight").text.split("(")
            Weight = weight_data_set[0]
            Delta_weight = weight_data_set[1].rstrip(")")
        except:
            Horse_weight, Delta_weight = re.findall(r'[0-9\+\-]+', tds[23].text)
     
        pre_ex = np.array([Horse_win_rate, Age, Gender, Number, Prize, Burden, Distance_prev, Time_diff_prev, Weight, Delta_weight, Jockey_win_rate,  Distance, FirstTime]).reshape(1,13)
        horse_data = ""
        for d in pre_ex:
            horse_data = horse_data + str(d) + str("/")

        race.racedata_set.create(horse_name = Horsename, horse_data = horse_data)    

                #header = 
        print("Processing...")


for race in Racelist.objects.all():
    Parse_from(race.pk)




