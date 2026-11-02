# RecoSense - AI Product Recommendation & Customer Preference System
BCA Vth Sem Project | Python + Flask + Pandas + Scikit-learn

## Laptop pe chalane ke steps (Windows)
1. Python 3.10+ install hona chahiye (python.org). Install karte time "Add Python to PATH" tick karo.
2. Is poore folder ko Desktop pe rakho. Folder ke address bar mein `cmd` likh ke Enter dabao.
3. Libraries install karo (sirf ek baar, internet chahiye):
       pip install -r requirements.txt
4. (Optional) Naya sample data banana ho to:
       python generate_data.py
   Data pehle se `data/` folder mein rakha hai, to ye step skip kar sakte ho.
5. Website start karo:
       python app.py
6. Browser kholo: http://127.0.0.1:5000
   Demo ke time internet ki zarurat NAHI hai.

## Files kya karti hain
| File | Kaam |
|---|---|
| generate_data.py | Sample products / customers / purchases CSV banata hai |
| recommender.py | Poora ML: Content-Based + Collaborative + Hybrid + RFM Segmentation + accuracy test |
| app.py | Flask website (dashboard, customer page, product targeting, JSON API) |
| templates/ | HTML pages |
| data/ | 3 CSV files (products, customers, purchases) |

## ML kaise kaam karta hai (viva ke liye)
1. Content-Based: product ke naam+category+description ko TF-IDF se numbers mein badla, cosine similarity se similar products nikale.
2. Collaborative: jo products same customers ne saath mein khareede, wo similar maane (item-item cosine similarity).
3. Hybrid: 50% Collaborative + 50% Content-Based mix. Iska score `alpha` se control hota hai (`recommender.py`).
4. Segmentation: har customer ke Recency, Frequency, Monetary (RFM) nikale, K-Means (k=4) se 4 groups: High-Value, Loyal, Regular, At-Risk.
5. Accuracy: har customer ka last purchase chhupa ke test kiya (Hit Rate@5). Dashboard ke neeche table dikhti hai.
6. Cold start: bilkul naye customer ko popular products dikhte hain.

## Demo flow (5 minute)
1. Dashboard dikhao: stats + segments + accuracy table.
2. "High-Value Customer" bar pe click karo, kisi customer pe "View recommendations".
3. "Because you bought ..." wali line samjhao (explainable recommendation).
4. Top menu "Product Targeting": product chuno, dikhao kis customer ko recommend karna hai.
5. Browser mein `/api/recommend/5` kholo: dikhao ki koi bhi company apni website se is API ko call kar sakti hai.

## Apna real data lagana ho to
`data/` ki 3 CSV files same columns ke saath replace karo:
- products.csv : product_id, name, category, price, description
- customers.csv : customer_id, name, city
- purchases.csv : customer_id, product_id, date (YYYY-MM-DD), quantity
Phir `python app.py` dobara chalao.

## Common errors
- `'python' is not recognized` -> Python install karte time PATH tick nahi hua. Dobara install karo.
- `pip` nahi chal raha -> `python -m pip install -r requirements.txt`
- Port busy -> `app.run(port=5001)` kar do `app.py` ke last line mein.
