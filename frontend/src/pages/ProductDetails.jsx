import { Link } from "react-router-dom";

export default function ProductDetails({ product, onAdd }) {
  if (!product) return <main className="section"><div className="empty-state"><h2>Product not found</h2><Link to="/products">Back to products</Link></div></main>;

  return (
    <main className="section">
      <Link to="/products" className="back-link">← Back to products</Link>
      <section className="detail-card">
        <div className="detail-image"><span>{product.category_name || "Product"}</span></div>
        <div className="detail-content">
          <p className="category-label">{product.category_name}</p>
          <h1>{product.name}</h1>
          <p className="sku">SKU: {product.sku}</p>
          <h2>₹{Number(product.price).toLocaleString()}</h2>
          <p className="stock">{product.stock_quantity > 0 ? `✓ ${product.stock_quantity} available` : "Currently unavailable"}</p>
          <p>Quality product from the ShopSpark catalog. Inventory and pricing are managed through the Django commerce API.</p>
          <button disabled={!product.stock_quantity} onClick={() => onAdd(product)}>Add to cart</button>
        </div>
      </section>
    </main>
  );
}
