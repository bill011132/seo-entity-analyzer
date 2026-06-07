"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { supabase } from "@/lib/supabase";

type User = {
  id: string;
  email?: string;
};

export default function DashboardPage() {
  const router = useRouter();

  const [user, setUser] = useState<User | null>(null);
  const [keyword, setKeyword] = useState("4G 吃到飽");
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [message, setMessage] = useState("");

  const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;

  useEffect(() => {
    async function checkUser() {
      const { data } = await supabase.auth.getUser();

      if (!data.user) {
        router.push("/login");
        return;
      }

      setUser({
        id: data.user.id,
        email: data.user.email || "",
      });

      setLoading(false);
    }

    checkUser();
  }, [router]);

  async function handleAnalyze() {
    if (!user) return;

    setAnalyzing(true);
    setMessage("");
    setResult(null);

    try {
      const res = await fetch(
        `${apiBaseUrl}/api/analyze-and-export?keyword=${encodeURIComponent(keyword)}`
      );

      if (!res.ok) {
        throw new Error("API request failed");
      }

      const data = await res.json();
      setResult(data);

      const { error } = await supabase.from("analysis_history").insert({
        user_id: user.id,
        keyword,
        result_count: data.result_count,
        articles: data.articles,
        topic_groups: data.topic_groups,
        sheet_result: data.sheet_result,
      });

      if (error) {
        throw error;
      }

      setMessage("分析完成，已輸出到 Google Sheet，並儲存到 Supabase。");
    } catch (error: any) {
      setMessage(error.message || "發生錯誤");
    } finally {
      setAnalyzing(false);
    }
  }

  async function handleLogout() {
    await supabase.auth.signOut();
    router.push("/login");
  }

  if (loading) {
    return <main style={{ padding: 24 }}>載入中...</main>;
  }

  return (
    <main style={{ maxWidth: 900, margin: "40px auto", padding: 24 }}>
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <div>
          <h1>SEO Entity Analyzer</h1>
          <p>登入帳號：{user?.email}</p>
        </div>

        <button onClick={handleLogout}>登出</button>
      </div>

      <div style={{ marginTop: 24 }}>
        <label>輸入關鍵字</label>
        <input
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          style={{ width: "100%", padding: 10, marginTop: 6 }}
        />

        <button
          onClick={handleAnalyze}
          disabled={analyzing}
          style={{ marginTop: 12, padding: 10 }}
        >
          {analyzing ? "分析中..." : "開始分析並輸出到 Google Sheet"}
        </button>
      </div>

      {message && <p style={{ marginTop: 16 }}>{message}</p>}

      {result && (
        <section style={{ marginTop: 32 }}>
          <h2>分析結果摘要</h2>
          <p>關鍵字：{result.keyword}</p>
          <p>文章數：{result.result_count}</p>

          <h3>主題分群</h3>
          <ul>
            {result.topic_groups?.map((group: any) => (
              <li key={group.topic}>
                {group.topic}：{group.total_count} 次，{group.unique_entity_count} 個 entity
              </li>
            ))}
          </ul>
        </section>
      )}
    </main>
  );
}