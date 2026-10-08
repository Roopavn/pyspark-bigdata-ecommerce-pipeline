import { useEffect, useState } from "react";
import { BrowserRouter, Route, Routes, useParams } from "react-router-dom";
import Navbar from "./components/Navbar";
import { api } from "./services/api";
import Home from "./pages/Home";
import Products from "./pages/Products";
import ProductDetails from "./pages/ProductDetails";
import Cart from "./pages/Cart";
import Analytics from "./pages/Analytics";

function listData(value) {
  return Array.isArray(value) ? value : value?.results || [];
}

export default function App() {
  const [categories, setCategories] = useState([]);
  const [cart, setCart] = useState(() => JSON.parse(localStorage.getItem("shop-spark-cart") || "[]"));
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    api.categories()
      .then((categoryData) => setCategories(listData(categoryData)))
      .catch((err) => setError(err.message || "Unable to load store data"))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    localStorage.setItem("shop-spark-cart", JSON.stringify(cart));
  }, [cart]);

  const addToCart = (product) => {
    setCart((current) => {
      const existing = current.find((item) => item.id === product.id);
      if (existing) return current.map((item) => item.id === product.id ? { ...item, quantity: Math.min(item.quantity + 1, product.stock_quantity) } : item);
      return [...current, { ...product, quantity: 1 }];
    });
  };

  const changeQuantity = (id, quantity) => {
    if (quantity <= 0) return setCart((current) => current.filter((item) => item.id !== id));
    setCart((current) => current.map((item) => item.id === id ? { ...item, quantity: Math.min(quantity, item.stock_quantity) } : item));
  };

  const removeFromCart = (id) => setCart((current) => current.filter((item) => item.id !== id));

  return (
    <BrowserRouter>
      <Navbar cartCount={cart.reduce((sum, item) => sum + item.quantity, 0)} />
      {error && <div className="global-error">{error}</div>}
      {loading ? <div className="loading">Loading store...</div> : (
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/products" element={<Products categories={categories} onAdd={addToCart} />} />
          <Route path="/products/:id" element={<ProductRoute onAdd={addToCart} />} />
          <Route path="/cart" element={<Cart cart={cart} onChangeQuantity={changeQuantity} onRemove={removeFromCart} />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="*" element={<Home />} />
        </Routes>
      )}
    </BrowserRouter>
  );
}

function ProductRoute({ onAdd }) {
  return <ProductDetails onAdd={onAdd} />;
}
