"""
STEP 2 — Analyze SharkNinja reviews with Claude API
Reads sharkninja_reviews.csv, sends batches to Claude, saves results.

Run: python step2_analyze.py
Output: analysis_results.json
"""

import os
import json
import time
import pandas as pd
import anthropic

# ── CONFIG ────────────────────────────────────────────────────────────
API_KEY       = os.environ.get("ANTHROPIC_API_KEY", "your-api-key-here")
BATCH_SIZE    = 20       # reviews per Claude call (keep small to control cost)
MAX_REVIEWS   = 500      # total reviews to analyze (increase once working)
OUTPUT_FILE   = "analysis_results.json"

client = anthropic.Anthropic(api_key=API_KEY)

# ── LOAD DATA ─────────────────────────────────────────────────────────
print("Loading reviews...")
reviews_df = pd.read_csv("sharkninja_reviews.csv")
products_df = pd.read_csv("sharkninja_products.csv")

# Merge to get product title and category with each review
df = reviews_df.merge(
    products_df[["asin", "title", "category"]],
    on="asin", how="left"
)

# Focus on text reviews only, cap at MAX_REVIEWS
df = df[df["text"].str.len() > 20].head(MAX_REVIEWS)
print(f"Analyzing {len(df)} reviews across {df['asin'].nunique()} products...")

# ── CLAUDE PROMPT ─────────────────────────────────────────────────────
SYSTEM_PROMPT = """
You are a product analytics AI for a consumer electronics company.
You analyze batches of Amazon customer reviews and extract structured insights.

Always respond with ONLY valid JSON — no explanation, no markdown, no preamble.
""".strip()

def build_prompt(batch_df):
    reviews_text = ""
    for _, row in batch_df.iterrows():
        reviews_text += f"""
---
Product: {row.get('title', 'Unknown')}
Rating: {row.get('rating', 'N/A')}/5
Review: {str(row.get('text', ''))[:400]}
""".strip() + "\n"

    return f"""
Analyze these {len(batch_df)} Amazon customer reviews for SharkNinja products.

{reviews_text}

Return a JSON object with this exact structure:
{{
  "overall_sentiment": <float between -1.0 (very negative) and 1.0 (very positive)>,
  "avg_rating": <float>,
  "top_complaints": [
    {{"issue": "<issue name>", "count": <int>, "example": "<short quote from review>"}}
  ],
  "top_praises": [
    {{"aspect": "<aspect name>", "count": <int>, "example": "<short quote from review>"}}
  ],
  "feature_requests": [
    {{"feature": "<feature name>", "count": <int>}}
  ],
  "summary": "<2-3 sentence executive summary a product manager can act on>"
}}

Rules:
- top_complaints: list up to 5 most common complaints
- top_praises: list up to 5 most praised aspects
- feature_requests: list up to 5 most requested improvements
- Keep all text fields under 100 characters
- Return ONLY the JSON object, nothing else
""".strip()

# ── PROCESS IN BATCHES ────────────────────────────────────────────────
all_results = []
batches = [df.iloc[i:i+BATCH_SIZE] for i in range(0, len(df), BATCH_SIZE)]

print(f"\nSending {len(batches)} batches to Claude API...")
print("-" * 50)

for i, batch in enumerate(batches):
    print(f"Batch {i+1}/{len(batches)} ({len(batch)} reviews)...", end=" ", flush=True)

    try:
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": build_prompt(batch)}]
        )

        raw = response.content[0].text.strip()

        # Strip markdown fences if Claude adds them
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        parsed = json.loads(raw)

        # Attach metadata
        parsed["batch_index"]    = i
        parsed["product_asins"]  = batch["asin"].unique().tolist()
        parsed["review_count"]   = len(batch)
        parsed["category"]       = batch["category"].mode()[0] if "category" in batch else "Unknown"

        all_results.append(parsed)
        print(f"✓ sentiment={parsed['overall_sentiment']:.2f}")

    except json.JSONDecodeError as e:
        print(f"✗ JSON parse error: {e}")
        all_results.append({"batch_index": i, "error": str(e), "raw": raw[:200]})

    except Exception as e:
        print(f"✗ Error: {e}")
        all_results.append({"batch_index": i, "error": str(e)})

    # Be polite to the API
    time.sleep(0.5)

# ── AGGREGATE RESULTS ─────────────────────────────────────────────────
print("\n" + "=" * 50)
print("Aggregating results...")

successful = [r for r in all_results if "error" not in r]

# Flatten complaints across all batches
all_complaints = {}
all_praises    = {}
all_requests   = {}

for r in successful:
    for c in r.get("top_complaints", []):
        key = c["issue"].lower()
        all_complaints[key] = all_complaints.get(key, 0) + c.get("count", 1)

    for p in r.get("top_praises", []):
        key = p["aspect"].lower()
        all_praises[key] = all_praises.get(key, 0) + p.get("count", 1)

    for f in r.get("feature_requests", []):
        key = f["feature"].lower()
        all_requests[key] = all_requests.get(key, 0) + f.get("count", 1)

aggregate = {
    "total_reviews_analyzed" : len(df),
    "total_batches"          : len(batches),
    "successful_batches"     : len(successful),
    "avg_sentiment"          : round(sum(r["overall_sentiment"] for r in successful) / max(len(successful), 1), 3),
    "avg_rating"             : round(df["rating"].mean(), 2),
    "top_complaints"         : sorted(all_complaints.items(), key=lambda x: -x[1])[:10],
    "top_praises"            : sorted(all_praises.items(),    key=lambda x: -x[1])[:10],
    "feature_requests"       : sorted(all_requests.items(),   key=lambda x: -x[1])[:10],
    "batch_results"          : all_results,
}

with open(OUTPUT_FILE, "w") as f:
    json.dump(aggregate, f, indent=2)

print(f"Saved → {OUTPUT_FILE}")
print(f"\nQuick summary:")
print(f"  Reviews analyzed : {aggregate['total_reviews_analyzed']}")
print(f"  Avg sentiment    : {aggregate['avg_sentiment']} (scale: -1 to 1)")
print(f"  Avg star rating  : {aggregate['avg_rating']}/5")
print(f"  Top complaint    : {aggregate['top_complaints'][0][0] if aggregate['top_complaints'] else 'N/A'}")
print("\nStep 2 complete. Run step3_dashboard.py next.")