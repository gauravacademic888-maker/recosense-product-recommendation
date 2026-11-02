"""Poora AI/ML logic yahin hai.

1. Content-Based Filtering : product ke text (name+category+description) se similarity (TF-IDF)
2. Collaborative Filtering : jo products same customers ne saath mein khareede (item-item cosine)
3. Hybrid                  : dono ka weighted mix  ->  alpha * CF + (1-alpha) * CB
4. Segmentation            : RFM (Recency, Frequency, Monetary) + KMeans
"""
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler


class Recommender:
    def __init__(self, products, purchases, alpha=0.5):
        self.products = products.reset_index(drop=True)
        self.purchases = purchases.copy()
        self.alpha = alpha
        self.pids = self.products["product_id"].tolist()
        self.pidx = {p: i for i, p in enumerate(self.pids)}
        self._build()

    # ---------- model banana ----------
    def _build(self):
        # Content-Based similarity
        text = (self.products["name"] + " " + self.products["category"] + " " +
                self.products["category"] + " " + self.products["description"])
        tfidf = TfidfVectorizer(stop_words="english").fit_transform(text)
        self.cb_sim = cosine_similarity(tfidf)

        # User-Item matrix (kis customer ne kaunsa product kitni baar khareeda)
        self.cids = sorted(self.purchases["customer_id"].unique())
        self.cidx = {c: i for i, c in enumerate(self.cids)}
        self.U = np.zeros((len(self.cids), len(self.pids)))
        for r in self.purchases.itertuples():
            self.U[self.cidx[r.customer_id], self.pidx[r.product_id]] += r.quantity

        # Collaborative (item-item) similarity
        self.cf_sim = cosine_similarity(self.U.T)
        np.fill_diagonal(self.cf_sim, 0)
        np.fill_diagonal(self.cb_sim, 0)

    def _sim(self, mode):
        if mode == "cf":
            return self.cf_sim
        if mode == "cb":
            return self.cb_sim
        return self.alpha * self.cf_sim + (1 - self.alpha) * self.cb_sim

    # ---------- recommendation ----------
    def recommend(self, customer_id, n=5, mode="hybrid"):
        if customer_id not in self.cidx:
            return self.popular(n)
        u = self.U[self.cidx[customer_id]]
        sim = self._sim(mode)
        scores = u @ sim                       # har product ka score
        scores[u > 0] = -1                     # jo pehle khareed chuka, wo na dikhao
        top = np.argsort(scores)[::-1][:n]
        out = []
        for j in top:
            contrib = u * sim[:, j]            # kis purane purchase ki wajah se ye aaya
            src = int(np.argmax(contrib))
            out.append({
                "product_id": self.pids[j],
                "name": self.products.loc[j, "name"],
                "category": self.products.loc[j, "category"],
                "price": int(self.products.loc[j, "price"]),
                "score": round(float(scores[j]), 2),
                "reason": f"Because you bought {self.products.loc[src, 'name']}",
            })
        return out

    def popular(self, n=5):
        """Naye customer (cold start) ke liye: sabse popular products."""
        pop = self.U.sum(axis=0)
        return [{"product_id": self.pids[j], "name": self.products.loc[j, "name"],
                 "category": self.products.loc[j, "category"],
                 "price": int(self.products.loc[j, "price"]), "score": 0,
                 "reason": "Popular with all customers"} for j in np.argsort(pop)[::-1][:n]]

    def target_customers(self, product_id, n=10):
        """Business ka sawal: 'Ye product kis customer ko dikhana chahiye?'"""
        j = self.pidx[product_id]
        scores = self.U @ self._sim("hybrid")[:, j]
        scores[self.U[:, j] > 0] = -1
        top = np.argsort(scores)[::-1][:n]
        return [(int(self.cids[i]), round(float(scores[i]), 2)) for i in top if scores[i] > 0]

    # ---------- customer segmentation ----------
    def segments(self, k=4):
        df = self.purchases.merge(self.products[["product_id", "price", "category"]], on="product_id")
        df["date"] = pd.to_datetime(df["date"])
        df["amount"] = df["price"] * df["quantity"]
        now = df["date"].max()
        rfm = df.groupby("customer_id").agg(
            recency=("date", lambda s: (now - s.max()).days),
            frequency=("date", "count"),
            monetary=("amount", "sum"),
            top_category=("category", lambda s: s.value_counts().index[0]),
        )
        X = StandardScaler().fit_transform(rfm[["recency", "frequency", "monetary"]])
        rfm["cluster"] = KMeans(n_clusters=k, n_init=10, random_state=42).fit_predict(X)

        m = rfm.groupby("cluster")[["recency", "frequency", "monetary"]].mean()
        labels = {}
        left = list(m.index)
        hv = m.loc[left, "monetary"].idxmax(); labels[hv] = "High-Value Customer"; left.remove(hv)
        ia = m.loc[left, "recency"].idxmax();  labels[ia] = "At-Risk / Inactive"; left.remove(ia)
        if left:
            lo = m.loc[left, "frequency"].idxmax(); labels[lo] = "Loyal - Likely to Buy Again"; left.remove(lo)
        for c in left:
            labels[c] = "Regular Customer"
        rfm["segment"] = rfm["cluster"].map(labels)
        rfm["monetary"] = rfm["monetary"].astype(int)
        return rfm.drop(columns="cluster")


# ---------- accuracy check (report ke Results chapter ke liye) ----------
def evaluate(products, purchases, k=5, alpha=0.5):
    """Har customer ka LAST purchase chhupa do, baaki se model train karo,
    aur dekho ki top-k recommendations mein wo chhupa hua product aaya ya nahi (Hit Rate@k)."""
    p = purchases.copy()
    p["date"] = pd.to_datetime(p["date"])
    p = p.sort_values("date")
    first_buy = p.drop_duplicates(["customer_id", "product_id"])
    n_items = first_buy.groupby("customer_id")["product_id"].count()
    eligible = n_items[n_items >= 4].index
    held = first_buy[first_buy.customer_id.isin(eligible)].groupby("customer_id").tail(1)
    held_set = set(zip(held.customer_id, held.product_id))
    train = p[[(c, pr) not in held_set for c, pr in zip(p.customer_id, p.product_id)]]
    rec = Recommender(products, train, alpha)
    res = {}
    for mode, label in [("cb", "Content-Based"), ("cf", "Collaborative"), ("hybrid", "Hybrid")]:
        hits = sum(any(r["product_id"] == pr for r in rec.recommend(c, k, mode)) for c, pr in held_set)
        res[label] = round(hits / len(held_set), 3)
    return res, len(held_set)
