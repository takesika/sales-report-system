import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "営業日報システム",
  description: "営業担当者が日々の顧客訪問活動を報告するシステム",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ja">
      <body>{children}</body>
    </html>
  );
}
