from mutagen import File
import os

root_path = u"E:\\music\\V collection 11 -NT-\\V collection 12 -REMIX-\\deploy"


def deal_file_name(path):
    is_star = 2
    for item in os.listdir(path):
        current_path = os.path.join(path, item)
        if item.lower().endswith(".mp3"):
            afile = File(current_path)
            trckNum = int(afile.tags.get("TRCK").text[0])
            resNum = ""
            title = None
            artist = None
            if trckNum < 10:
                resNum = "0" + str(trckNum)
            else:
                resNum = str(trckNum)

            try:
                title = afile.tags.get("TIT2").text[0]
            except AttributeError:
                print('标题输入不全')
            try:
                artist = afile.tags.get("TPE1").text[0].replace("/", " ")
            except AttributeError:
                print('请确保全部输入作者名')
                exit()
            if is_star > 0:
                newFileName = resNum + "." + "【☆】" + title + " - " + artist + ".mp3"
            else:
                newFileName = resNum + "." + title + " - " + artist + ".mp3"
            newFileName = newFileName.replace("*", "").replace(":", " ")
            is_star = is_star - 1
            os.rename(current_path, os.path.join(path, newFileName))

        if os.path.isdir(current_path):
            deal_file_name(current_path)


deal_file_name(root_path)