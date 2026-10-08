import { Link } from "react-router-dom";
import { imageForProduct } from "../services/productImages";

export default function Home({ products }) {
  const featured = products.slice(0, 3);
  const heroProduct = products[0];
  return (
    <main>
      <section className="hero">
        <div>
          <p className="eyebrow">Next-generation commerce</p>
          <h1>Discover products.<br /><span>Shop smarter.</span></h1>
          <p className="hero-copy">A production-style e-commerce experience backed by Django, PostgreSQL and a PySpark Bronze → Silver → Gold analytics platform.</p>
          <div className="hero-actions"><Link to="/products" className="primary-button">Start shopping →</Link><Link to="/analytics" className="secondary-button">View insights</Link></div>
        </div>
        <div className="hero-visual">
          {heroProduct && <img className="hero-product-image" src={imageForProduct(heroProduct)} alt="" />}
          <div className="visual-card main"><span>Today's store performance</span><strong className="metric">₹2.67L</strong><span>Revenue processed through the analytics pipeline</span></div>
          <div className="visual-card small left"><span>Orders</span><strong>15</strong></div>
          <div className="visual-card small right"><span>Customers</span><strong>11</strong></div>
        </div>
      </section>
      <section className="section">
        <div className="section-heading"><div><p className="eyebrow">Curated for you</p><h2>Trending products</h2></div><Link className="back-link" to="/products">View all →</Link></div>
        <div className="feature-strip">{featured.map((product) => <Link className="mini-product" key={product.id} to={"/products/" + product.id}><img src={imageForProduct(product)} alt="" /><div className="mini-product-info"><span>{product.category_name || "Featured"}</span><strong>{product.name}</strong><b>₹{Number(product.price).toLocaleString("en-IN")}</b></div></Link>)}</div>
        <div className="trust-strip">
          <div className="trust-card"><b>⚡ Fast shopping</b><span>Simple browsing and a persistent cart.</span></div>
          <div className="trust-card"><b>🔒 Secure foundation</b><span>Django APIs and PostgreSQL-ready architecture.</span></div>
          <div className="trust-card"><b>📊 Data-driven</b><span>Every order can feed the PySpark analytics pipeline.</span></div>
        </div>
      </section>
    </main>
  );
}
