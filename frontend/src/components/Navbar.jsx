import { NavLink } from "react-router-dom";

export default function Navbar({ cartCount, wishlistCount }) {
  return (
    <header className="navbar">
      <div className="nav-inner">
        <NavLink to="/" className="brand">
          <span className="brand-mark">E</span>
          <span>ShopSpark</span>
        </NavLink>
        <nav>
          <NavLink to="/" end>Home</NavLink>
          <NavLink to="/products">Products</NavLink>
          <NavLink to="/wishlist">Wishlist <span className="cart-badge">{wishlistCount}</span></NavLink>\n          <NavLink to="/analytics">Analytics</NavLink>
          <NavLink to="/cart" className="cart-link">
            Cart <span className="cart-badge">{cartCount}</span>
          </NavLink>
        </nav>
      </div>
    </header>
  );
}
