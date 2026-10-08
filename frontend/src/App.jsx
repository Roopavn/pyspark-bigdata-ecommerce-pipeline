import { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

export default function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch(`${API_URL}/dashboard/`)
      .then((response) => response.json())
      .then(setData)
      .catch(() => setData({ revenue: 0, orders: 0, customers: 0, daily_metrics: [] }));
  }, []);

  const metrics = data || { revenue: 0, orders: 0, customers: 0, daily_metrics: [] };

  return (
    <main className="dashboard">
      <header>
        <p className="eyebrow">PySpark Big Data Project</p>
        <h1>E-Commerce Analytics</h1>
        <p>React → Django REST → PostgreSQL → PySpark Gold data</p>
      </header>

      <section className="cards">
        <article><span>Revenue</span><strong>₹{Number(metrics.revenue).toLocaleString()}</strong></article>
        <article><span>Orders</span><strong>{Number(metrics.orders).toLocaleString()}</strong></article>
        <article><span>Customers</span><strong>{Number(metrics.customers).toLocaleString()}</strong></article>
      </section>

      <section className="panel">
        <h2>Daily Revenue</h2>
        <div className="chart">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={metrics.daily_metrics}>
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="revenue" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </section>
    </main>
  );
}
