def LearningData_Parse_from(year):
    import requests
    from bs4 import BeautifulSoup
    import matplotlib.pyplot as plt
    import datetime
    import re
    import numpy as np
    import math
    from datetime import date
    from dateutil.relativedelta import relativedelta
    import numpy.matlib

    def ToTotal_time(text_time):
                minutes, seconds,milliseconds = map(int, re.split('[:.]',text_time))
                deltatime = datetime.timedelta(minutes=minutes, seconds=seconds, milliseconds = milliseconds*100)
                total_time = deltatime.total_seconds()
                return(total_time)

    def get_bs(url):
        res = requests.get(url)
        res.encoding = res.apparent_encoding
        res = res.text
        soup = BeautifulSoup(res, 'html.parser')
        return(soup)
            

    def age_calculator(d0):
        dy = relativedelta(date.today(), d0)
        return dy.years



    EX_list = np.empty((1,14))
    EX_list = np.delete(EX_list, 0,0)

    for year in range(5,9):
        for i in range(100):
            #appendするlistは次元を揃えるため"delete"の手続きが必要
            #pace_list = np.empty((1,2))
            #pace_list = np.delete(pace_list, 0, 0)
            url = "https://db.netkeiba.com/horse/" + str(201) + str(year) + str(100100 + i)
            print(url)
            res = requests.get(url)
            res.encoding = res.apparent_encoding
            res = res.text
            soup = BeautifulSoup(res, 'html.parser')
            race_table = soup.find(class_ = "db_h_race_results")
            if  race_table != None:
                print("XXXXXXXXXXXXXXXX")
                race_results = race_table.tbody.find_all("tr")
                horse_profile = soup.find(class_ = "db_prof_area_02")
                age_text = re.findall(r'[0-9]+',  horse_profile.find_all("td")[0].text)
                
                Age = age_calculator(date(int(age_text[0]), int(age_text[1]), int(age_text[2])))

                profile_trs =  horse_profile.find_all("tr")
                for tr in profile_trs:
                    if str(tr).find("通算成績") != -1:
                        a,b,c,d,e = re.findall(r'[0-9]+', tr.find("td").text)[0:5]
                        if(a != '0'):
                            Horse_win_rate = ( int(c) + int(d) + int(e))/int(a)
                        else:
                            Horse_win_rate = 0
                        
                horse_title = soup.find(class_ = "horse_title").find(class_ = "txt_01").text
                gender = re.findall('[牝牡セ]', horse_title)[0]
                if gender == "牝":
                    Gender = 0
                elif gender == "牡":
                    Gender = 1
                else:
                    Gender = 2
       
                print("馬複勝率:{}".format(Horse_win_rate))
                print("年齢:{}".format(Age))
                print("性別:{}".format(Gender))
                for j in range(len(race_results)):
                    tds = race_results[j].find_all("td")
                    if  len(tds[17].text) >= 6:
                        Number = tds[6].text
                        print("頭数:{}".format(Number))
                        race_url = "https://db.netkeiba.com" + tds[4].a.get("href")
                        race_info = get_bs(race_url)
                        Win_prize = race_info.find(class_="race_table_01").find_all("tr")[1].find_all("td")[20].text
                        print("一位賞金:{}".format(Win_prize))
                        jockey_url = "https://db.netkeiba.com/jockey/result/" + tds[12].a.get("href").split("/")[2]
                        try:
                            jockey_info = get_bs(jockey_url).find("table")
                            Jockey_win_ratio = "0" + jockey_info.find_all("tr")[2].find_all("td")[18].text
                        except:
                            Jockey_win_ratio = 0
                        print("騎手複勝率:{}".format(Jockey_win_ratio))
                        Burden = tds[13].text
                        print("Burden:{}".format(Burden))
                        if j > 1:
                            tds_prev =  race_results[j-1].find_all("td")
                            Distance_prev = tds_prev[14].text[1:5]
                            Time_diff_prev = tds_prev[18].text
                            FirstTime = 0
                        else:
                            Distance_prev = None
                            Time_diff_prev = None 
                            FirstTime = 1
                        Distance = tds[14].text[1:5]
                        print("距離:{}".format(Distance))
                        print("前走距離:{}".format(Distance_prev))
                        print("前走着差:{}".format(Time_diff_prev))
                        try:
                            Horse_weight, _Delta_weight = re.findall(r'[0-9\+\-]+', tds[23].text)
                        except:
                            Horse_weight = None
                            Delta_weight = None
                        print("馬重:{}".format(Horse_weight))
                        print("体重増減:{}".format(Delta_weight))
                        Time = ToTotal_time(tds[17].text)
                        print("走破タイム:{}".format(Time))
                        pre_ex = np.array([Horse_win_rate, Age, Gender, Number, Prize, Burden, Distance_prev, Time_diff_prev, Horse_weight, Delta_weight, Jockey_win_rate,  Distance, FirstTime, Time]).reshape(1,14)
                        print(pre_ex)
                        EX_list = np.append(EX_list, pre_ex, axis=0)
            else:
                    print("情報がありません")

    return(EX_list)

def model_update():
    import requests
    from bs4 import BeautifulSoup
    import datetime
    import re
    import numpy as np

    def write_csv(data,path,mode):
        #overwrite mode w
        #append mode a
        with open(path, mode) as f:
            writer = csv.writer(f)
            writer.writerows(data)


    newdata = LearningData_Parse_from(year)

    write_csv(newdata, 'static/data/learning_dataset.csv', 'a')

    Xmean, Xstd = calc_norm_parameters_of(new_learning_csv_data)
    write_csv(Xmean, 'static/data/Xmean.csv', 'w')
    write_csv(Xstd, 'static/data/Xstd.csv', 'w')

    mlp = generate_new_model_from(new_learning_csv_data)

    #Overwrite
    filename = 'static/data/mlp_model.sav'
    pickle.dump(mlp, open(filename, 'wb'))
    

#2/1 https://race.netkeiba.com/race/result.html?race_id=202005010101&rf=race_list
#



