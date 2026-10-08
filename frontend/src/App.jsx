import { useCallback, useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";
const emptyDashboard = { revenue: 0, orders: 0, customers: 0, average_order_value: 0, daily_metrics: [] };

export default function App() {
  const [data, setData] = useState(emptyDashboard);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadDashboard = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const response = await fetch(`${API_URL}/dashboard/`);
      if (!response.ok) throw new Error(`Dashboard API returned ${response.status}`);
      setData(await response.json());
    } catch (err) {
      setError(err.message || "Unable to load dashboard");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { loadDashboard(); }, [loadDashboard]);

  return (
    <main className="dashboard">
      <header>
        <p className="eyebrow">PySpark Big Data Project</p>
        <h1>E-Commerce Analytics</h1>
        <p>React → Django REST → PostgreSQL → PySpark Gold data</p>
        <button onClick={loadDashboard} disabled={loading}>{loading ? "Refreshing..." : "Refresh dashboard"}</button>
      </header>
      {error && <p role="alert" className="error">{error}</p>}
      <section className="cards">
        <article><span>Revenue</span><strong>₹{Number(data.revenue).toLocaleString()}</strong></article>
        <article><span>Orders</span><strong>{Number(data.orders).toLocaleString()}</strong></article>
        <article><span>Customers</span><strong>{Number(data.customers).toLocaleString()}</strong></article>
        <article><span>Average Order Value</span><strong>₹{Number(data.average_order_value).toLocaleString()}</strong></article>
      </section>
      <section className="panel">
        <h2>Daily Revenue</h2>
        <div className="chart">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data.daily_metrics}>
              <XAxis dataKey="date" /><YAxis /><Tooltip />
              <Line type="monotone" dataKey="revenue" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </section>
    </main>
  );
}
