# Odoo 17 (最新版) + 開発ツール
# 注意: 執筆時点でOdoo 19はリリースされていないため、最新版17を使用
# 19.0がリリースされたらFROMを変更してください

FROM odoo:17.0

USER root

# 開発ツールのインストール
RUN apt-get update && apt-get install -y \
    git \
    vim \
    nano \
    curl \
    wget \
    iputils-ping \
    net-tools \
    postgresql-client \
    python3-pip \
    python3-venv \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# GitHub CLI (gh) のインストール
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
    && chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    && apt-get update \
    && apt-get install -y gh \
    && rm -rf /var/lib/apt/lists/*

# Pre-commitのインストール
RUN pip3 install pre-commit

# Odoo開発用の追加Pythonパッケージ
RUN pip3 install \
    debugpy \
    pylint-odoo \
    flake8 \
    black \
    isort \
    pytest

# 作業ディレクトリの作成
RUN mkdir -p /mnt/extra-addons /workspace

USER odoo

# Odoo設定ファイルのコピー
COPY ./config/odoo.conf /etc/odoo/odoo.conf

EXPOSE 8069 8071 8072

CMD ["odoo"]
