-- CreateTable: REPORT_COMMENT（日報コメントテーブル）
-- 日報に対するコメントテーブル。上長や本人が複数コメントを投稿可能
-- ER図・テーブル定義書（docs/er-diagram.md）に基づき作成
--
-- 依存テーブル:
--   - DAILY_REPORT (report_id)
--   - SALESPERSON (commenter_id)

CREATE TABLE `REPORT_COMMENT` (
    `comment_id` INTEGER NOT NULL AUTO_INCREMENT COMMENT 'コメントID',
    `report_id` INTEGER NOT NULL COMMENT '日報ID',
    `commenter_id` INTEGER NOT NULL COMMENT 'コメント者ID（営業担当者）',
    `comment_text` TEXT NOT NULL COMMENT 'コメント内容（最大2000文字）',
    `created_at` DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) COMMENT 'コメント投稿日時',

    -- インデックス: 日報ID（日報ごとのコメント取得用）
    INDEX `IX_REPORT_COMMENT_REPORT`(`report_id`),
    -- インデックス: コメント者ID（コメント者ごとの検索用）
    INDEX `IX_REPORT_COMMENT_COMMENTER`(`commenter_id`),
    -- インデックス: 作成日時（時系列でのソート用）
    INDEX `IX_REPORT_COMMENT_CREATED`(`created_at`),

    PRIMARY KEY (`comment_id`)
) DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- AddForeignKey: 日報への参照
-- 日報削除時はコメントもカスケード削除
ALTER TABLE `REPORT_COMMENT` ADD CONSTRAINT `FK_REPORT_COMMENT_REPORT`
    FOREIGN KEY (`report_id`) REFERENCES `DAILY_REPORT`(`report_id`)
    ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey: コメント者（営業担当者）への参照
-- コメント者は参照がある場合は削除不可（RESTRICT）
ALTER TABLE `REPORT_COMMENT` ADD CONSTRAINT `FK_REPORT_COMMENT_COMMENTER`
    FOREIGN KEY (`commenter_id`) REFERENCES `SALESPERSON`(`salesperson_id`)
    ON DELETE RESTRICT ON UPDATE CASCADE;
