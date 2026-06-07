"use client";

import { useState } from "react";

export default function Home() {
  const [keyword, setKeyword] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");

  const handleAnalyzeAndExport = async () => {
    if (!keyword.trim()) {
      setError("請輸入關鍵字");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

      const res = await fetch(
        `${API_BASE_URL}/api/analyze-and-export?keyword=${encodeURIComponent(keyword)}`
      );

      if (!res.ok) {
        throw new Error("API request failed");
      }

      const data = await res.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message || "分析失敗");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main style={{ padding: "40px", fontFamily: "Arial, sans-serif" }}>
      <h1>SEO Entity Analyzer</h1>

      <p>請輸入關鍵字，系統會分析 Google 第一頁前 10 名文章的 Entity，並輸出到 Google Sheet。</p>

      <input
        type="text"
        value={keyword}
        onChange={(e) => setKeyword(e.target.value)}
        placeholder="例如：4G 吃到飽"
        style={{
          padding: "10px",
          width: "320px",
          border: "1px solid #ccc",
          borderRadius: "6px",
        }}
      />

      <button
        onClick={handleAnalyzeAndExport}
        disabled={loading}
        style={{
          marginLeft: "12px",
          padding: "10px 18px",
          border: "none",
          borderRadius: "6px",
          cursor: "pointer",
        }}
      >
        {loading ? "分析中..." : "分析並匯出"}
      </button>

      {error && (
        <p style={{ color: "red", marginTop: "16px" }}>
          {error}
        </p>
      )}

      {result && (
        <section style={{ marginTop: "32px" }}>
          <h2>分析完成</h2>

          <p>
            <strong>關鍵字：</strong>
            {result.keyword}
          </p>

          <p>
            <strong>文章數量：</strong>
            {result.result_count}
          </p>

          <p>
            <strong>Google Sheet 匯出：</strong>
            {result.sheet_result?.success ? "成功" : "失敗"}
          </p>

          <h3>主題分群結果</h3>

          {result.topic_groups?.map((group: any) => (
            <div
              key={group.topic}
              style={{
                marginTop: "16px",
                padding: "16px",
                border: "1px solid #ddd",
                borderRadius: "8px",
              }}
            >
              <h4>{group.topic}</h4>
              <p>總出現次數：{group.total_count}</p>
              <p>不重複 Entity 數：{group.unique_entity_count}</p>

              <ul>
                {group.entities?.slice(0, 10).map((item: any) => (
                  <li key={item.entity}>
                    {item.entity}：{item.count}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </section>
      )}
    </main>
  );
}