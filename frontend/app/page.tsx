import Link from "next/link";

export default function HomePage() {
  return (
    <main style={{ maxWidth: 720, margin: "80px auto", padding: 24 }}>
      <h1>SEO Entity Analyzer</h1>

      <p>
        這是一個可以輸入關鍵字、抓取 Google 第一頁結果、分析 entity、
        進行主題分群，並輸出到 Google Sheet 的工具。
      </p>

      <div style={{ marginTop: 24, display: "flex", gap: 12 }}>
        <Link href="/login">登入</Link>
        <Link href="/register">註冊</Link>
        <Link href="/dashboard">進入 Dashboard</Link>
      </div>
    </main>
  );
}