# 🦈 Product Review Intelligence

An AI-powered pipeline that analyzes SharkNinja product reviews using Claude API and displays insights in an interactive dashboard.

**Live Demo → [sharkninja-review-analyzer.streamlit.app](https://appuct-review-analyzer-d6kxfzwwi34ttrdaad3slx.streamlit.app)**

---

## What It Does

- Analyzes 500+ SharkNinja product reviews across 9 products (Shark vacuums, Ninja air fryers, blenders)
- Uses Claude API to extract sentiment scores, top complaints, praises, and feature requests per batch
- Generates AI executive summaries a product manager can act on
- Displays everything in an interactive dark-themed dashboard with filterable charts

## Key Findings

| Insight | Result |
|---|---|
| Overall Sentiment | Positive (0.61 / 1.0) |
| Avg Star Rating | 3.95 / 5.0 |
| Top Complaint | Noise level |
| Top Praise | Strong suction power |
| Top Feature Request | Longer power cord |

## Architecture

```
Product Reviews (CSV)
       ↓
Python — cleans and batches reviews
       ↓
Claude API (Messages API) — extracts structured insights as JSON
       ↓
analysis_results.json
       ↓
Streamlit Dashboard — charts, summaries, raw review explorer
```

## Stack

| Layer | Tool | Cost |
|---|---|---|
| Data | Product reviews | Free |
| AI Analysis | Claude API (claude-sonnet-4-5) | Free tier |
| Dashboard | Streamlit + Plotly | Free |
| Hosting | Streamlit Community Cloud | Free |
| Version Control | GitHub | Free |

**Total cost: $0**

## Project Structure

```
sharkninja-review-analyzer/
├── .streamlit/
│   └── config.toml          # Dark purple theme config
├── generate_data.py          # Generates synthetic review dataset
├── analyze.py                # Sends reviews to Claude API, saves JSON
├── step3_dashboard.py        # Streamlit dashboard
├── requirements.txt          # Python dependencies
└── README.md
```

## Run Locally

**1. Clone the repo:**
```bash
git clone https://github.com/YOUR_USERNAME/sharkninja-review-analyzer
cd sharkninja-review-analyzer
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Set your Claude API key:**
```powershell
# Windows PowerShell
$env:ANTHROPIC_API_KEY="sk-ant-your-key-here"

# Mac / Linux
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

**4. Generate data and run analysis:**
```bash
python generate_data.py    # Creates review CSVs
python analyze.py          # Calls Claude API, saves analysis_results.json
```

**5. Launch the dashboard:**
```bash
streamlit run step3_dashboard.py
```
Opens at `localhost:8501`

## Requirements

```
anthropic
pandas
streamlit
plotly
```

Built with Python · Claude API · Streamlit · Plotly
