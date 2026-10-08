import { Link } from "react-router-dom";

export default function Wishlist({ wishlist, onToggle, onAdd }) {
  return (
    <main className="section">
      <div className="section-heading"><div><p className="eyebrow">Shopping</p><h1>Wishlist</h1></div><span>{wishlist.length} saved</span></div>
      {!wishlist.length ? <div className="empty-state"><h2>Your wishlist is empty</h2><p>Save products you want to revisit later.</p><Link className="primary-button" to="/products">Browse products</Link></div> : (
        <div className="product-grid">
          {wishlist.map((product) => <article className="product-card" key={product.id}>
            <Link to={`/products/${product.id}`}><img className="product-image" src={product.image_url} alt={product.name} loading="lazy" /></Link>
            <div className="product-card-body"><p className="category-label">{product.category_name || "E-Commerce"}</p><h3>{product.name}</h3>
              <div className="product-row"><strong>₹{Number(product.price).toLocaleString("en-IN")}</strong><span>{product.stock_quantity > 0 ? "In stock" : "Out of stock"}</span></div>
              <div className="product-actions"><button disabled={!product.stock_quantity} onClick={() => onAdd(product)}>Add to cart</button><button className="remove-button" onClick={() => onToggle(product)}>Remove</button></div>
            </div>
          </article>)}
        </div>
      )}
    </main>
  );
}
