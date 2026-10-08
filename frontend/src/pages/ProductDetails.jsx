import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api } from "../services/api";

export default function ProductDetails({ onAdd }) {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    api.product(id)
      .then(setProduct)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <main className="section"><div className="loading">Loading product...</div></main>;
  if (error || !product) return <main className="section"><div className="empty-state"><h2>Product not found</h2><Link to="/products">Back to products</Link></div></main>;

  const image = product.image_url || "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?auto=format&fit=crop&w=1200&q=85";

  return (
    <main className="section">
      <Link to="/products" className="back-link">← Back to products</Link>
      <section className="detail-card">
        <img className="detail-image" src={image} alt={product.name} />
        <div className="detail-content">
          <p className="category-label">{product.category_name}</p>
          <h1>{product.name}</h1>
          <p className="sku">SKU: {product.sku}</p>
          <h2>₹{Number(product.price).toLocaleString("en-IN")}</h2>
          <p className="stock">{product.stock_quantity > 0 ? `✓ ${product.stock_quantity} available` : "Currently unavailable"}</p>
          <p>Quality product from the ShopSpark catalog. Inventory and pricing are managed through the Django commerce API.</p>
          <button disabled={!product.stock_quantity} onClick={() => onAdd(product)}>Add to cart</button>
        </div>
      </section>
    </main>
  );
}
