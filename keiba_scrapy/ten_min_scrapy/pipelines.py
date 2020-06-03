from datetime import datetime 
import os
import sqlite3
import psycopg2

try:
    database_url = os.environ['DATABASE_URL']
except KeyError:
    from .local_database_url import *
    
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
                date DATE NOT NULL \
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
        
        sentence = "INSERT INTO blogs_racelist (title, url, place, date) VALUES " + "('" +  item['title'] + "', '" +  item['url'] + "', '" +  item['place'] + "', '" +  item['date'] + "');"
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