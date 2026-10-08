import { Link } from "react-router-dom";
import { imageForProduct } from "../services/productImages";

export default function ProductCard({ product, onAdd }) {
  return (
    <article className="product-card">
      <div className="product-image">
        <img src={imageForProduct(product)} alt={product.name} loading="lazy" />
      </div>
      <div className="product-card-body">
        <p className="category-label">{product.category_name || "E-Commerce"}</p>
        <h3>{product.name}</h3>
        <p className="sku">SKU: {product.sku}</p>
        <div className="product-row">
          <strong>₹{Number(product.price).toLocaleString("en-IN")}</strong>
          <span>{product.stock_quantity > 0 ? product.stock_quantity + " in stock" : "Out of stock"}</span>
        </div>
        <div className="product-actions">
          <Link className="secondary-button" to={"/products/" + product.id}>View details</Link>
          <button disabled={!product.stock_quantity} onClick={() => onAdd(product)}>Add to cart</button>
        </div>
      </div>
    </article>
  );
}