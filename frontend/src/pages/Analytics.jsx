import { useCallback, useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { api } from "../services/api";

const emptyDashboard = { revenue: 0, orders: 0, customers: 0, average_order_value: 0, daily_metrics: [] };

export default function Analytics() {
  const [data, setData] = useState(emptyDashboard);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadDashboard = useCallback(async () => {
    setLoading(true);
    setError("");
    try { setData(await api.dashboard()); }
    catch (err) { setError(err.message || "Unable to load analytics"); }
    finally { setLoading(false); }
  }, []);

  useEffect(() => { loadDashboard(); }, [loadDashboard]);

  return (
    <main className="section">
      <div className="section-heading">
        <div><p className="eyebrow">PySpark Gold</p><h1>Analytics</h1><p>PostgreSQL → PySpark Gold → serving layer → Django REST</p></div>
        <button onClick={loadDashboard} disabled={loading}>{loading ? "Refreshing..." : "Refresh"}</button>
      </div>
      {error && <p role="alert" className="error">{error}</p>}
      <section className="cards">
        <article><span>Revenue</span><strong>₹{Number(data.revenue).toLocaleString()}</strong></article>
        <article><span>Orders</span><strong>{Number(data.orders).toLocaleString()}</strong></article>
        <article><span>Customers</span><strong>{Number(data.customers).toLocaleString()}</strong></article>
        <article><span>Average Order Value</span><strong>₹{Number(data.average_order_value).toLocaleString()}</strong></article>
      </section>
      <section className="panel"><h2>Daily Revenue</h2><div className="chart">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data.daily_metrics}><XAxis dataKey="date" /><YAxis /><Tooltip /><Line type="monotone" dataKey="revenue" strokeWidth={2} /></LineChart>
        </ResponsiveContainer>
      </div></section>
    </main>
  );
}
