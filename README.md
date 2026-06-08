# SharkNinja Review Intelligence
**AI-powered product review analyzer built with Claude API**

Streams real SharkNinja product reviews from the Amazon Reviews 2023 dataset,
analyzes them with Claude to extract complaints, praises, and feature gaps,
and displays everything in an interactive Streamlit dashboard.

---

## What It Does
- Streams only SharkNinja-branded rows from a 1M+ product dataset — no full download
- Sends review batches to Claude API and gets back structured JSON insights
- Displays sentiment trends, top complaints, feature requests, and an AI executive summary

## Stack
| Layer | Tool | Cost |
|---|---|---|
| Data | Amazon Reviews 2023 (McAuley Lab, UCSD) | Free |
| AI Analysis | Claude API (claude-sonnet-4) | Free tier |
| Dashboard | Streamlit | Free |
| Hosting | Streamlit Community Cloud | Free |

## Setup

```bash
git clone https://github.com/YOUR_USERNAME/sharkninja-review-analyzer
cd sharkninja-review-analyzer
pip install -r requirements.txt
```

Set your Claude API key:
```bash
export ANTHROPIC_API_KEY=your-key-here
```

## Run

```bash
# Step 1: Stream SharkNinja reviews (takes ~10-20 min on first run)
python step1_get_data.py

# Step 2: Analyze with Claude API
python step2_analyze.py

# Step 3: Launch the dashboard
streamlit run step3_dashboard.py
```

## Data Source
Amazon Reviews 2023 — McAuley Lab, UC San Diego  
https://amazon-reviews-2023.github.io/
