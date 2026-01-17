import { useEffect, useState } from "react";

interface NewsItem {
  symbol: string;
  headline: string;
  source: string;
  timestamp: number;
  url: string;
}

export default function NewsPanel({ symbol }: { symbol: string | null }) {
  const [news, setNews] = useState<NewsItem[]>([]);

  useEffect(() => {
    if (!symbol) return;

    fetch(`http://localhost:8000/news/${symbol}`)
      .then(res => res.json())
      .then(setNews)
      .catch(err => console.error("News fetch failed:", err));
  }, [symbol]);

  return (
    <div className="panel">
      <h2>News for {symbol || "—"}</h2>

      {news.length === 0 && <div>No news available.</div>}

      {news.map((n, i) => (
        <div key={i} className="news-item" style={{ marginBottom: "12px" }}>
          <a href={n.url} target="_blank" rel="noreferrer">
            <strong>{n.headline}</strong>
          </a>
          <div style={{ fontSize: "0.85rem", opacity: 0.7 }}>
            {n.source} — {new Date(n.timestamp * 1000).toLocaleString()}
          </div>
        </div>
      ))}
    </div>
  );
}
