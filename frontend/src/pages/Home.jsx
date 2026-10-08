import { Link } from "react-router-dom";

export default function Home({ products }) {
  return (
    <main>
      <section className="hero">
        <div>
          <p className="eyebrow">Big Data E-Commerce Platform</p>
          <h1>Shop today.<br /><span>Understand tomorrow.</span></h1>
          <p className="hero-copy">
            A full-stack store powered by Django, PostgreSQL and a PySpark
            Bronze → Silver → Gold analytics pipeline.
          </p>
          <div className="hero-actions">
            <Link to="/products" className="primary-button">Explore products</Link>
            <Link to="/analytics" className="secondary-button">View analytics</Link>
          </div>
        </div>
        <div className="hero-card">
          <span>Platform flow</span>
          <strong>Store → Orders → PySpark</strong>
          <small>PostgreSQL → Bronze → Silver → Gold</small>
        </div>
      </section>

      <section className="section">
        <div className="section-heading">
          <div><p className="eyebrow">Featured</p><h2>Latest products</h2></div>
          <Link to="/products">View all →</Link>
        </div>
        <div className="feature-strip">
          {products.slice(0, 3).map((product) => (
            <Link className="mini-product" key={product.id} to={`/products/${product.id}`}>
              <span>{product.category_name || "Product"}</span>
              <strong>{product.name}</strong>
              <b>₹{Number(product.price).toLocaleString()}</b>
            </Link>
          ))}
        </div>
      </section>
    </main>
  );
}
