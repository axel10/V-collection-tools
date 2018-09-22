import os
from pathlib import Path
from mutagen import File
from mutagen.mp4 import MP4
from PIL import Image
from io import BytesIO
import math
import json
import sqlite3

conn = sqlite3.connect("E:\music\V collection 11 -NT-\\vc.db")
cur = conn.cursor()


def get_dirs(path):
    return _get_dirs(path, '', path)


def get_mp3_title(path):
    if path.lower().endswith('mp3'):
        afile = File(path)
        return afile.tags.get("TIT2").text[0]
    else:
        afile = MP4(path)
        return afile.tags.get("©nam")[0]


def get_id(db_path):
    cur.execute('select id from items WHERE Path=?', [db_path])
    # if cur.rowcount != -1:
    res = cur.fetchone()
    if res is not None:
        return res[0]
    else:
        cur.execute("insert into items (Path) values (?);", [db_path])
        return cur.lastrowid


def _get_dirs(path, parents, root_path):
    content = []
    paths = os.listdir(path)
    for item in paths:
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            sort, name = item.split('.')
            db_path = os.path.join(parents, item)
            id = get_id(db_path)

            content.append(
                {'title': name,
                 'content': _get_dirs(item_path, os.path.join(parents, name), root_path),
                 'sort': int(sort),
                 'id': id
                 })
        else:
            if item.lower().endswith('.mp3') or item.lower().endswith('.m4a'):
                content.append(deal_mp3(item_path, parents, root_path))

    return content


def deal_mp3(file_path, parents, root_path):
    title = artist = trck = ""
    cd_title = ""
    id = None
    year = None
    time = None
    artwork = ""

    cd_cover_dir = os.path.join(os.path.dirname(root_path), '封面', parents)
    if not os.path.exists(cd_cover_dir):
        os.makedirs(cd_cover_dir)

    if file_path.lower().endswith('.mp3'):
        afile = File(file_path)

        try:
            title = afile.tags.get("TIT2").text[0]
            db_path = os.path.join(parents, title)
            id = get_id(db_path)

        except AttributeError:
            print(file_path + " 标题输入不全")
            exit()
        try:
            artist = afile.tags.get("TPE1").text[0]
        except AttributeError:
            print(file_path + " 艺术家输入不全")
            exit()
        try:
            trck = int(afile.tags.get("TRCK").text[0])
        except AttributeError:
            trck = 0
            # print(item_path + " 序号输入不全")
            # exit()

        try:
            cd_title = afile.tags.get("TALB").text[0]
        except AttributeError:
            print(file_path + " 专辑名输入不全")
            exit()

        second = int(afile.info.length)
        min = math.floor(second / 60)
        sec = math.floor(second % 60)

        if sec < 10:
            sec = '0' + str(sec)

        time = str(min) + ':' + str(sec)
        try:
            artwork = afile.tags['APIC:'].data
        except KeyError:
            print(file_path + " 封面不全")
            exit()

    else:
        afile = MP4(file_path)

        try:
            title = afile.tags.get("©nam")[0]
            db_path = os.path.join(parents, title)
            id = get_id(db_path)
        except AttributeError:
            print(file_path + " 标题输入不全")
            exit()
        try:
            artist = afile.tags.get("©ART")[0]
        except AttributeError:
            print(file_path + " 艺术家输入不全")
            exit()
        try:
            trck = int(afile.tags.get("trkn")[0][0])
        except AttributeError:
            # trck = 0
            print(file_path + " 序号输入不全")
            exit()

        try:
            cd_title = afile.tags.get("©alb")[0]
        except AttributeError:
            print(file_path + " 专辑名输入不全")
            exit()

        second = int(afile.info.length)
        min = math.floor(second / 60)
        sec = math.floor(second % 60)

        if sec < 10:
            sec = '0' + str(sec)

        time = str(min) + ':' + str(sec)

        try:
            artwork = afile.tags['covr'][0]
        except KeyError:
            tmp = MP4(file_path)

            print(file_path + " 封面不全")
            exit()

    # try:
    #     year = afile.tags.get("TDRC").text[0].year
    # except AttributeError:
    #     year = None

    obj = dict(title=title, p=artist, sort=trck, cd_title=cd_title, id=id, time=time)

    # 开始提取封面

    img = Image.open(BytesIO(artwork))
    img = img.convert("RGB")
    w, h = img.size
    rate = 300 / w
    width = w * rate
    height = h * rate
    img = img.resize((int(width), int(height)), Image.ANTIALIAS)
    cover_path = os.path.join(cd_cover_dir, title + ".jpg")
    # with open(cover_path, "wb+") as cover:
    #     cover.write(artwork)
    img.save(cover_path, optimize=True, quality=90)

    return obj


root_path = u'E:\music\V collection 11 -NT-\lib'

res = get_dirs(u'E:\music\V collection 11 -NT-\lib')
with open(os.path.join(Path(root_path).resolve().parent, "result.json"), "w+", encoding='utf-8') as json_file:
    json_file.write(json.dumps(res, ensure_ascii=False))

# cur.execute("select id from items where Path=?", [u'10.V 1collection EX【UC】'])
# print(cur.fetchone())

conn.commit()
