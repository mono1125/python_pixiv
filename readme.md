# 任意のPixivユーザのイラストや漫画をダウンロードするソフトです。
1ユーザ毎にログインする仕様になっています。（ダウンロードが中断されないように）

そのため、複数のユーザのイラストや漫画をダウンロードするときは、予めPixivのログイン通知が行くメールアドレスの変更などを行っておくと良いでしょう。

## 使い方
Anaconda3で環境構築を行います。
### 環境など
```
$ git clone https://...

# anaconda環境
$ conda create -n mypixiv

# requests.txtをインストール
$ pip install -r requests.txt
```

### 各種必要なファイルの作成
ログイン情報を収納するための`client.json`ファイルとダウンロードしたいPixivユーザのIDを格納した`artist.csv`ファイルを作成します。

client.json
```client.json
{
  "pixiv_id":"hogehoge",
  "password":"hogehoge",
  "user_id":"12345678"
}
```

artist.csv
```artist.csv
user_id, name
<ダウンロードしたいユーザーのid>, ペンネーム
.
.
.
.
```
## 実行

```
$ conda activate mypixiv
$ python temp.py
> Type illustrator pixiv_id number list(csv):
>>> artist.csv

# 順次ダウンロードされる
```
