# ベースイメージを指定
FROM python:3.9.11

# Pythonの出力を即時にする環境変数を設定
ENV PYTHONUNBUFFERED 1

# 作業ディレクトリを作成
RUN mkdir -p /root/workspace

# requirements.txtを作業ディレクトリにコピー
COPY requirements.txt /root/workspace/

# 作業ディレクトリを設定
WORKDIR /root/workspace

# パッケージをインストール
RUN pip3 install --upgrade pip\
    && pip3 install --upgrade setuptools\
    && pip3 install -r requirements.txt\
    && pip3 install django

# コンテナのデフォルトコマンド
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]


# 参考にした記事：https://qiita.com/a-im12/items/7f3c8d1212dac3685e77