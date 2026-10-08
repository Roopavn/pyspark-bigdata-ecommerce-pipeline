import { Link } from "react-router-dom";

export default function Cart({ cart, onChangeQuantity, onRemove }) {
  const total = cart.reduce((sum, item) => sum + Number(item.price) * item.quantity, 0);

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
                <div className="cart-thumb">{item.category_name || "Item"}</div>
                <div className="cart-info"><h3>{item.name}</h3><span>₹{Number(item.price).toLocaleString()} each</span></div>
                <div className="quantity">
                  <button onClick={() => onChangeQuantity(item.id, item.quantity - 1)}>−</button>
                  <strong>{item.quantity}</strong>
                  <button onClick={() => onChangeQuantity(item.id, item.quantity + 1)}>+</button>
                </div>
                <strong>₹{(Number(item.price) * item.quantity).toLocaleString()}</strong>
                <button className="remove-button" onClick={() => onRemove(item.id)}>Remove</button>
              </article>
            ))}
          </div>
          <aside className="summary">
            <h2>Order summary</h2>
            <div><span>Subtotal</span><strong>₹{total.toLocaleString()}</strong></div>
            <div><span>Shipping</span><strong>Free</strong></div>
            <hr />
            <div className="total"><span>Total</span><strong>₹{total.toLocaleString()}</strong></div>
            <button className="checkout-button" disabled>Checkout — coming next</button>
          </aside>
        </div>
      )}
    </main>
  );
}
