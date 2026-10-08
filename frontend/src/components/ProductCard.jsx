import { Link } from "react-router-dom";

function fallbackImage(product) {
  const category = (product.category_name || "").toLowerCase();
  const images = {
    mobile: "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=900&q=85",
    laptop: "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=900&q=85",
    audio: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=900&q=85",
    home: "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&w=900&q=85",
    fashion: "https://images.unsplash.com/photo-1445205170230-053b83016050?auto=format&fit=crop&w=900&q=85",
  };

  return Object.entries(images).find(([key]) => category.includes(key))?.[1] ||
    "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?auto=format&fit=crop&w=900&q=85";
}

export default function ProductCard({ product, onAdd, isWishlisted, onToggleWishlist }) {
  const image = product.image_url || fallbackImage(product);

  return (
    <article className="product-card">
      <div className="product-image-wrap">
        <Link to={`/products/${product.id}`} className="product-image-link">
          <img className="product-image" src={image} alt={product.name} loading="lazy" />
        </Link>
        <button
          className={`wishlist-button${isWishlisted ? " wishlisted" : ""}`}
          onClick={() => onToggleWishlist(product)}
          aria-label={isWishlisted ? "Remove from wishlist" : "Add to wishlist"}
          title={isWishlisted ? "Remove from wishlist" : "Add to wishlist"}
        >
          {isWishlisted ? "♥" : "♡"}
        </button>
      </div>

      <div className="product-card-body">
        <p className="category-label">{product.category_name || "E-Commerce"}</p>
        <h3>{product.name}</h3>
        <p className="sku">SKU: {product.sku}</p>
        <div className="product-row">
          <strong>₹{Number(product.price).toLocaleString("en-IN")}</strong>
          <span>{product.stock_quantity > 0 ? `${product.stock_quantity} in stock` : "Out of stock"}</span>
        </div>
        <div className="product-actions">
          <Link className="secondary-button" to={`/products/${product.id}`}>View</Link>
          <button disabled={!product.stock_quantity} onClick={() => onAdd(product)}>
            Add to cart
          </button>
        </div>
      </div>
    </article>
  );
}
