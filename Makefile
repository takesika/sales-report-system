# 営業日報システム Makefile
# Cloud Run デプロイ用

# ==============================================================================
# 変数定義
# ==============================================================================
PROJECT_ID := gen-lang-client-0887846013
REGION := asia-northeast1

# サービス名
FRONTEND_SERVICE := sales-report-frontend
BACKEND_SERVICE := sales-report-backend

# イメージ名
FRONTEND_IMAGE := $(REGION)-docker.pkg.dev/$(PROJECT_ID)/sales-report/frontend
BACKEND_IMAGE := $(REGION)-docker.pkg.dev/$(PROJECT_ID)/sales-report/backend

# ==============================================================================
# ローカル開発
# ==============================================================================
.PHONY: dev dev-frontend dev-backend
dev: dev-frontend dev-backend

dev-frontend:
	cd frontend && npm run dev

dev-backend:
	cd backend && uv run uvicorn src.main:app --reload

# ==============================================================================
# Lint & Test
# ==============================================================================
.PHONY: lint lint-frontend lint-backend test test-frontend test-backend
lint: lint-frontend lint-backend

lint-frontend:
	cd frontend && npm run lint

lint-backend:
	cd backend && uv run ruff check . && uv run ruff format --check .

test: test-frontend test-backend

test-frontend:
	cd frontend && npm run test:run

test-backend:
	cd backend && uv run pytest -v

# ==============================================================================
# Docker ビルド（ローカル）
# ==============================================================================
.PHONY: docker-build docker-build-frontend docker-build-backend
docker-build: docker-build-frontend docker-build-backend

docker-build-frontend:
	docker build -t $(FRONTEND_SERVICE):local -f frontend/Dockerfile frontend

docker-build-backend:
	docker build -t $(BACKEND_SERVICE):local -f backend/Dockerfile backend

# ==============================================================================
# Docker 実行（ローカル）
# ==============================================================================
.PHONY: docker-run-frontend docker-run-backend
docker-run-frontend:
	docker run -p 3000:8080 $(FRONTEND_SERVICE):local

docker-run-backend:
	docker run -p 8000:8080 $(BACKEND_SERVICE):local

# ==============================================================================
# GCP 認証 & セットアップ
# ==============================================================================
.PHONY: gcp-auth gcp-setup
gcp-auth:
	gcloud auth login
	gcloud auth configure-docker $(REGION)-docker.pkg.dev

gcp-setup:
	gcloud config set project $(PROJECT_ID)
	gcloud services enable run.googleapis.com
	gcloud services enable artifactregistry.googleapis.com
	gcloud artifacts repositories create sales-report \
		--repository-format=docker \
		--location=$(REGION) \
		--description="Sales Report System Docker Repository" || true

# ==============================================================================
# Cloud Run デプロイ
# ==============================================================================
.PHONY: deploy deploy-frontend deploy-backend

# フロントエンドデプロイ
deploy-frontend: build-push-frontend
	gcloud run deploy $(FRONTEND_SERVICE) \
		--image $(FRONTEND_IMAGE):latest \
		--platform managed \
		--region $(REGION) \
		--allow-unauthenticated \
		--port 8080 \
		--memory 512Mi \
		--cpu 1 \
		--min-instances 0 \
		--max-instances 10

# バックエンドデプロイ
deploy-backend: build-push-backend
	gcloud run deploy $(BACKEND_SERVICE) \
		--image $(BACKEND_IMAGE):latest \
		--platform managed \
		--region $(REGION) \
		--allow-unauthenticated \
		--port 8080 \
		--memory 512Mi \
		--cpu 1 \
		--min-instances 0 \
		--max-instances 10

# 両方デプロイ
deploy: deploy-frontend deploy-backend

# ==============================================================================
# Cloud Build & Push
# ==============================================================================
.PHONY: build-push-frontend build-push-backend

build-push-frontend:
	docker build -t $(FRONTEND_IMAGE):latest -f frontend/Dockerfile frontend
	docker push $(FRONTEND_IMAGE):latest

build-push-backend:
	docker build -t $(BACKEND_IMAGE):latest -f backend/Dockerfile backend
	docker push $(BACKEND_IMAGE):latest

# ==============================================================================
# Cloud Build（リモートビルド）
# ==============================================================================
.PHONY: cloud-build-frontend cloud-build-backend

cloud-build-frontend:
	gcloud builds submit frontend \
		--tag $(FRONTEND_IMAGE):latest \
		--project $(PROJECT_ID)

cloud-build-backend:
	gcloud builds submit backend \
		--tag $(BACKEND_IMAGE):latest \
		--project $(PROJECT_ID)

# ==============================================================================
# クリーンアップ
# ==============================================================================
.PHONY: clean
clean:
	rm -rf frontend/.next frontend/node_modules
	rm -rf backend/.venv backend/__pycache__
	docker system prune -f

# ==============================================================================
# ヘルプ
# ==============================================================================
.PHONY: help
help:
	@echo "営業日報システム Makefile"
	@echo ""
	@echo "ローカル開発:"
	@echo "  make dev              - フロントエンド・バックエンド両方起動"
	@echo "  make dev-frontend     - フロントエンドのみ起動"
	@echo "  make dev-backend      - バックエンドのみ起動"
	@echo ""
	@echo "Lint & Test:"
	@echo "  make lint             - 全てのLint実行"
	@echo "  make test             - 全てのテスト実行"
	@echo ""
	@echo "Docker（ローカル）:"
	@echo "  make docker-build     - Dockerイメージビルド"
	@echo "  make docker-run-frontend  - フロントエンドコンテナ起動"
	@echo "  make docker-run-backend   - バックエンドコンテナ起動"
	@echo ""
	@echo "GCP:"
	@echo "  make gcp-auth         - GCP認証"
	@echo "  make gcp-setup        - GCPプロジェクト設定"
	@echo ""
	@echo "デプロイ:"
	@echo "  make deploy           - 全てデプロイ"
	@echo "  make deploy-frontend  - フロントエンドのみデプロイ"
	@echo "  make deploy-backend   - バックエンドのみデプロイ"
