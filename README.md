# site_analizer
# 概要
ウェブサイトを捜査してごちゃごちゃ遊ぶときに便利なライブラリを作った。

ネットから HTML ソースを取ってきたり、
取ってきた HTML ソースからデータをいろいろスクレイピングしたり、
ファイルをダウンロードしてきたり...

それをする上で便利な、
ファイルやディレクトリを作ったり、
文字列を操作したり、
ファイルの種類を特定したり...

とにかく、いろいろウェブスクレイピングをするプログラムを作ってきて、共通化できる処理をまとめたライブラリになっている。

まだまだアップデートする余地はあるし、アップデートしていく。

# 使い方
1. 任意の場所にこのリポジトリをクローン
    ```
    cd ~/lib
    git clone https://github.com/yazawakenichi/site_analizer
    ```
    説明の都合上ここでは `~/lib` とする
2. `site_analizer/lib` を PTH ファイルに追加する
    1. PTH ファイルの場所を確認する
        ```
        python3
        >>> import site
        >>> site.getsitepackages()
        ['/usr/local/lib/python3.8/site-packages']
        ```
        説明の都合上ここでは PTH ファイルの場所を `/usr/local/lib/python3.8/site-packages` とする
    2. ファイルを追加し、追加したいパスを記述する
        ```
        vim /usr/local/lib/python3.8/site-packages/site_analizer.pth
        ```
        `site_analizer.pth`
        ```
        /home/user/lib/site_analizer/lib
        ```
3. Python スクリプト上で import する
    ```
    import FDEditor
    import PathEditor
    import SoupMaster
    import StringEditor
    ```

# 参考サイト
- [requests モジュールでダウンロードに失敗するときの対策方法 - GAMMASOFT](https://gammasoft.jp/support/solutions-of-requests-get-failed/)
- [【 初心者向け 】 Python os.path.basename() とは？ - AI Academy Media](https://aiacademy.jp/media/?p=1584)
- [[Python] 別ディレクトリの自作モジュールを import](https://fuji-pocketbook.net/another-dir-module/)
- [【Python】 urllib.error.HTTPError の解決方法](https://self-development.info/%E3%80%90python%E3%80%91urllib-error-httperror%E3%81%AE%E8%A7%A3%E6%B1%BA%E6%96%B9%E6%B3%95/)