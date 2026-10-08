import { NavLink } from "react-router-dom";

export default function Navbar({ cartCount }) {
  return (
    <header className="navbar">
      <div className="nav-inner">
        <NavLink to="/" className="brand"><span className="brand-mark">S</span><span>ShopSpark</span></NavLink>
        <nav>
          <NavLink to="/" end>Home</NavLink>
          <NavLink to="/products">Shop</NavLink>
          <NavLink to="/analytics">Insights</NavLink>
          <NavLink to="/cart" className="cart-link">Cart <span className="cart-badge">{cartCount}</span></NavLink>
        </nav>
      </div>
    </header>
  );
}