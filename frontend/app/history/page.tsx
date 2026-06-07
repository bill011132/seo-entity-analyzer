"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { supabase } from "@/lib/supabase";

export default function HistoryPage() {
  const router = useRouter();
  const [history, setHistory] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadHistory() {
      const { data: userData } = await supabase.auth.getUser();

      if (!userData.user) {
        router.push("/login");
        return;
      }

      const { data, error } = await supabase
        .from("analysis_history")
        .select("*")
        .order("created_at", { ascending: false });

      if (!error && data) {
        setHistory(data);
      }

      setLoading(false);
    }

    loadHistory();
  }, [router]);

  if (loading) {
    return <main style={{ padding: 24 }}>載入中...</main>;
  }

  return (
    <main style={{ maxWidth: 900, margin: "40px auto", padding: 24 }}>
      <h1>分析歷史紀錄</h1>

      <button onClick={() => router.push("/dashboard")}>回到 Dashboard</button>

      <table style={{ width: "100%", marginTop: 24, borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th style={{ borderBottom: "1px solid #ccc", textAlign: "left" }}>時間</th>
            <th style={{ borderBottom: "1px solid #ccc", textAlign: "left" }}>關鍵字</th>
            <th style={{ borderBottom: "1px solid #ccc", textAlign: "left" }}>文章數</th>
          </tr>
        </thead>

        <tbody>
          {history.map((item) => (
            <tr key={item.id}>
              <td style={{ padding: 8 }}>{new Date(item.created_at).toLocaleString()}</td>
              <td style={{ padding: 8 }}>{item.keyword}</td>
              <td style={{ padding: 8 }}>{item.result_count}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </main>
  );
}