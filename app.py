"""Step 2: Website chalane ke liye.  Run: python app.py   ->  browser mein http://127.0.0.1:5000"""
import pandas as pd
from flask import Flask, jsonify, render_template, request, abort
from recommender import Recommender, evaluate

app = Flask(__name__)

products = pd.read_csv("data/products.csv")
customers = pd.read_csv("data/customers.csv").set_index("customer_id")
purchases = pd.read_csv("data/purchases.csv")

rec = Recommender(products, purchases, alpha=0.5)
seg = rec.segments()
scores, n_tested = evaluate(products, purchases)

SEGMENT_NOTE = {
    "High-Value Customer": "Premium products aur early-access offers dikhao",
    "Loyal - Likely to Buy Again": "Cross-sell karo: related products aur combo offers",
    "Regular Customer": "Popular + discounted products se engagement badhao",
    "At-Risk / Inactive": "Win-back offer / reminder email bhejo",
}


@app.route("/")
def dashboard():
    q = request.args.get("q", "").strip().lower()
    seg_filter = request.args.get("segment", "")
    df = seg.join(customers)
    counts = seg["segment"].value_counts()
    revenue = int(seg["monetary"].sum())
    rows = df
    if seg_filter:
        rows = rows[rows["segment"] == seg_filter]
    if q:
        rows = rows[rows["name"].str.lower().str.contains(q) | rows.index.astype(str).str.contains(q)]
    rows = rows.sort_values("monetary", ascending=False).head(25)
    return render_template(
        "index.html", n_customers=len(seg), n_products=len(products), n_orders=len(purchases),
        revenue=revenue, counts=counts.to_dict(), max_count=int(counts.max()), notes=SEGMENT_NOTE,
        rows=rows.reset_index().to_dict("records"), q=q, seg_filter=seg_filter,
        scores=scores, n_tested=n_tested)


@app.route("/customer/<int:cid>")
def customer(cid):
    if cid not in seg.index:
        abort(404)
    c = seg.loc[cid]
    hist = (purchases[purchases.customer_id == cid]
            .merge(products[["product_id", "name", "category", "price"]], on="product_id")
            .sort_values("date", ascending=False))
    return render_template(
        "customer.html", cid=cid, info=customers.loc[cid], c=c, note=SEGMENT_NOTE[c["segment"]],
        history=hist.head(12).to_dict("records"), recs=rec.recommend(cid, 5))


@app.route("/product/<int:pid>")
def product(pid):
    p = products[products.product_id == pid]
    if p.empty:
        abort(404)
    targets = [{"cid": cid, "score": s, "name": customers.loc[cid, "name"], "segment": seg.loc[cid, "segment"]}
               for cid, s in rec.target_customers(pid, 10)]
    return render_template("product.html", p=p.iloc[0], targets=targets,
                           all_products=products.to_dict("records"))


@app.route("/api/recommend/<int:cid>")
def api_recommend(cid):
    """Company apni website se is URL ko call karke recommendations le sakti hai (JSON)."""
    n = request.args.get("n", 5, type=int)
    return jsonify({"customer_id": cid,
                    "segment": seg.loc[cid, "segment"] if cid in seg.index else "New Customer",
                    "recommendations": rec.recommend(cid, n)})


if __name__ == "__main__":
    app.run(debug=False)
