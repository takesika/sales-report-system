# 営業日報システム API仕様書

## 1. 概要

### 1.1 基本情報
| 項目 | 内容 |
|------|------|
| ベースURL | `/api/v1` |
| 認証方式 | Bearer Token (JWT) |
| データ形式 | JSON |
| 文字コード | UTF-8 |

### 1.2 共通ヘッダー

**リクエストヘッダー**
```
Content-Type: application/json
Authorization: Bearer {access_token}
```

**レスポンスヘッダー**
```
Content-Type: application/json
```

### 1.3 共通レスポンス形式

**成功時**
```json
{
  "success": true,
  "data": { ... }
}
```

**エラー時**
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "エラーメッセージ"
  }
}
```

### 1.4 共通エラーコード

| HTTPステータス | エラーコード | 説明 |
|---------------|-------------|------|
| 400 | BAD_REQUEST | リクエストパラメータ不正 |
| 401 | UNAUTHORIZED | 認証エラー |
| 403 | FORBIDDEN | 権限エラー |
| 404 | NOT_FOUND | リソースが見つからない |
| 409 | CONFLICT | 競合エラー（重複など） |
| 422 | VALIDATION_ERROR | バリデーションエラー |
| 500 | INTERNAL_SERVER_ERROR | サーバー内部エラー |

### 1.5 ページネーション

**リクエストパラメータ**
| パラメータ | 型 | 必須 | デフォルト | 説明 |
|-----------|-----|------|-----------|------|
| page | integer | - | 1 | ページ番号 |
| per_page | integer | - | 20 | 1ページあたりの件数（最大100） |

**レスポンス**
```json
{
  "success": true,
  "data": {
    "items": [ ... ],
    "pagination": {
      "current_page": 1,
      "per_page": 20,
      "total_count": 100,
      "total_pages": 5
    }
  }
}
```

---

## 2. API一覧

| カテゴリ | メソッド | エンドポイント | 説明 |
|---------|---------|----------------|------|
| 認証 | POST | /auth/login | ログイン |
| 認証 | POST | /auth/logout | ログアウト |
| 認証 | GET | /auth/me | ログインユーザー情報取得 |
| 日報 | GET | /reports | 日報一覧取得 |
| 日報 | POST | /reports | 日報作成 |
| 日報 | GET | /reports/{id} | 日報詳細取得 |
| 日報 | PUT | /reports/{id} | 日報更新 |
| 日報 | DELETE | /reports/{id} | 日報削除 |
| 日報 | PUT | /reports/{id}/submit | 日報提出 |
| 日報 | PUT | /reports/{id}/confirm | 日報確認済み |
| コメント | GET | /reports/{id}/comments | コメント一覧取得 |
| コメント | POST | /reports/{id}/comments | コメント投稿 |
| 顧客 | GET | /customers | 顧客一覧取得 |
| 顧客 | POST | /customers | 顧客登録 |
| 顧客 | GET | /customers/{id} | 顧客詳細取得 |
| 顧客 | PUT | /customers/{id} | 顧客更新 |
| 顧客 | DELETE | /customers/{id} | 顧客削除（論理削除） |
| 営業担当者 | GET | /salespersons | 営業担当者一覧取得 |
| 営業担当者 | POST | /salespersons | 営業担当者登録 |
| 営業担当者 | GET | /salespersons/{id} | 営業担当者詳細取得 |
| 営業担当者 | PUT | /salespersons/{id} | 営業担当者更新 |
| 営業担当者 | DELETE | /salespersons/{id} | 営業担当者削除（論理削除） |
| ダッシュボード | GET | /dashboard | ダッシュボード情報取得 |

---

## 3. 認証 API

### 3.1 POST /auth/login
ログイン認証を行い、アクセストークンを発行する

**リクエスト**
```json
{
  "email": "yamada@example.com",
  "password": "password123"
}
```

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| email | string | ○ | メールアドレス |
| password | string | ○ | パスワード |

**レスポンス（成功）**
```json
{
  "success": true,
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "Bearer",
    "expires_in": 86400,
    "user": {
      "salesperson_id": 1,
      "name": "山田太郎",
      "email": "yamada@example.com",
      "is_manager": false
    }
  }
}
```

**エラーレスポンス**
| コード | 説明 |
|--------|------|
| 401 | メールアドレスまたはパスワードが不正 |

---

### 3.2 POST /auth/logout
ログアウト処理を行う

**リクエスト**
なし

**レスポンス（成功）**
```json
{
  "success": true,
  "data": {
    "message": "ログアウトしました"
  }
}
```

---

### 3.3 GET /auth/me
ログイン中のユーザー情報を取得する

**リクエスト**
なし

**レスポンス（成功）**
```json
{
  "success": true,
  "data": {
    "salesperson_id": 1,
    "name": "山田太郎",
    "email": "yamada@example.com",
    "manager_id": 10,
    "manager_name": "佐藤課長",
    "is_manager": false,
    "is_admin": false
  }
}
```

---

## 4. 日報 API

### 4.1 GET /reports
日報一覧を取得する

**クエリパラメータ**
| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| date_from | string (YYYY-MM-DD) | - | 検索開始日 |
| date_to | string (YYYY-MM-DD) | - | 検索終了日 |
| salesperson_id | integer | - | 営業担当者ID（上長のみ指定可能） |
| status | string | - | ステータス（draft/submitted/confirmed） |
| page | integer | - | ページ番号 |
| per_page | integer | - | 1ページあたり件数 |

**レスポンス（成功）**
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "report_id": 1,
        "report_date": "2026-01-10",
        "salesperson_id": 1,
        "salesperson_name": "山田太郎",
        "status": "submitted",
        "status_label": "提出済",
        "visit_count": 3,
        "comment_count": 2,
        "has_unread_comments": true,
        "created_at": "2026-01-10T18:00:00+09:00",
        "updated_at": "2026-01-10T18:30:00+09:00"
      }
    ],
    "pagination": {
      "current_page": 1,
      "per_page": 20,
      "total_count": 50,
      "total_pages": 3
    }
  }
}
```

---

### 4.2 POST /reports
新規日報を作成する

**リクエスト**
```json
{
  "report_date": "2026-01-11",
  "problem": "株式会社Aの案件について、価格交渉が難航しています。",
  "plan": "・株式会社C 初回訪問（10:00）\n・株式会社B フォローアップ電話",
  "status": "draft",
  "visit_records": [
    {
      "customer_id": 1,
      "visit_time": "10:00",
      "visit_content": "新規提案を実施。先方は前向きに検討中。",
      "display_order": 1
    },
    {
      "customer_id": 2,
      "visit_time": "14:00",
      "visit_content": "見積提出。来週回答予定。",
      "display_order": 2
    }
  ]
}
```

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| report_date | string (YYYY-MM-DD) | ○ | 報告日 |
| problem | string | - | 課題・相談事項（最大4000文字） |
| plan | string | - | 明日の予定（最大4000文字） |
| status | string | ○ | ステータス（draft/submitted） |
| visit_records | array | - | 訪問記録リスト |
| visit_records[].customer_id | integer | ○ | 顧客ID |
| visit_records[].visit_time | string (HH:MM) | - | 訪問時刻 |
| visit_records[].visit_content | string | ○ | 訪問内容（最大2000文字） |
| visit_records[].display_order | integer | - | 表示順 |

**レスポンス（成功）**
```json
{
  "success": true,
  "data": {
    "report_id": 100,
    "message": "日報を作成しました"
  }
}
```

**エラーレスポンス**
| コード | 説明 |
|--------|------|
| 409 | 指定日の日報が既に存在する |
| 422 | バリデーションエラー |

---

### 4.3 GET /reports/{id}
日報の詳細を取得する

**パスパラメータ**
| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| id | integer | ○ | 日報ID |

**レスポンス（成功）**
```json
{
  "success": true,
  "data": {
    "report_id": 1,
    "report_date": "2026-01-10",
    "salesperson_id": 1,
    "salesperson_name": "山田太郎",
    "status": "submitted",
    "status_label": "提出済",
    "problem": "株式会社Aの案件について、価格交渉が難航しています。",
    "plan": "・株式会社C 初回訪問（10:00）\n・株式会社B フォローアップ電話",
    "visit_records": [
      {
        "visit_id": 1,
        "customer_id": 1,
        "customer_name": "株式会社A",
        "visit_time": "10:00",
        "visit_content": "新規提案を実施。先方は前向きに検討中。",
        "display_order": 1
      },
      {
        "visit_id": 2,
        "customer_id": 2,
        "customer_name": "株式会社B",
        "visit_time": "14:00",
        "visit_content": "見積提出。来週回答予定。",
        "display_order": 2
      }
    ],
    "comments": [
      {
        "comment_id": 1,
        "commenter_id": 10,
        "commenter_name": "佐藤課長",
        "comment_text": "株式会社Aの件、明日MTGで相談しましょう。",
        "created_at": "2026-01-10T18:30:00+09:00"
      }
    ],
    "can_edit": false,
    "can_confirm": true,
    "created_at": "2026-01-10T18:00:00+09:00",
    "updated_at": "2026-01-10T18:30:00+09:00"
  }
}
```

---

### 4.4 PUT /reports/{id}
日報を更新する（下書きステータスのみ）

**パスパラメータ**
| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| id | integer | ○ | 日報ID |

**リクエスト**
```json
{
  "report_date": "2026-01-11",
  "problem": "更新された課題内容",
  "plan": "更新された明日の予定",
  "status": "draft",
  "visit_records": [
    {
      "visit_id": 1,
      "customer_id": 1,
      "visit_time": "10:00",
      "visit_content": "更新された訪問内容",
      "display_order": 1
    },
    {
      "customer_id": 3,
      "visit_time": "15:00",
      "visit_content": "新規追加の訪問記録",
      "display_order": 2
    }
  ]
}
```

**レスポンス（成功）**
```json
{
  "success": true,
  "data": {
    "report_id": 1,
    "message": "日報を更新しました"
  }
}
```

**エラーレスポンス**
| コード | 説明 |
|--------|------|
| 403 | 編集権限がない（下書き以外） |
| 404 | 日報が見つからない |

---

### 4.5 DELETE /reports/{id}
日報を削除する（下書きステータスのみ）

**パスパラメータ**
| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| id | integer | ○ | 日報ID |

**レスポンス（成功）**
```json
{
  "success": true,
  "data": {
    "message": "日報を削除しました"
  }
}
```

---

### 4.6 PUT /reports/{id}/submit
日報を提出する（ステータスを「提出済」に変更）

**パスパラメータ**
| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| id | integer | ○ | 日報ID |

**リクエスト**
なし

**レスポンス（成功）**
```json
{
  "success": true,
  "data": {
    "report_id": 1,
    "status": "submitted",
    "message": "日報を提出しました"
  }
}
```

**エラーレスポンス**
| コード | 説明 |
|--------|------|
| 403 | 提出権限がない |
| 422 | 訪問記録が0件（提出には最低1件必要） |

---

### 4.7 PUT /reports/{id}/confirm
日報を確認済みにする（上長のみ）

**パスパラメータ**
| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| id | integer | ○ | 日報ID |

**リクエスト**
なし

**レスポンス（成功）**
```json
{
  "success": true,
  "data": {
    "report_id": 1,
    "status": "confirmed",
    "message": "日報を確認済みにしました"
  }
}
```

**エラーレスポンス**
| コード | 説明 |
|--------|------|
| 403 | 確認権限がない（上長以外） |
| 422 | 提出済でないため確認できない |

---

## 5. コメント API

### 5.1 GET /reports/{id}/comments
日報のコメント一覧を取得する

**パスパラメータ**
| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| id | integer | ○ | 日報ID |

**レスポンス（成功）**
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "comment_id": 1,
        "commenter_id": 10,
        "commenter_name": "佐藤課長",
        "comment_text": "株式会社Aの件、明日MTGで相談しましょう。",
        "created_at": "2026-01-10T18:30:00+09:00"
      },
      {
        "comment_id": 2,
        "commenter_id": 1,
        "commenter_name": "山田太郎",
        "comment_text": "承知しました。資料を準備しておきます。",
        "created_at": "2026-01-10T18:45:00+09:00"
      }
    ]
  }
}
```

---

### 5.2 POST /reports/{id}/comments
日報にコメントを投稿する

**パスパラメータ**
| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| id | integer | ○ | 日報ID |

**リクエスト**
```json
{
  "comment_text": "コメント内容"
}
```

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| comment_text | string | ○ | コメント内容（最大2000文字） |

**レスポンス（成功）**
```json
{
  "success": true,
  "data": {
    "comment_id": 3,
    "message": "コメントを投稿しました"
  }
}
```

---

## 6. 顧客 API

### 6.1 GET /customers
顧客一覧を取得する

**クエリパラメータ**
| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| company_name | string | - | 会社名（部分一致） |
| is_active | boolean | - | 有効フラグ |
| page | integer | - | ページ番号 |
| per_page | integer | - | 1ページあたり件数 |

**レスポンス（成功）**
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "customer_id": 1,
        "company_name": "株式会社A",
        "contact_name": "田中一郎",
        "phone": "03-1234-5678",
        "address": "東京都千代田区...",
        "is_active": true,
        "created_at": "2026-01-01T10:00:00+09:00",
        "updated_at": "2026-01-05T15:00:00+09:00"
      }
    ],
    "pagination": {
      "current_page": 1,
      "per_page": 20,
      "total_count": 50,
      "total_pages": 3
    }
  }
}
```

---

### 6.2 POST /customers
顧客を新規登録する

**リクエスト**
```json
{
  "company_name": "株式会社D",
  "contact_name": "鈴木四郎",
  "phone": "03-4567-8901",
  "address": "東京都港区...",
  "is_active": true
}
```

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| company_name | string | ○ | 会社名（最大200文字） |
| contact_name | string | - | 担当者名（最大100文字） |
| phone | string | - | 電話番号（最大20文字） |
| address | string | - | 住所（最大500文字） |
| is_active | boolean | - | 有効フラグ（デフォルト: true） |

**レスポンス（成功）**
```json
{
  "success": true,
  "data": {
    "customer_id": 100,
    "message": "顧客を登録しました"
  }
}
```

---

### 6.3 GET /customers/{id}
顧客の詳細を取得する

**パスパラメータ**
| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| id | integer | ○ | 顧客ID |

**レスポンス（成功）**
```json
{
  "success": true,
  "data": {
    "customer_id": 1,
    "company_name": "株式会社A",
    "contact_name": "田中一郎",
    "phone": "03-1234-5678",
    "address": "東京都千代田区...",
    "is_active": true,
    "created_at": "2026-01-01T10:00:00+09:00",
    "updated_at": "2026-01-05T15:00:00+09:00"
  }
}
```

---

### 6.4 PUT /customers/{id}
顧客情報を更新する

**パスパラメータ**
| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| id | integer | ○ | 顧客ID |

**リクエスト**
```json
{
  "company_name": "株式会社A（更新）",
  "contact_name": "田中一郎",
  "phone": "03-1234-5678",
  "address": "東京都千代田区...",
  "is_active": true
}
```

**レスポンス（成功）**
```json
{
  "success": true,
  "data": {
    "customer_id": 1,
    "message": "顧客情報を更新しました"
  }
}
```

---

### 6.5 DELETE /customers/{id}
顧客を削除する（論理削除）

**パスパラメータ**
| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| id | integer | ○ | 顧客ID |

**レスポンス（成功）**
```json
{
  "success": true,
  "data": {
    "message": "顧客を削除しました"
  }
}
```

---

## 7. 営業担当者 API

### 7.1 GET /salespersons
営業担当者一覧を取得する（管理者のみ）

**クエリパラメータ**
| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| name | string | - | 氏名（部分一致） |
| is_active | boolean | - | 有効フラグ |
| page | integer | - | ページ番号 |
| per_page | integer | - | 1ページあたり件数 |

**レスポンス（成功）**
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "salesperson_id": 1,
        "name": "山田太郎",
        "email": "yamada@example.com",
        "manager_id": 10,
        "manager_name": "佐藤課長",
        "is_active": true,
        "created_at": "2026-01-01T10:00:00+09:00",
        "updated_at": "2026-01-05T15:00:00+09:00"
      }
    ],
    "pagination": {
      "current_page": 1,
      "per_page": 20,
      "total_count": 15,
      "total_pages": 1
    }
  }
}
```

---

### 7.2 POST /salespersons
営業担当者を新規登録する（管理者のみ）

**リクエスト**
```json
{
  "name": "新規担当者",
  "email": "new@example.com",
  "password": "password123",
  "manager_id": 10,
  "is_active": true
}
```

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| name | string | ○ | 氏名（最大100文字） |
| email | string | ○ | メールアドレス（最大255文字、重複不可） |
| password | string | ○ | パスワード（最大100文字） |
| manager_id | integer | - | 上長ID |
| is_active | boolean | - | 有効フラグ（デフォルト: true） |

**レスポンス（成功）**
```json
{
  "success": true,
  "data": {
    "salesperson_id": 100,
    "message": "営業担当者を登録しました"
  }
}
```

**エラーレスポンス**
| コード | 説明 |
|--------|------|
| 409 | メールアドレスが既に使用されている |

---

### 7.3 GET /salespersons/{id}
営業担当者の詳細を取得する（管理者のみ）

**パスパラメータ**
| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| id | integer | ○ | 営業担当者ID |

**レスポンス（成功）**
```json
{
  "success": true,
  "data": {
    "salesperson_id": 1,
    "name": "山田太郎",
    "email": "yamada@example.com",
    "manager_id": 10,
    "manager_name": "佐藤課長",
    "is_active": true,
    "created_at": "2026-01-01T10:00:00+09:00",
    "updated_at": "2026-01-05T15:00:00+09:00"
  }
}
```

---

### 7.4 PUT /salespersons/{id}
営業担当者情報を更新する（管理者のみ）

**パスパラメータ**
| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| id | integer | ○ | 営業担当者ID |

**リクエスト**
```json
{
  "name": "山田太郎（更新）",
  "email": "yamada@example.com",
  "password": "newpassword123",
  "manager_id": 10,
  "is_active": true
}
```

| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| name | string | ○ | 氏名 |
| email | string | ○ | メールアドレス |
| password | string | - | パスワード（空欄の場合は変更なし） |
| manager_id | integer | - | 上長ID |
| is_active | boolean | ○ | 有効フラグ |

**レスポンス（成功）**
```json
{
  "success": true,
  "data": {
    "salesperson_id": 1,
    "message": "営業担当者情報を更新しました"
  }
}
```

---

### 7.5 DELETE /salespersons/{id}
営業担当者を削除する（論理削除、管理者のみ）

**パスパラメータ**
| パラメータ | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| id | integer | ○ | 営業担当者ID |

**レスポンス（成功）**
```json
{
  "success": true,
  "data": {
    "message": "営業担当者を削除しました"
  }
}
```

---

## 8. ダッシュボード API

### 8.1 GET /dashboard
ダッシュボード表示用の情報を取得する

**リクエスト**
なし

**レスポンス（成功）**
```json
{
  "success": true,
  "data": {
    "today_report": {
      "exists": true,
      "report_id": 100,
      "status": "draft",
      "status_label": "下書き"
    },
    "unread_comment_count": 3,
    "recent_reports": [
      {
        "report_id": 99,
        "report_date": "2026-01-10",
        "status": "confirmed",
        "status_label": "確認済",
        "visit_count": 5,
        "comment_count": 2
      },
      {
        "report_id": 98,
        "report_date": "2026-01-09",
        "status": "submitted",
        "status_label": "提出済",
        "visit_count": 3,
        "comment_count": 0
      }
    ]
  }
}
```

| フィールド | 説明 |
|-----------|------|
| today_report.exists | 本日の日報が存在するか |
| today_report.report_id | 本日の日報ID（存在する場合） |
| today_report.status | 本日の日報ステータス |
| unread_comment_count | 未読コメント数 |
| recent_reports | 直近7日間の日報リスト |

---

## 9. セレクトボックス用 API

### 9.1 GET /customers/select
顧客セレクトボックス用のリストを取得する（有効な顧客のみ）

**レスポンス（成功）**
```json
{
  "success": true,
  "data": {
    "items": [
      { "value": 1, "label": "株式会社A" },
      { "value": 2, "label": "株式会社B" },
      { "value": 3, "label": "株式会社C" }
    ]
  }
}
```

---

### 9.2 GET /salespersons/select
営業担当者セレクトボックス用のリストを取得する（有効な担当者のみ）

**レスポンス（成功）**
```json
{
  "success": true,
  "data": {
    "items": [
      { "value": 1, "label": "山田太郎" },
      { "value": 2, "label": "鈴木花子" },
      { "value": 10, "label": "佐藤課長" }
    ]
  }
}
```

---

### 9.3 GET /salespersons/subordinates
部下一覧を取得する（上長用、日報検索の担当者フィルタ用）

**レスポンス（成功）**
```json
{
  "success": true,
  "data": {
    "items": [
      { "value": 1, "label": "山田太郎" },
      { "value": 2, "label": "鈴木花子" }
    ]
  }
}
```

---

## 10. ステータス定義

### 日報ステータス
| 値 | ラベル | 説明 |
|----|--------|------|
| draft | 下書き | 作成中、編集可能 |
| submitted | 提出済 | 提出済み、編集不可 |
| confirmed | 確認済 | 上長が確認済み |

### ステータス遷移
```
draft → submitted → confirmed
  ↑
  └── (削除可能)
```

---

## 11. 認可ルール

| API | 一般営業 | 上長 | 管理者 |
|-----|---------|------|--------|
| 自分の日報 CRUD | ○ | ○ | ○ |
| 部下の日報閲覧 | × | ○ | ○ |
| 日報確認済み更新 | × | ○ | ○ |
| コメント投稿 | ○ | ○ | ○ |
| 顧客 参照 | ○ | ○ | ○ |
| 顧客 登録・更新・削除 | × | ○ | ○ |
| 営業担当者 全操作 | × | × | ○ |
| ダッシュボード | ○ | ○ | ○ |
