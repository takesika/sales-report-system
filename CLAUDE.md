# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

営業日報システム - 営業担当者が日々の顧客訪問活動を報告し、上長がコメント・フィードバックを行うためのシステム。

## 設計ドキュメント

実装時は必ず以下のドキュメントを参照すること：

- @docs/er-diagram.md - ER図・テーブル定義書（DDL含む）
- @docs/screen-definition.md - 画面定義書（10画面）
- @docs/api-specification.md - API仕様書（REST API、JWT認証）
- @docs/test-specification.md - テスト仕様書

### 参照ガイド

| 作業内容 | 参照ドキュメント |
|---------|----------------|
| DB設計・マイグレーション作成 | @docs/er-diagram.md |
| API実装 | @docs/api-specification.md |
| フロントエンド実装 | @docs/screen-definition.md |
| テスト作成 | @docs/test-specification.md |

## データモデル

5つのテーブルで構成：

- `SALESPERSON` - 営業担当者マスタ（上長は自己参照で表現）
- `CUSTOMER` - 顧客マスタ
- `DAILY_REPORT` - 日報（担当者×日付でユニーク）
- `VISIT_RECORD` - 訪問記録（日報に複数紐付け）
- `REPORT_COMMENT` - 日報コメント

## API設計方針

- ベースURL: `/api/v1`
- 認証: Bearer Token (JWT)
- 日報ステータス: `draft` → `submitted` → `confirmed`

## 権限モデル

3種類のロール：
- 一般営業: 自分の日報のみ操作可能
- 上長: 部下の日報閲覧・確認済み更新・顧客マスタ編集可能
- 管理者: 全機能にアクセス可能

## 技術スタック

### フロントエンド (`frontend/`)
- Next.js 14 (App Router) + TypeScript
- ESLint 9 (Flat Config)

### バックエンド (`backend/`)
- Python + FastAPI
- MySQL

## コマンド

### フロントエンド
```bash
cd frontend
npm install          # 依存関係インストール
npm run dev          # 開発サーバー起動
npm run lint         # ESLint実行
npm run lint:fix     # ESLint自動修正
npm run type-check   # TypeScript型チェック
npm run build        # ビルド
```

### バックエンド
```bash
cd backend
uv sync              # 依存関係インストール
uv run uvicorn src.main:app --reload  # 開発サーバー起動
uv run ruff check    # Linter実行
uv run ruff format   # フォーマット
uv run pytest        # テスト実行
```

### Makefile（デプロイ）
```bash
make help            # コマンド一覧
make dev             # ローカル開発サーバー起動
make lint            # 全Lint実行
make test            # 全テスト実行
make deploy          # Cloud Runにデプロイ
make deploy-frontend # フロントエンドのみデプロイ
make deploy-backend  # バックエンドのみデプロイ
```

## CI/CD

- **CI**: `.github/workflows/ci.yml` - PR/push時にLint・テスト・ビルド
- **CD**: `.github/workflows/cd.yml` - main pushで変更のあるサービスのみCloud Runにデプロイ
- **プロジェクトID**: `gen-lang-client-0887846013`
- **リージョン**: `asia-northeast1`

## 言語

日本語でやりとりしてください。コメントやドキュメントも日本語で記述します。
