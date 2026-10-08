import { useEffect, useState } from "react";
import ProductCard from "../components/ProductCard";
import { api } from "../services/api";

export default function Products({ categories, onAdd }) {
  const [products, setProducts] = useState([]);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("all");
  const [sort, setSort] = useState("name");
  const [minPrice, setMinPrice] = useState("");
  const [maxPrice, setMaxPrice] = useState("");
  const [inStock, setInStock] = useState(false);
  const [page, setPage] = useState(1);
  const [meta, setMeta] = useState({ count: 0, next: null, previous: null });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const timer = setTimeout(() => {
      setLoading(true);
      api.products({
        search,
        category,
        min_price: minPrice,
        max_price: maxPrice,
        in_stock: inStock ? "true" : "",
        ordering: sort,
        page,
      })
        .then((data) => {
          setProducts(data.results || []);
          setMeta({ count: data.count || 0, next: data.next, previous: data.previous });
        })
        .catch((err) => setError(err.message))
        .finally(() => setLoading(false));
    }, 250);

    return () => clearTimeout(timer);
  }, [search, category, sort, minPrice, maxPrice, inStock, page]);

  const updateFilter = (setter, value) => {
    setter(value);
    setPage(1);
  };

  return (
    <main className="section">
      <div className="section-heading">
        <div><p className="eyebrow">Store</p><h1>Products</h1></div>
        <span>{meta.count} products</span>
      </div>

      <div className="catalog-toolbar">
        <input
          value={search}
          onChange={(e) => updateFilter(setSearch, e.target.value)}
          placeholder="Search by product, SKU or category..."
        />
        <select value={category} onChange={(e) => updateFilter(setCategory, e.target.value)}>
          <option value="all">All categories</option>
          {categories.map((item) => <option key={item.id} value={item.id}>{item.name}</option>)}
        </select>
        <select value={sort} onChange={(e) => updateFilter(setSort, e.target.value)}>
          <option value="name">Name: A-Z</option>
          <option value="-name">Name: Z-A</option>
          <option value="price">Price: Low to High</option>
          <option value="-price">Price: High to Low</option>
          <option value="-created_at">Newest</option>
        </select>
        <input type="number" min="0" value={minPrice} onChange={(e) => updateFilter(setMinPrice, e.target.value)} placeholder="Min ₹" />
        <input type="number" min="0" value={maxPrice} onChange={(e) => updateFilter(setMaxPrice, e.target.value)} placeholder="Max ₹" />
        <label className="stock-filter"><input type="checkbox" checked={inStock} onChange={(e) => updateFilter(setInStock, e.target.checked)} /> In stock only</label>
      </div>

      {error && <div className="error">{error}</div>}
      {loading ? <div className="loading">Loading products...</div> : products.length ? (
        <>
          <div className="product-grid">{products.map((product) =>
            <ProductCard key={product.id} product={product} onAdd={onAdd} />
          )}</div>
          <div className="pagination">
            <button disabled={!meta.previous} onClick={() => setPage((value) => value - 1)}>← Previous</button>
            <span>Page {page}</span>
            <button disabled={!meta.next} onClick={() => setPage((value) => value + 1)}>Next →</button>
          </div>
        </>
      ) : <div className="empty-state"><h2>No products found</h2><p>Try another search, category or price range.</p></div>}
    </main>
  );
}
