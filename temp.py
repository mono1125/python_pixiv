from pixivpy3 import *
import json
from time import sleep
import os
import numpy as np
import pandas as pd

# フォローユーザのpixiv_idをcsvファイルから取得しidをリストで返す
def follow_user_pixiv_id_lists():
    file_name = input("Type illustrator pixiv_id number list(csv):\n>>>")
    df = pd.read_csv(file_name, encoding='utf-8')
    following_user_id = []
    following_user_id = df['user_id']
    return following_user_id


# ログイン処理
def login():
    api = PixivAPI()
    f = open("client.json", "r")
    client_info = json.load(f)
    f.close()
    api.login(client_info["pixiv_id"], client_info["password"])
    return api


# 入力されたpixiv_idから絵師情報を取得しダウンロード
def getinfo_and_download(user_id):
    api = login()
    json_result = api.users_works(int(user_id), per_page=1000) # とりあえずmax1000作品と定義
    total_works = json_result.pagination.total
    illust = json_result.response[0]

    # ファイル名規則チェック(抵触するものは0で置換)
    illust.user.name = illust.user.name.translate(str.maketrans({'\\': '0', '/': '0', ':': '0', ';': '0', ',': '0', '*': '0', \
                                                    '?': '0', '\"': '0', '<': '0', '>': '0', '|': '0', '.': '0'}))

    # ユーザーネーム＠hogeを除去
    illust.user.name = illust.user.name[0:((illust.user.name + '@').index('@'))] # 半角の@以降を削除
    illust.user.name = illust.user.name[0:((illust.user.name + '＠').index('＠'))]  # 全角の@以降を削除
    # ユーザーネーム(hoge)を除去
    illust.user.name = illust.user.name[0:((illust.user.name + '(').index('('))]  # 半角の(以降を削除
    illust.user.name = illust.user.name[0:((illust.user.name + '（').index('（'))]  # 全角の（以降を削除
    illust.user.name = illust.user.name[0:((illust.user.name + '[').index('['))]  # 半角の[以降を削除
    illust.user.name = illust.user.name[0:((illust.user.name + '「').index('「'))]  # 全角の「以降を削除

    # 文字列がなくなったとき
    if len(illust.user.name) == 0:
        illust.user.name = user_id + '(name_error)'

    if not os.path.exists("./pixiv_images"): # 保存用フォルダがない場合は生成
        os.mkdir("./pixiv_images")
    saving_direcory_path = "./pixiv_images/" + illust.user.name + "/"
    aapi = AppPixivAPI()
    separator = "------------------------------------------------------------"

    # ダウンロード
    print("Artist: %s" % illust.user.name)
    print("Works: %d" % total_works)
    print(separator)
    if not os.path.exists(saving_direcory_path):
        os.mkdir(saving_direcory_path)
    for work_no in range(0, total_works):

        illust = json_result.response[work_no]
        print("Procedure: %d/%d" % (work_no + 1, total_works))
        print("Title: %s" % illust.title)
        print("URL: %s" % illust.image_urls["large"])
        print("Caption: %s" % illust.caption)

        # イラストがすでにダウンロードされている場合
        if os.path.exists(saving_direcory_path + str(illust.id) + "_p0.png") or os.path.exists(
                saving_direcory_path + str(illust.id) + "_p0.jpg"):
            print("Title:" + str(illust.title) + " has already downloaded.")
            print(separator)
            sleep(2)

            continue

        # 漫画の場合
        if illust.is_manga:
            work_info = api.works(illust.id)
            for page_no in range(0, work_info.response[0].page_count):
                page_info = work_info.response[0].metadata.pages[page_no]
                aapi.download(page_info.image_urls.large, saving_direcory_path)
                sleep(3)
        # イラストの場合
        else:
            aapi.download(illust.image_urls.large, saving_direcory_path)
            sleep(3)
        print(separator)


user_id_list = follow_user_pixiv_id_lists()

for i in user_id_list:
    getinfo_and_download(i)
    sleep(4)

print("\nThat\'s all.")