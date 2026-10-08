import { Link } from "react-router-dom";
import { imageForProduct } from "../services/productImages";

export default function Cart({ cart, onChangeQuantity, onRemove }) {
  const total = cart.reduce((sum, item) => sum + Number(item.price) * item.quantity, 0);
  return (
    <main className="section">
      <div className="section-heading"><div><p className="eyebrow">Your shopping bag</p><h1>Cart</h1></div></div>
      {!cart.length ? <div className="empty-state"><h2>Your cart is empty</h2><p>Discover something you will love.</p><Link className="primary-button" to="/products">Continue shopping</Link></div> :
      <div className="cart-layout"><div className="cart-items">{cart.map((item) => <article className="cart-item" key={item.id}><img className="cart-thumb" src={imageForProduct(item)} alt={item.name} /><div className="cart-info"><h3>{item.name}</h3><span>₹{Number(item.price).toLocaleString("en-IN")} each</span></div><div className="quantity"><button onClick={() => onChangeQuantity(item.id, item.quantity - 1)}>−</button><strong>{item.quantity}</strong><button onClick={() => onChangeQuantity(item.id, item.quantity + 1)}>+</button></div><strong>₹{(Number(item.price) * item.quantity).toLocaleString("en-IN")}</strong><button className="remove-button" onClick={() => onRemove(item.id)}>Remove</button></article>)}</div>
      <aside className="summary"><h2>Order summary</h2><div><span>Subtotal</span><strong>₹{total.toLocaleString("en-IN")}</strong></div><div><span>Shipping</span><strong>Free</strong></div><hr/><div className="total"><span>Total</span><strong>₹{total.toLocaleString("en-IN")}</strong></div><button className="checkout-button" disabled>Checkout — coming next</button></aside></div>}
    </main>
  );
}