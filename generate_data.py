"""
Generates a realistic synthetic dataset of SharkNinja product reviews.
Saves directly to sharkninja_reviews.csv and sharkninja_products.csv.

Run: python generate_data.py
"""

import csv
import random
from datetime import datetime, timedelta

random.seed(42)

# ── PRODUCTS ──────────────────────────────────────────────────────────
PRODUCTS = [
    {"asin": "SN001", "title": "Shark Navigator Lift-Away Upright Vacuum", "brand": "Shark", "category": "Shark", "price": "$149.99"},
    {"asin": "SN002", "title": "Shark Robot Vacuum IQ Series", "brand": "Shark", "category": "Shark", "price": "$349.99"},
    {"asin": "SN003", "title": "Shark Apex DuoClean Cordless Vacuum", "brand": "Shark", "category": "Shark", "price": "$279.99"},
    {"asin": "SN004", "title": "Shark Stratos Upright Vacuum with DuoClean", "brand": "Shark", "category": "Shark", "price": "$329.99"},
    {"asin": "NJ001", "title": "Ninja Air Fryer Pro 4-Quart", "brand": "Ninja", "category": "Ninja", "price": "$99.99"},
    {"asin": "NJ002", "title": "Ninja Foodi 9-in-1 Pressure Cooker & Air Fryer", "brand": "Ninja", "category": "Ninja", "price": "$199.99"},
    {"asin": "NJ003", "title": "Ninja Professional Blender 1000W", "brand": "Ninja", "category": "Ninja", "price": "$79.99"},
    {"asin": "NJ004", "title": "Ninja Creami Ice Cream Maker", "brand": "Ninja", "category": "Ninja", "price": "$199.99"},
    {"asin": "NJ005", "title": "Ninja Speedi Rapid Cooker & Air Fryer", "brand": "Ninja", "category": "Ninja", "price": "$159.99"},
]

# ── REVIEW TEMPLATES ──────────────────────────────────────────────────
REVIEWS_BY_RATING = {
    5: [
        ("Best vacuum I've ever owned", "This {product} completely changed how I clean my house. Picks up pet hair effortlessly and the suction is incredible. Worth every penny."),
        ("Absolutely love it", "Finally bought the {product} after months of research and I'm not disappointed. Easy to assemble, powerful suction, and very maneuverable. Highly recommend."),
        ("Game changer", "The {product} is outstanding. My floors have never been cleaner. The attachments are very useful and it's surprisingly lightweight."),
        ("Exceeded expectations", "I was skeptical at first but the {product} has been phenomenal. No loss of suction, easy to empty, and works great on both carpet and hardwood."),
        ("Perfect purchase", "The {product} is exactly what I needed. Quiet enough to use while my baby sleeps, powerful enough to handle dog hair everywhere. Zero complaints."),
        ("Love this thing", "Got the {product} as a gift and now I vacuum every day. It's that satisfying to use. Filters are easy to clean and battery lasts a long time."),
    ],
    4: [
        ("Great product, minor issues", "The {product} works really well overall. Suction is strong and it's easy to use. Docking a star only because the dustbin could be larger."),
        ("Very happy with purchase", "Happy with my {product}. Does exactly what it promises. The cord is a bit short for my large living room but otherwise no complaints."),
        ("Solid performer", "The {product} is a reliable machine. Good suction power, easy to maintain. The instructions could be clearer but once you figure it out it works great."),
        ("Good value", "For the price the {product} delivers solid performance. Not perfect but definitely gets the job done. Would recommend to friends and family."),
        ("Works as described", "The {product} does what it says. Good suction on carpet, handles pet hair well. Minor complaint is that it's a bit loud but nothing terrible."),
    ],
    3: [
        ("Decent but not great", "The {product} is okay for the price. It works but I expected more suction power. It struggles with larger debris. Average product overall."),
        ("Mixed feelings", "My {product} has been fine for light cleaning but struggles with heavy messes. Also had to contact customer service once which wasn't ideal."),
        ("Average product", "Nothing wrong with the {product} but nothing special either. Does the job but so would cheaper options. The quality feels a bit plastic-y."),
        ("It does the job", "The {product} cleans my floors adequately. The filters clog faster than I expected and I've already had to replace one after 6 months of use."),
        ("Disappointed slightly", "Expected more from the {product} based on reviews. It works but the battery life is not as advertised and the charger is slow."),
    ],
    2: [
        ("Stopped working after 3 months", "My {product} worked fine at first but stopped working properly after about 3 months. The suction dropped dramatically and customer service was unhelpful."),
        ("Quality issues", "The {product} has good suction but the build quality is poor. The attachment clips broke within weeks and replacement parts are expensive."),
        ("Not worth the price", "For the amount I paid for this {product}, I expected much better. The motor is loud, it overheats, and the warranty process was a nightmare."),
        ("Disappointed", "The {product} started making a strange noise after 2 months. Build quality is not great. Would not buy again."),
    ],
    1: [
        ("Complete waste of money", "The {product} broke after 6 weeks. Called customer support and they were useless. Do not buy this product."),
        ("Terrible quality control", "My {product} arrived with a cracked part and after 3 weeks the motor started burning smell. Returned immediately."),
        ("Don't buy this", "The {product} is a huge disappointment. Weak suction from day one, loud, and the dustbin releases dust back into the air when you empty it."),
        ("Returned immediately", "The {product} didn't work out of the box. Had to return it. Very poor quality control from Shark/Ninja."),
    ],
}

# ── DISTRIBUTION (realistic — skewed positive) ────────────────────────
RATING_WEIGHTS = {5: 45, 4: 25, 3: 15, 2: 9, 1: 6}

def random_date(start_year=2014, end_year=2023):
    start = datetime(start_year, 1, 1)
    end   = datetime(end_year, 12, 31)
    delta = end - start
    return (start + timedelta(days=random.randint(0, delta.days))).strftime("%Y-%m-%d")

# ── GENERATE ──────────────────────────────────────────────────────────
reviews     = []
review_id   = 1
ratings_pop = [r for r, w in RATING_WEIGHTS.items() for _ in range(w)]

for product in PRODUCTS:
    n_reviews = random.randint(50, 80)
    for _ in range(n_reviews):
        rating  = random.choice(ratings_pop)
        tmpl    = random.choice(REVIEWS_BY_RATING[rating])
        title   = tmpl[0]
        text    = tmpl[1].format(product=product["title"].split()[0] + " " + product["title"].split()[1])
        date    = random_date()
        helpful = random.choices([0, 1, 2, 3, 5, 8, 12], weights=[40,20,15,10,8,5,2])[0]

        reviews.append({
            "asin"    : product["asin"],
            "rating"  : rating,
            "title"   : title,
            "text"    : text,
            "helpful" : helpful,
            "verified": random.random() > 0.15,
            "date"    : date,
            "year"    : int(date[:4]),
        })
        review_id += 1

random.shuffle(reviews)

# ── SAVE REVIEWS ──────────────────────────────────────────────────────
with open("sharkninja_reviews.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["asin","rating","title","text","helpful","verified","date","year"])
    writer.writeheader()
    writer.writerows(reviews)

# ── SAVE PRODUCTS ─────────────────────────────────────────────────────
with open("sharkninja_products.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["asin","title","brand","category","price","avg_rating","rating_count"])
    writer.writeheader()
    for p in PRODUCTS:
        p_reviews = [r for r in reviews if r["asin"] == p["asin"]]
        avg = round(sum(r["rating"] for r in p_reviews) / len(p_reviews), 2)
        writer.writerow({**p, "avg_rating": avg, "rating_count": len(p_reviews)})

print(f"Done. Generated {len(reviews)} reviews across {len(PRODUCTS)} products.")
print(f"Date range: 2014 - 2023")
print(f"Saved → sharkninja_reviews.csv")
print(f"Saved → sharkninja_products.csv")
print(f"\nRun analyze.py next.")
