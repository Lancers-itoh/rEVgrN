from datetime import datetime 
import os
import sqlite3
import psycopg2
import re

try:
    database_url = os.environ['DATABASE_URL']
except KeyError:
    from .local_database_url import *
regex = re.compile('\d+')
    
print(database_url)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TenMinScrapyPipeline(object):
    _db = None
    @classmethod
    def get_database(cls):
        #cls._db = sqlite3.connect(
        #    os.path.join(BASE_DIR, 'db.sqlite3')
        #)
        connection = psycopg2.connect(database_url)
        #見た所、なければ新たに作成すると言うことで、ここに指定したファイルへアクセスしている
        cursor = connection.cursor()
        print("CURSOR!!!")
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS blogs_racelist(\
                id SERIAL PRIMARY KEY, \
                url TEXT UNIQUE NOT NULL, \
                title TEXT NOT NULL, \
                place TEXT NOT NULL, \
                date DATE NOT NULL, \
                race_num INTEGER NOT NULL, \
                racedata_updated_at DATE NOT NULL \
            );')

        return cursor

    def process_item(self, item, spider):
        """
        Pipeline にデータが渡される時に実行される
        item に spider から渡された item がセットされる
        """
        self.save_post(item)
        return item

    def save_post(self, item):
        """
        item を DB に保存する
        """
        if self.find_post(item['url']):
            # 既に同じURLのデータが存在する場合はスキップ
            return
        elif item['url'].find("shutuba") != -1:
            result_url = 'https://race.netkeiba.com/race/result.html?race_id=' + regex.findall(item['url'])[0] + "&rf=race_list"
            if self.find_post(result_url):
                # 既に同じレースのresult URLが存在する場合はスキップ
                return
        elif item['url'].find("result") != -1:
            #result url の場合は、shutuba url を消す
            shutuba_url = 'https://race.netkeiba.com/race/shutuba.html?race_id=' + regex.findall(item['url'])[0] + "&rf=race_list"
            print(shutuba_url)
            if self.find_post(shutuba_url):
                sentence = "DELETE FROM blogs_racelist WHERE url ='" + shutuba_url + "';"
                print(sentence)
                with psycopg2.connect(database_url) as conn:
                    with conn.cursor() as cur:
                        cur.execute(sentence)
                    conn.commit()

                #self.find_post(shutuba_url).delete()
        
        print(item['racedata_updated_at'])
        sentence = "INSERT INTO blogs_racelist (title, url, place, date, race_num, racedata_updated_at) VALUES " + "('" +  item['title'] + "', '" +  item['url'] + "', '" +  item['place'] + "', '" +  item['date'] + "', '" + item['race_num'] + "','" + item['racedata_updated_at'] + "');"
        print(sentence) 

        with psycopg2.connect(database_url) as conn:
            with conn.cursor() as cur:
                cur.execute(sentence)
            conn.commit()

    def find_post(self, url):
        db = self.get_database()
        sentence = "SELECT * FROM blogs_racelist WHERE url = " + "'" + url + "'" + ";"
        print(sentence)
        cursor = db.execute(
            sentence
        )
        return db.fetchone()