from mutagen import File
import os
import math

root_path = u'D:\\nginx\\html\\lib'

def deal_mp3(root_path):
    names = os.listdir(root_path)
    for name in names:
        path = os.path.join(root_path, name)
        if os.path.isdir(path):
            deal_mp3(path)
        if path.endswith('.aac'):
            afile = File(path)
            try:
                title = afile.tags.get("TIT2").text[0]
                os.rename(path, os.path.join(os.path.dirname(path), title + '.mp3'))
            except AttributeError:
                print(path + " 标题输入不全")
                exit()


deal_mp3(root_path)