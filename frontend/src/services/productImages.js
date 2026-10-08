const images = {
  mobile: "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=900&q=85",
  laptop: "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=900&q=85",
  audio: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=900&q=85",
  home: "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?auto=format&fit=crop&w=900&q=85",
  fashion: "https://images.unsplash.com/photo-1445205170230-053b83016050?auto=format&fit=crop&w=900&q=85",
  default: "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?auto=format&fit=crop&w=900&q=85",
};

export function imageForProduct(product = {}) {
  const value = `${product.category_name || ""} ${product.name || ""}`.toLowerCase();
  if (value.includes("mobile") || value.includes("phone")) return images.mobile;
  if (value.includes("laptop") || value.includes("computer")) return images.laptop;
  if (value.includes("audio") || value.includes("headphone") || value.includes("earbud")) return images.audio;
  if (value.includes("home") || value.includes("furniture")) return images.home;
  if (value.includes("fashion") || value.includes("cloth") || value.includes("shoe")) return images.fashion;
  return images.default;
}
