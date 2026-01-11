-- CreateTable: CUSTOMER（顧客マスタ）
-- ER図・テーブル定義書（docs/er-diagram.md）に基づき作成

CREATE TABLE `CUSTOMER` (
    `customer_id` INTEGER NOT NULL AUTO_INCREMENT,
    `company_name` VARCHAR(200) NOT NULL COMMENT '会社名',
    `contact_name` VARCHAR(100) NULL COMMENT '担当者名',
    `phone` VARCHAR(20) NULL COMMENT '電話番号',
    `address` VARCHAR(500) NULL COMMENT '住所',
    `is_active` BOOLEAN NOT NULL DEFAULT true COMMENT '有効フラグ',
    `created_at` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) COMMENT '作成日時',
    `updated_at` DATETIME(3) NOT NULL COMMENT '更新日時',

    -- インデックス: 会社名（検索用）
    INDEX `IX_CUSTOMER_COMPANY_NAME`(`company_name`),
    -- インデックス: 有効フラグ（絞り込み用）
    INDEX `IX_CUSTOMER_IS_ACTIVE`(`is_active`),

    PRIMARY KEY (`customer_id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
