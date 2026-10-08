import { useMemo, useState } from "react";
import ProductCard from "../components/ProductCard";

export default function Products({ products, categories, onAdd }) {
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("all");

  const filtered = useMemo(() => products.filter((product) => {
    const matchesSearch = product.name.toLowerCase().includes(search.toLowerCase()) ||
      product.sku.toLowerCase().includes(search.toLowerCase());
    const matchesCategory = category === "all" || String(product.category) === category;
    return matchesSearch && matchesCategory && product.is_active;
  }), [products, search, category]);

  return (
    <main className="section">
      <div className="section-heading">
        <div><p className="eyebrow">Store</p><h1>Products</h1></div>
        <span>{filtered.length} products</span>
      </div>
      <div className="filters">
        <input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="Search products or SKU..." />
        <select value={category} onChange={(e) => setCategory(e.target.value)}>
          <option value="all">All categories</option>
          {categories.map((item) => <option key={item.id} value={item.id}>{item.name}</option>)}
        </select>
      </div>
      {filtered.length ? (
        <div className="product-grid">{filtered.map((product) =>
          <ProductCard key={product.id} product={product} onAdd={onAdd} />
        )}</div>
      ) : <div className="empty-state"><h2>No products found</h2><p>Try another search or category.</p></div>}
    </main>
  );
}
