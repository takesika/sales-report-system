-- CreateTable: DAILY_REPORT（日報テーブル）
-- 営業担当者ごと・日付ごとに1レコード
-- ER図・テーブル定義書（docs/er-diagram.md）に基づき作成

CREATE TABLE `DAILY_REPORT` (
    `report_id` INTEGER NOT NULL AUTO_INCREMENT,
    `salesperson_id` INTEGER NOT NULL COMMENT '営業担当者ID',
    `report_date` DATE NOT NULL COMMENT '報告日',
    `problem` TEXT NULL COMMENT '課題・相談事項（最大4000文字）',
    `plan` TEXT NULL COMMENT '明日の予定（最大4000文字）',
    `status` VARCHAR(20) NOT NULL DEFAULT 'draft' COMMENT 'ステータス（draft/submitted/confirmed）',
    `created_at` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) COMMENT '作成日時',
    `updated_at` DATETIME(3) NOT NULL COMMENT '更新日時',

    -- ユニーク制約: 同一営業担当者が同じ日付の日報を複数作成不可
    UNIQUE INDEX `UK_DAILY_REPORT_DATE`(`salesperson_id`, `report_date`),
    -- インデックス: 報告日（日付での検索用）
    INDEX `IX_DAILY_REPORT_DATE`(`report_date`),
    -- インデックス: ステータス（絞り込み用）
    INDEX `IX_DAILY_REPORT_STATUS`(`status`),

    PRIMARY KEY (`report_id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- AddForeignKey: 営業担当者への参照
-- salesperson_idはSALESPERSON.salesperson_idを参照
ALTER TABLE `DAILY_REPORT` ADD CONSTRAINT `FK_DAILY_REPORT_SALESPERSON`
    FOREIGN KEY (`salesperson_id`) REFERENCES `SALESPERSON`(`salesperson_id`)
    ON DELETE RESTRICT ON UPDATE CASCADE;
