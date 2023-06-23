# site_analizer
# 概要
自分がよく使う処理をまとめたライブラリ

できることはざっくり以下のような感じ

- スクレイピング
- ダウンロード
- コンテンツの保存・表示・加工

# 動作環境
- 
- 

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

詳しいリファレンスは [lib/README.md](https://github.com/yazawakenichi/site_analizer/tree/main/lib) 参照

# 参考サイト
- [requests モジュールでダウンロードに失敗するときの対策方法 - GAMMASOFT](https://gammasoft.jp/support/solutions-of-requests-get-failed/)
- [【 初心者向け 】 Python os.path.basename() とは？ - AI Academy Media](https://aiacademy.jp/media/?p=1584)
- [[Python] 別ディレクトリの自作モジュールを import](https://fuji-pocketbook.net/another-dir-module/)
- [【Python】 urllib.error.HTTPError の解決方法](https://self-development.info/%E3%80%90python%E3%80%91urllib-error-httperror%E3%81%AE%E8%A7%A3%E6%B1%BA%E6%96%B9%E6%B3%95/)
