import { Link } from "react-router-dom";
import { imageForProduct } from "../services/productImages";

export default function ProductDetails({ product, onAdd }) {
  if (!product) return <main className="section"><div className="empty-state"><h2>Product not found</h2><Link className="back-link" to="/products">Back to products</Link></div></main>;
  return (
    <main className="section">
      <Link to="/products" className="back-link">← Back to products</Link>
      <section className="detail-card">
        <div className="detail-image"><img src={imageForProduct(product)} alt={product.name} /></div>
        <div className="detail-content">
          <p className="category-label">{product.category_name}</p><h1>{product.name}</h1><p className="sku">SKU: {product.sku}</p>
          <h2>₹{Number(product.price).toLocaleString("en-IN")}</h2>
          <p className="stock">{product.stock_quantity > 0 ? "✓ " + product.stock_quantity + " available for immediate purchase" : "Currently unavailable"}</p>
          <p>Designed for everyday use with reliable quality. Inventory and pricing are managed through the Django commerce API, while purchase analytics can flow into the PySpark data platform.</p>
          <button disabled={!product.stock_quantity} onClick={() => onAdd(product)}>Add to cart</button>
        </div>
      </section>
    </main>
  );
}