# ビルドステージ
FROM python:3.12-slim AS builder

WORKDIR /app

# uvのインストール
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# 依存関係のインストール
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# 本番ステージ
FROM python:3.12-slim AS runner

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# 非rootユーザーで実行
RUN useradd --create-home --shell /bin/bash appuser

# 仮想環境と依存関係のコピー
COPY --from=builder /app/.venv /app/.venv

# ソースコードのコピー
COPY src ./src

# パスの設定
ENV PATH="/app/.venv/bin:$PATH"

USER appuser

EXPOSE 8080

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
