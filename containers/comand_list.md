ビルドコマンド
### docker-compose build

コンテナの構築・起動コマンド（-dオプションを付けてバックグランドで実行）ログが出力される
### docker-compose up

コンテナの停止、削除を実行
### docker-compose down

キャッシュを使わずにビルド（Dockerfileを更新したなどの理由でキャッシュを使いたくない場合）
### docker-compose build --no-cache

既存のコンテナを起動（ログが出力されない）
### docker-compose start <サービス名>

コンテナを停止
### docker-compose stop <サービス名>

imageの構築から、コンテナの構築・起動
### docker-compose run <サービス名>

dockerの仮想環境に入るコマンド（サービスのコンテナ内でコマンドを実行）
### docker exec -it <container_name> /bin/bash

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

データベースの構築間違えたら（手順）
https://hk-software.hatenablog.com/entry/2022/12/25/194032

1.sqlite3の更新とインストール
### apt-get update
### apt-get install -y sqlite3

2.SQLiteデータベースに接続
### sqlite3 db.sqlite3

3.既存のテーブルを削除
### DROP TABLE IF EXISTS django_migrations;
### DROP TABLE IF EXISTS django_content_type;
### DROP TABLE IF EXISTS auth_permission;
### これ以降もある。一つずづ削除していく（コマンドは一括入力可能）

4.SQLiteから退出
### .exit
### python3 manage.py showmigrationsで確認する

5.マイグレーションのレセット
### python3 manage.py migrate モデル名 zero

6.データベースのリセットとマイグレート
### rm db.sqlite3
### python3 manage.py migrate

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━