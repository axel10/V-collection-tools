import sqlite3
import os
from mutagen.mp4 import MP4
from mutagen import File
import configparser

config = configparser.ConfigParser()
config.read('./config.ini')
root_path = config['path']['root']

conn = sqlite3.connect(config['path']['db'])
cur = conn.cursor()


def get_mp3_title(path):
    if path.lower().endswith('mp3'):
        afile = File(path)
        return afile.tags.get("TIT2").text[0]
    else:
        afile = MP4(path)
        return afile.tags.get("©nam")[0]


def _get_path(path, current_path):
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path):
            title = get_mp3_title(item_path)
            db_path = os.path.join(current_path, title)
            cur.execute('select Id from items where Path=?', [db_path])
            if cur.rowcount == -1:
                cur.execute("insert into items (Path) values (?);", [db_path])
        if os.path.isdir(item_path):
            db_path = os.path.join(current_path, item)
            cur.execute('select Id from items where Path=?', [db_path])
            if cur.rowcount == -1:
                cur.execute("insert into items (Path) values (?);", [db_path])
            _get_path(item_path, os.path.join(current_path, item))


def get_path(path):
    _get_path(path, '')


# get_path(root_path)
cur.execute("select id from items WHERE Path='1.V collection 1【Leader】\【★】Cantarella'")
print(cur.fetchone()[0])
conn.commit()
