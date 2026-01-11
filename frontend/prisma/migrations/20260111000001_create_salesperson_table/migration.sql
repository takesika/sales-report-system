-- CreateTable: SALESPERSON（営業担当者マスタ）
-- 上長も同テーブルで管理し、manager_idで階層構造を表現
-- ER図・テーブル定義書（docs/er-diagram.md）に基づき作成

CREATE TABLE `SALESPERSON` (
    `salesperson_id` INTEGER NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(100) NOT NULL COMMENT '氏名',
    `email` VARCHAR(255) NOT NULL COMMENT 'メールアドレス（ログインID）',
    `password_hash` VARCHAR(255) NOT NULL COMMENT 'パスワードハッシュ',
    `manager_id` INTEGER NULL COMMENT '上長ID（自己参照、NULLは最上位者）',
    `is_active` BOOLEAN NOT NULL DEFAULT true COMMENT '有効フラグ',
    `created_at` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) COMMENT '作成日時',
    `updated_at` DATETIME(3) NOT NULL COMMENT '更新日時',

    -- ユニークインデックス: メールアドレス
    UNIQUE INDEX `UK_SALESPERSON_EMAIL`(`email`),
    -- インデックス: 上長ID（上長-部下の検索用）
    INDEX `IX_SALESPERSON_MANAGER`(`manager_id`),

    PRIMARY KEY (`salesperson_id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- AddForeignKey: 自己参照（上長-部下）
-- manager_idはSALESPERSON.salesperson_idを参照
ALTER TABLE `SALESPERSON` ADD CONSTRAINT `FK_SALESPERSON_MANAGER`
    FOREIGN KEY (`manager_id`) REFERENCES `SALESPERSON`(`salesperson_id`)
    ON DELETE SET NULL ON UPDATE CASCADE;
