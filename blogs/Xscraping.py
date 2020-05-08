
def Parse_from(race_url):
    import requests
    from bs4 import BeautifulSoup
    import datetime
    import re
    import numpy as np
    from blogs.models import Racelist, Racedata

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


    DataList = np.empty((1,13))
    soup = get_bs(race_url)
    ## Universal data in this race
    string_distance = soup.find(class_ = "RaceData01").span.text
    Distance = re.sub("\\D", "", string_distance)
    RaceData02_spans = soup.find(class_ = "RaceData02").find_all("span")
    Number = re.sub("\\D", "", RaceData02_spans[7].text)
    Prize = RaceData02_spans[8].text.split(":")[1].split(",")[0]
    ## Each horse data 
    table = soup.find("table").tbody
    
    table_trs = table.find_all("tr")
    for row in table_trs:  
        horse_info = row.find(class_ = "Detail_Left").text
        if horse_info.find("牡") == -1:
            #"牝"
            Gender = 0
        else:
            Gender = 1
                #"牡"
        Age = re.sub("\\D", "", horse_info)
        Burden = row.find(class_ = "JockeyWeight").text

        Jockey_code = re.sub("\\D", "", row.find(class_ = "Jockey").a.get("href"))
        Jockey_win_rate = JC_WinRateOf(Jockey_code)

        weight_data_set = row.find(class_ = "Weight").text.split("(")
        Weight = weight_data_set[0]
        Delta_weight = weight_data_set[1].rstrip(")")
        horse_name = row.find(class_ = "Horse_Name")
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
            FirstTime = 0
        
        
        pre_ex = np.array([Horse_win_rate, Age, Gender, Number, Prize, Burden, Distance_prev, Time_diff_prev, Weight, Delta_weight, Jockey_win_rate,  Distance, FirstTime]).reshape(1,13)
        DataList = np.append( DataList, pre_ex, axis=0)
        DataList = np.delete(DataList,0,0)
        give_data = DataList.astype('float64')   
            #header = 
        print("Processing...")

    return(give_data)

def normalization(values_as_nparr, XmeanCsvPath, XstdCsvPath):
    import csv
    import numpy as np
    with open(XmeanCsvPath) as f:
        reader = csv.reader(f)
        Xmean = [row for row in reader]
    Xmean = np.array(Xmean).astype('float64')
    
    with open(XstdCsvPath) as f:
        reader = csv.reader(f)
        Xstd = [row for row in reader]
    Xstd = np.array(Xstd).astype('float64')

    EX = list(range(len(values_as_nparr)))
    for col in [0,3,4,5,6,7,8,9,10,11]:
        z_score = (values_as_nparr[col] - Xmean[0,col])/Xstd[0,col]
        EX[col] = z_score
    EX[1] = values_as_nparr[1]
    EX[2] = values_as_nparr[2]
    EX[12] = values_as_nparr[12]

    return(EX)

def Predict_from_these(given_data, ModelPath, Ymean, Ystd):
    import pickle
    import numpy as np
    from sklearn.neural_network import MLPRegressor
    loaded_model = pickle.load(open(ModelPath, 'rb'))
    EX = np.array(given_data).reshape(1,13)
    Predicted_data = loaded_model.predict(EX)
    return(Predicted_data*Ystd + Ymean)



 