from datetime import datetime 
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class TenMinScrapyPipeline(object):
    _db = None

    @classmethod
    def get_database(cls):
        cls._db = sqlite3.connect(
            os.path.join(BASE_DIR, 'db.sqlite3')
        )
        #見た所、なければ新たに作成すると言うことで、ここに指定したファイルへアクセスしている
        # テーブル作成
        cursor = cls._db.cursor()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS blogs_racelist(\
                id INTEGER PRIMARY KEY AUTOINCREMENT, \
                url TEXT UNIQUE NOT NULL, \
                title TEXT NOT NULL, \
                place TEXT NOT NULL, \
                date DATE NOT NULL \
            );')

        return cls._db

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
        
        db = self.get_database()
        db.execute(
            'INSERT INTO blogs_racelist (title, url, place, date) VALUES (?, ?, ?, ?)', (
                item['title'],
                item['url'],
                item['place'],
                datetime.strptime(item['date'], '%y%m%d')
            )
        )
        db.commit()

    def find_post(self, url):
        db = self.get_database()
        cursor = db.execute(
            'SELECT * FROM blogs_racelist WHERE url=?',
            (url,)
        )
        return cursor.fetchone()