import { useMemo, useState } from "react";
import { Link } from "react-router-dom";

const coupons = { SHOP10: 0.10, SAVE500: 0.05 };

export default function Cart({ cart, onChangeQuantity, onRemove }) {
  const [coupon, setCoupon] = useState("");
  const [appliedCoupon, setAppliedCoupon] = useState("");
  const [couponError, setCouponError] = useState("");
  const subtotal = useMemo(() => cart.reduce((sum, item) => sum + Number(item.price) * item.quantity, 0), [cart]);
  const discountRate = coupons[appliedCoupon] || 0;
  const discount = subtotal * discountRate;
  const total = subtotal - discount;

  const applyCoupon = () => {
    const code = coupon.trim().toUpperCase();
    if (!coupons[code]) { setCouponError("Invalid coupon. Try SHOP10 or SAVE500."); setAppliedCoupon(""); return; }
    setAppliedCoupon(code);
    setCouponError("");
  };

  return (
    <main className="section">
      <div className="section-heading"><div><p className="eyebrow">Shopping</p><h1>Your cart</h1></div></div>
      {!cart.length ? (
        <div className="empty-state"><h2>Your cart is empty</h2><p>Add a few products to get started.</p><Link className="primary-button" to="/products">Browse products</Link></div>
      ) : (
        <div className="cart-layout">
          <div className="cart-items">
            {cart.map((item) => (
              <article className="cart-item" key={item.id}>
                <Link to={`/products/${item.id}`}><img className="cart-thumb" src={item.image_url} alt={item.name} /></Link>
                <div className="cart-info"><h3>{item.name}</h3><span>₹{Number(item.price).toLocaleString("en-IN")} each</span></div>
                <div className="quantity"><button onClick={() => onChangeQuantity(item.id, item.quantity - 1)}>−</button><strong>{item.quantity}</strong><button disabled={item.quantity >= item.stock_quantity} onClick={() => onChangeQuantity(item.id, item.quantity + 1)}>+</button></div>
                <strong>₹{(Number(item.price) * item.quantity).toLocaleString("en-IN")}</strong>
                <button className="remove-button" onClick={() => onRemove(item.id)}>Remove</button>
              </article>
            ))}
            <Link className="secondary-button" to="/products">← Continue shopping</Link>
          </div>
          <aside className="summary">
            <h2>Order summary</h2>
            <div><span>Subtotal</span><strong>₹{subtotal.toLocaleString("en-IN", { maximumFractionDigits: 2 })}</strong></div>
            <div className="coupon-box"><input value={coupon} onChange={(e) => setCoupon(e.target.value)} placeholder="Coupon code" /><button onClick={applyCoupon}>Apply</button></div>
            {couponError && <p className="coupon-error">{couponError}</p>}
            {appliedCoupon && <div><span>Discount ({appliedCoupon})</span><strong>-₹{discount.toLocaleString("en-IN", { maximumFractionDigits: 2 })}</strong></div>}
            <div><span>Shipping</span><strong>Free</strong></div>
            <hr />
            <div className="total"><span>Total</span><strong>₹{total.toLocaleString("en-IN", { maximumFractionDigits: 2 })}</strong></div>
            <button className="checkout-button" disabled>Checkout — Phase 14</button>
          </aside>
        </div>
      )}
    </main>
  );
}
