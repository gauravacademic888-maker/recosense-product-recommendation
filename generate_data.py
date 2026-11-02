"""Step 1: Sample data banata hai (internet / Kaggle ki zarurat nahi).
Run: python generate_data.py
Output: data/products.csv, data/customers.csv, data/purchases.csv

Apni real company ka data use karna ho to bas in 3 CSV files ko
same columns ke saath replace kar do."""
import random
from datetime import date, timedelta
import pandas as pd

random.seed(42)

CATALOG = {
    "Sports": [("Running Shoes", 2999, "running jogging shoes cushioned sports footwear"),
               ("Sports Socks", 299, "running socks breathable sports cotton"),
               ("Running Watch", 4999, "gps smartwatch running fitness tracker sports"),
               ("Gym T-Shirt", 599, "gym workout dry fit tshirt sports training"),
               ("Yoga Mat", 899, "yoga exercise mat fitness workout home"),
               ("Dumbbell Set", 2499, "dumbbell weights strength gym workout fitness"),
               ("Football", 799, "football outdoor sports ball team game"),
               ("Cricket Bat", 1999, "cricket bat willow sports outdoor game")],
    "Electronics": [("Wireless Earbuds", 1999, "bluetooth earbuds wireless audio music electronics"),
                    ("Power Bank", 1299, "power bank charging battery portable electronics"),
                    ("Smart Watch", 3999, "smartwatch bluetooth fitness notifications electronics"),
                    ("Bluetooth Speaker", 1799, "speaker bluetooth portable music audio electronics"),
                    ("USB Charger", 499, "fast charger usb type c mobile electronics"),
                    ("Laptop Bag", 999, "laptop bag backpack office travel electronics"),
                    ("Gaming Mouse", 1199, "gaming mouse rgb usb computer electronics"),
                    ("Mechanical Keyboard", 2799, "keyboard mechanical gaming typing computer electronics")],
    "Fashion": [("Formal Shirt", 1299, "formal shirt office cotton men fashion clothing"),
                ("Slim Fit Jeans", 1599, "jeans denim slim fit casual fashion clothing"),
                ("Winter Jacket", 2999, "winter jacket warm wool fashion clothing"),
                ("Leather Belt", 699, "leather belt formal fashion accessory"),
                ("Casual Sneakers", 1999, "sneakers casual shoes fashion footwear"),
                ("Sunglasses", 899, "sunglasses uv protection fashion accessory"),
                ("Woolen Scarf", 499, "scarf woolen winter warm fashion accessory"),
                ("Printed Tshirt", 499, "tshirt printed cotton casual fashion clothing")],
    "Home": [("Table Lamp", 899, "lamp led study desk home decor lighting"),
             ("Cotton Bedsheet", 1199, "bedsheet cotton bedroom home soft"),
             ("Coffee Mug Set", 599, "mug ceramic coffee tea kitchen home"),
             ("Wall Clock", 699, "clock wall decor home living room"),
             ("Storage Box", 499, "storage organizer box home room"),
             ("Air Fryer", 4499, "air fryer kitchen cooking appliance home"),
             ("Curtains", 999, "curtains window decor home bedroom"),
             ("Cushion Cover Set", 399, "cushion cover sofa decor home living room")],
    "Beauty": [("Face Wash", 249, "face wash cleanser skin care beauty"),
               ("Moisturizer", 399, "moisturizer cream skin care hydration beauty"),
               ("Sunscreen", 449, "sunscreen spf protection skin care beauty"),
               ("Hair Oil", 299, "hair oil nourishing hair care beauty"),
               ("Perfume", 1299, "perfume fragrance spray beauty"),
               ("Lipstick", 499, "lipstick makeup color beauty"),
               ("Beard Trimmer", 1499, "trimmer beard grooming electric beauty"),
               ("Shampoo", 349, "shampoo hair care cleansing beauty")],
    "Books": [("Python Programming Book", 599, "python programming coding book learning"),
              ("Data Science Handbook", 799, "data science machine learning book learning"),
              ("Self Help Bestseller", 349, "motivation habits self help book reading"),
              ("Mystery Novel", 299, "mystery thriller novel fiction book reading"),
              ("Study Notebook Pack", 199, "notebook study stationery pack school college"),
              ("Gel Pen Set", 149, "pen gel stationery writing college"),
              ("Mathematics Guide", 499, "mathematics exam guide study book learning"),
              ("Business Biography", 449, "business biography entrepreneur book reading")],
}

FIRST = ["Aarav", "Vivaan", "Aditya", "Rohan", "Karan", "Ankit", "Rahul", "Neha", "Priya", "Sneha",
         "Pooja", "Riya", "Anjali", "Kavya", "Isha", "Manish", "Deepak", "Suresh", "Nikhil", "Tanvi"]
LAST = ["Sharma", "Verma", "Gupta", "Singh", "Yadav", "Mishra", "Jain", "Kapoor", "Mehta", "Chauhan"]
CITIES = ["Delhi", "Noida", "Ghaziabad", "Greater Noida", "Gurugram", "Lucknow", "Meerut"]

rows = []
pid = 1
for cat, items in CATALOG.items():
    for name, price, desc in items:
        rows.append((pid, name, cat, price, desc)); pid += 1
products = pd.DataFrame(rows, columns=["product_id", "name", "category", "price", "description"])

cats = list(CATALOG)
customers, purchases = [], []
today = date(2026, 10, 15)
for cid in range(1, 301):
    customers.append((cid, f"{random.choice(FIRST)} {random.choice(LAST)}", random.choice(CITIES)))
    favs = random.sample(cats, random.choice([1, 2]))
    # customer type: kuch log zyada kharidte hain, kuch purane inactive hain
    kind = random.choices(["heavy", "normal", "light", "inactive"], [0.15, 0.40, 0.30, 0.15])[0]
    n = {"heavy": random.randint(14, 24), "normal": random.randint(7, 12),
         "light": random.randint(3, 6), "inactive": random.randint(3, 7)}[kind]
    span = (330, 365) if kind != "inactive" else (150, 365)
    for _ in range(n):
        cat = random.choice(favs) if random.random() < 0.8 else random.choice(cats)
        p = products[products.category == cat].sample(1).iloc[0]
        d = today - timedelta(days=random.randint(span[0] if kind == "inactive" else 1, span[1]))
        if kind != "inactive" and random.random() < 0.5:
            d = today - timedelta(days=random.randint(1, 120))
        purchases.append((cid, int(p.product_id), d.isoformat(), random.choice([1, 1, 1, 2])))

customers = pd.DataFrame(customers, columns=["customer_id", "name", "city"])
purchases = pd.DataFrame(purchases, columns=["customer_id", "product_id", "date", "quantity"])
products.to_csv("data/products.csv", index=False)
customers.to_csv("data/customers.csv", index=False)
purchases.to_csv("data/purchases.csv", index=False)
print(f"Done: {len(products)} products, {len(customers)} customers, {len(purchases)} purchases")
