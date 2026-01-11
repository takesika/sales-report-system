-- CreateTable: VISIT_RECORD（訪問記録テーブル）
-- 日報に紐づく訪問記録テーブル。1日報に対して複数の訪問記録を登録可能
-- ER図・テーブル定義書（docs/er-diagram.md）に基づき作成

CREATE TABLE `VISIT_RECORD` (
    `visit_id` INTEGER NOT NULL AUTO_INCREMENT,
    `report_id` INTEGER NOT NULL COMMENT '日報ID',
    `customer_id` INTEGER NOT NULL COMMENT '顧客ID',
    `visit_content` TEXT NOT NULL COMMENT '訪問内容（最大2000文字）',
    `visit_time` TIME NULL COMMENT '訪問時刻',
    `display_order` INTEGER NOT NULL DEFAULT 0 COMMENT '表示順',
    `created_at` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) COMMENT '作成日時',
    `updated_at` DATETIME(3) NOT NULL COMMENT '更新日時',

    -- インデックス: 日報ID（日報に紐づく訪問記録の検索用）
    INDEX `IX_VISIT_RECORD_REPORT`(`report_id`),
    -- インデックス: 顧客ID（顧客の訪問履歴検索用）
    INDEX `IX_VISIT_RECORD_CUSTOMER`(`customer_id`),

    PRIMARY KEY (`visit_id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- AddForeignKey: 日報への外部キー（カスケード削除）
-- 日報を削除すると紐づく訪問記録も自動削除される
ALTER TABLE `VISIT_RECORD` ADD CONSTRAINT `FK_VISIT_RECORD_REPORT`
    FOREIGN KEY (`report_id`) REFERENCES `DAILY_REPORT`(`report_id`)
    ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey: 顧客への外部キー（削除制限）
-- 訪問記録が存在する顧客は削除不可
ALTER TABLE `VISIT_RECORD` ADD CONSTRAINT `FK_VISIT_RECORD_CUSTOMER`
    FOREIGN KEY (`customer_id`) REFERENCES `CUSTOMER`(`customer_id`)
    ON DELETE RESTRICT ON UPDATE CASCADE;
